# Briefing

- Purpose: OAuth2 CGI app that authenticates UW students into class Discord servers and assigns Discord roles based on UW identity.
- Current scope: Python/Flask app deployed as CGI on UW ovid server. Handles Discord OAuth2 login, role add/remove via Discord bot API, optional log-channel messaging. Config via config.py (gitignored; config.example.py provided). Dependencies vendored to pypackages/ via pip -t (gitignored).
- Key decisions: MIT license under Jeremy Zhang (original author). pypackages/.gitkeep removed; directory fully gitignored. Tests use conftest.py to inject fake config so no real config.py is needed to run pytest.
- Non-goals: No CI pipeline. No database. No test coverage for full OAuth token exchange (requires live Discord API).
