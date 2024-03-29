from .base import *  # noqa: F401,F403

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3001",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
DEBUG = True
