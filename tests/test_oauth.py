import pytest
from uwdiscord.app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# --- callback: state validation ---

def test_callback_no_state_in_session_redirects_with_state_error(client):
    """Missing oauth2_state in session must redirect to logout (CSRF guard)."""
    response = client.get("/callback")
    assert response.status_code == 302
    location = response.headers["Location"]
    assert "logout" in location
    assert "state_error" in location


def test_callback_state_present_but_discord_returns_error(client):
    """Discord error query param should redirect to logout with discord_error."""
    with client.session_transaction() as sess:
        sess["oauth2_state"] = "a-valid-state-token"
    response = client.get("/callback?error=access_denied")
    assert response.status_code == 302
    location = response.headers["Location"]
    assert "logout" in location
    assert "discord_error" in location


def test_callback_error_value_is_forwarded(client):
    """The specific Discord error string should appear in the redirect location."""
    with client.session_transaction() as sess:
        sess["oauth2_state"] = "a-valid-state-token"
    response = client.get("/callback?error=temporarily_unavailable")
    location = response.headers["Location"]
    assert "temporarily_unavailable" in location


# --- login: state generation ---

def test_login_stores_oauth_state_in_session(client):
    """login() must store a non-empty oauth2_state in the session."""
    response = client.get("/login")
    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert "oauth2_state" in sess
        assert sess["oauth2_state"]


def test_login_redirects_to_discord_authorization_url(client):
    """login() redirect must point at Discord's OAuth2 endpoint."""
    response = client.get("/login")
    assert response.status_code == 302
    assert "discordapp.com" in response.headers["Location"]


def test_login_stores_redirect_param(client):
    """login() should preserve the redirect query param in the session."""
    response = client.get("/login?redirect=/some/path")
    with client.session_transaction() as sess:
        assert sess.get("redirect") == "/some/path"
