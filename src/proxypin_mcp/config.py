"""Configuration for ProxyPin MCP Server."""

import logging
import os
import sys
from pathlib import Path

LOGGER = logging.getLogger(__name__)

DEFAULT_HAR_LIMIT = 50
DEFAULT_MAX_BODY_SIZE = 1024 * 100  # 100 KB


def _read_int_env(
    key: str,
    default: int,
    minimum: int,
    maximum: int | None = None,
) -> int:
    value = os.environ.get(key)
    if value is None:
        return default

    try:
        parsed = int(value)
    except ValueError:
        LOGGER.warning("Ignoring invalid %s=%r, fallback to %d", key, value, default)
        return default

    if parsed < minimum or (maximum is not None and parsed > maximum):
        LOGGER.warning(
            "Ignoring out-of-range %s=%r, expected %d..%s, fallback to %d",
            key,
            value,
            minimum,
            maximum if maximum is not None else "inf",
            default,
        )
        return default
    return parsed


def get_proxypin_data_dir() -> Path:
    """Get ProxyPin history directory based on platform."""
    env_dir = os.environ.get("PROXYPIN_DATA_DIR")
    if env_dir:
        return Path(env_dir).expanduser()

    if sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
        candidates = [
            base / "com.proxy.pin" / "history",
            base / "ProxyPin" / "history",
        ]
    elif sys.platform == "win32":
        appdata = os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))
        base = Path(appdata)
        candidates = [
            base / "com.proxy.pin" / "history",
            base / "ProxyPin" / "history",
        ]
    else:
        base = Path.home() / ".config"
        candidates = [
            base / "com.proxy.pin" / "history",
            base / "proxypin" / "history",
            Path.home() / ".proxypin" / "history",
        ]

    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


def get_har_files_limit() -> int:
    """Get maximum number of HAR files to scan."""
    return _read_int_env("PROXYPIN_HAR_LIMIT", DEFAULT_HAR_LIMIT, minimum=1, maximum=1000)


def get_max_body_size() -> int:
    """Get maximum response/request body size in bytes before truncation."""
    return _read_int_env(
        "PROXYPIN_MAX_BODY_SIZE",
        DEFAULT_MAX_BODY_SIZE,
        minimum=1024,
        maximum=10 * 1024 * 1024,
    )


class Config:
    """Global configuration."""

    def __init__(self) -> None:
        self.data_dir = get_proxypin_data_dir()
        self.har_files_limit = get_har_files_limit()
        self.max_body_size = get_max_body_size()

        # Token-efficient defaults
        self.default_list_limit = 20
        self.summary_body_preview_length = 200
        self.key_body_preview_length = 500


config = Config()
