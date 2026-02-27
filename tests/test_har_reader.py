import json

from proxypin_mcp.har_reader import HarReader
from proxypin_mcp.models import DetailLevel


def _write_json_lines(path, items) -> None:
    path.write_text("\n".join(json.dumps(item) for item in items), encoding="utf-8")


def test_har_reader_generates_stable_id_for_entries_without__id(tmp_path) -> None:
    entry = {
        "startedDateTime": "2026-02-27T12:00:00.000Z",
        "time": 123.4,
        "request": {
            "method": "POST",
            "url": "https://api.example.com/v1/login",
            "headers": [{"name": "Content-Type", "value": "application/json"}],
            "postData": {"text": '{"username":"demo"}'},
        },
        "response": {
            "status": 200,
            "statusText": "OK",
            "content": {"text": '{"ok":true}'},
        },
    }
    har_file = tmp_path / "sample.txt"
    _write_json_lines(har_file, [entry])

    reader = HarReader(tmp_path)
    summary = reader.get_requests(limit=1, detail_level=DetailLevel.SUMMARY)[0]
    full = reader.get_request_by_id(summary.id, detail_level=DetailLevel.FULL)

    assert summary.id.startswith("auto-")
    assert full is not None
    assert full.id == summary.id


def test_search_handles_non_string_body_values(tmp_path) -> None:
    entry = {
        "_id": "req-1",
        "request": {
            "method": "POST",
            "url": "https://api.example.com/v1/search",
            "postData": {"text": {"query": "needle"}},
        },
        "response": {"status": 200, "content": {"text": None}},
    }
    har_file = tmp_path / "sample.txt"
    _write_json_lines(har_file, [entry])

    reader = HarReader(tmp_path)
    results = reader.search("needle", search_in="request_body", limit=10)

    assert len(results) == 1
    assert results[0]["id"] == "req-1"
    assert "request_body" in results[0]["_matches"]
