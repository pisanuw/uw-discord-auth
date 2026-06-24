import os

# Local development runner only. Discord OAuth requires https in production; this
# allows http on localhost. The production entrypoint is application.cgi, not this
# file. The env var is set before importing the app so the app can relax the
# Secure-cookie flag for local http (see uwdiscord/app.py).
os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

from uwdiscord.app import app  # noqa: E402  (import intentionally follows env setup)

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "3000"))
    # Debug is off by default; the Werkzeug debugger is a remote-code-execution
    # surface. Opt in explicitly with FLASK_DEBUG=1 on a trusted local machine.
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host=host, port=port, debug=debug)
