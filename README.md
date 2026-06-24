# uw-discord-auth

[![CI](https://github.com/pisanuw/uw-discord-auth/actions/workflows/ci.yml/badge.svg)](https://github.com/pisanuw/uw-discord-auth/actions/workflows/ci.yml)

Authentication for UW Discords. An OAuth2 CGI web app that authenticates UW students into class Discord servers and assigns Discord roles based on their identity.

## Provenance and credits

The original application was designed and written by **Jeremy Zhang** ([@EndenDragon](https://github.com/EndenDragon)) during a UW Bothell Independent Study; the OAuth flow, Discord API client, and CGI deployment in `uwdiscord/` and `application.cgi` are his work, and the project is MIT-licensed under his copyright (see `LICENSE`). This `pisanuw` copy is a maintained fork by Yusuf Pisan: the test suite (`tests/`), CI, dependency pinning, and the security/API-currency hardening described in `CHANGES.md` were added here. Please credit Jeremy Zhang as the author of the core application.

## Installation
1. Clone project within `public_html` (if on `ovid`) and `cd` into the directory.
2. `python3 -m pip install -r requirements.txt -t pypackages/`
3. Remove dataclasses from pypackages `rm pypackages/dataclasses.py`
    - It currently crashes the site due to python version differences between server and web execution platform.
4. Copy `config.example.py` into `config.py` and edit the values. The app refuses to start if `app-secret` is missing or left at a placeholder, so set a strong random secret. You may obtain Discord IDs by [enabling Developer Mode](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) and then right clicking the relevant portion of the Discord UI to access the Copy ID context menu option.
5. Edit `.htaccess` `RewriteRule` portion to your url. For instance, if the `application.cgi` file is located within `/rc00/d00/jkzhang/public_html/uw-discord-auth` directory (`pwd` command output on `ovid`), the `.htaccess` RewriteRule will contain `/jkzhang/uw-discord-auth/application.cgi/`.
6. Visit the [Discord Developer Portal](https://discord.com/developers/applications), select your application, and proceed to the OAuth2 tab. Add a redirect url entry such as `https://staff.washington.edu/jkzhang/uw-discord-auth/callback`, modified so the callback url points at your installation.

The app targets the current Discord API (`v10` on `discord.com`).

## Development and tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

ruff check .   # lint
pytest -q      # run the test suite
```

The tests inject a fake `config` module via `tests/conftest.py`, so no real `config.py` or Discord credentials are needed to run them. CI runs `ruff` and `pytest` on every push and pull request across Python 3.10 to 3.13.

## Local run (development only)

```bash
python run.py   # serves on 127.0.0.1:3000; set HOST/PORT/FLASK_DEBUG to override
```

`run.py` is a local development entrypoint only. It binds to localhost and keeps the Werkzeug debugger off unless you set `FLASK_DEBUG=1`. Production is served via `application.cgi`, not `run.py`.
