
import os
import sys

TESTING_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TESTING_DIR)
API_DIR = os.path.join(REPO_ROOT, "RECSYS_V2_API")

for path in (REPO_ROOT, API_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

_TEST_ENV_DEFAULTS = {
    "password": "test_password",
    "host": "localhost",
    "port": "5432",
    "database": "test_db",
    "user": "test_user",
    "memory_cost": "19456",
    "time_cost": "2",
    "parallelism": "1",
    "secret_key": "test_secret_key_for_pytest_only_padded_to_32_bytes",
    "algorithm": "HS256",
    "expiry_time": "30",
    "max_file_size": "2000000000",
}

for key, value in _TEST_ENV_DEFAULTS.items():
    os.environ.setdefault(key, value)

import types

if "streamlit" not in sys.modules:
    try:
        import streamlit  # noqa: F401
    except ImportError:
        fake_streamlit = types.ModuleType("streamlit")
        fake_streamlit.error = lambda *args, **kwargs: None
        fake_streamlit.user = None
        sys.modules["streamlit"] = fake_streamlit
