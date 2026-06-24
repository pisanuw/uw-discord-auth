import pytest
from uwdiscord.app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    # The test client talks http, so a Secure session cookie would not round-trip;
    # relax it here only (production keeps Secure on via OAUTHLIB_INSECURE_TRANSPORT).
    flask_app.config["SESSION_COOKIE_SECURE"] = False
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
    """login() redirect must point at Discord's current OAuth2 endpoint."""
    response = client.get("/login")
    assert response.status_code == 302
    assert "discord.com/api/oauth2/authorize" in response.headers["Location"]


def test_login_stores_redirect_param(client):
    """login() should preserve the redirect query param in the session."""
    response = client.get("/login?redirect=/some/path")
    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert sess.get("redirect") == "/some/path"


# --- API currency: guard against regressing to the retired Discord API ---

def test_uses_current_discord_api_base():
    """The app must target the live Discord API (v10 on discord.com), not the
    retired v6 / legacy discordapp.com domain."""
    from uwdiscord import app as appmod
    assert appmod.DISCORD_API_BASE == "https://discord.com/api/v10"
    assert "discordapp.com" not in appmod.DISCORD_API_BASE
    assert "discordapp.com" not in appmod.DISCORD_TOKEN_URL
    assert "discordapp.com" not in appmod.DISCORD_AUTHORIZE_URL
