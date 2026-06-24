import sys
import types

_fake_config = types.ModuleType("config")
_fake_config.config = {
    "app-secret": "test-secret-key-for-sessions",
    "client-id": "test-client-id",
    "client-secret": "test-client-secret",
    "bot-token": "test-bot-token",
    "discords": [],
}
sys.modules.setdefault("config", _fake_config)
