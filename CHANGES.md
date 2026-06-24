# Changes

Format: `YYYY-MM-DD [type] description` (max 200 chars). Types: decision, plan, doc, scope, code, note.

2026-06-10 [note] Initialized.
2026-06-10 [code] Removed pypackages/.gitkeep from git; simplified .gitignore to ignore pypackages/ entirely
2026-06-10 [code] Added tests/conftest.py + tests/test_oauth.py: 6 tests for OAuth state validation and callback error paths
2026-06-10 [code] Added MIT LICENSE; added requirements-dev.txt with pytest
2026-06-10 [decision] LICENSE copyright holder set to Jeremy Zhang (original author)

2026-06-24 [code] Modernized Discord API to v10 on discord.com (was retired v6 on discordapp.com); hoisted endpoints to constants; added regression test
2026-06-24 [code] Hardened security: Secure/HttpOnly/SameSite session cookie, refuse-to-boot on placeholder app-secret, run.py defaults to localhost with debug off, log InvalidGrantError before 401
2026-06-24 [code] Added GitHub Actions CI (ruff + pytest, Python 3.10-3.13) on push and PR; added ruff.toml
2026-06-24 [code] Pinned dependencies: requirements.in compiled to a fully-pinned requirements.txt lock; pinned dev tools
2026-06-24 [doc] README: added CI badge, provenance/credits to Jeremy Zhang, development/test instructions; updated dev portal link
