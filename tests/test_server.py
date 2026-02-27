import json

from proxypin_mcp import server
from proxypin_mcp.models import RequestSummary


def test_list_requests_falls_back_to_summary_detail(monkeypatch) -> None:
    fake_requests = [RequestSummary(id="1", method="GET", url="https://example.com", status=200)]

    def fake_get_requests(**kwargs):
        assert kwargs["detail_level"].value == "summary"
        return fake_requests

    monkeypatch.setattr(server.reader, "get_requests", fake_get_requests)

    result = json.loads(server.list_requests(limit=5, detail="unknown"))
    assert result[0]["id"] == "1"


def test_search_requests_requires_keyword() -> None:
    result = json.loads(server.search_requests(keyword="   "))
    assert result["error"] == "keyword is required"


def test_generate_code_rejects_unknown_language() -> None:
    result = server.generate_code(request_id="req-1", language="go")
    assert "unsupported language" in result
