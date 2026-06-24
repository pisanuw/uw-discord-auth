# Briefing

- Purpose: OAuth2 CGI app that authenticates UW students into class Discord servers and assigns Discord roles based on UW identity.
- Current scope: Python/Flask app deployed as CGI on UW ovid server. Handles Discord OAuth2 login, role add/remove via Discord bot API, optional log-channel messaging. Config via config.py (gitignored; config.example.py provided). Dependencies vendored to pypackages/ via pip -t (gitignored).
- Key decisions: MIT license under Jeremy Zhang (original author); README credits him as author of the core app, this copy is a maintained fork. pypackages/.gitkeep removed; directory fully gitignored. Tests use conftest.py to inject fake config so no real config.py is needed to run pytest. CI (ruff + pytest, Python 3.10-3.13) runs on push and PR. Runtime deps pinned via requirements.in -> requirements.txt lock. Session cookie Secure/HttpOnly/SameSite hardened; app refuses to boot on a placeholder app-secret; run.py defaults to localhost with debug off. Discord API modernized to v10 on discord.com.
- Non-goals: No database. No test coverage for full OAuth token exchange (requires live Discord API).
