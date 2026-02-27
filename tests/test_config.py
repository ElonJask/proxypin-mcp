from pathlib import Path

from proxypin_mcp import config as config_module


def test_get_proxypin_data_dir_from_env(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("PROXYPIN_DATA_DIR", str(tmp_path))
    assert config_module.get_proxypin_data_dir() == Path(tmp_path)


def test_get_har_files_limit_invalid_value(monkeypatch) -> None:
    monkeypatch.setenv("PROXYPIN_HAR_LIMIT", "invalid")
    assert config_module.get_har_files_limit() == config_module.DEFAULT_HAR_LIMIT


def test_get_max_body_size_out_of_range(monkeypatch) -> None:
    monkeypatch.setenv("PROXYPIN_MAX_BODY_SIZE", "10")
    assert config_module.get_max_body_size() == config_module.DEFAULT_MAX_BODY_SIZE
