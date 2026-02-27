"""ProxyPin MCP Server - main entry point."""

from __future__ import annotations

import json
import re
from typing import Any

from mcp.server.fastmcp import FastMCP

from .har_reader import reader
from .models import DetailLevel, RequestFull, RequestSummary

mcp = FastMCP("proxypin")

VALID_DETAILS = {level.value for level in DetailLevel}
VALID_SEARCH_AREAS = {"all", "url", "request_body", "response_body"}
VALID_LANGUAGES = {"python", "javascript", "typescript", "curl"}
VALID_PYTHON_FRAMEWORKS = {"requests", "httpx"}
VALID_JS_FRAMEWORKS = {"fetch", "axios"}


def _json_response(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def _bounded_limit(value: int, default: int, maximum: int) -> int:
    if value <= 0:
        return default
    return min(value, maximum)


@mcp.tool()
def list_requests(
    limit: int = 20,
    detail: str = "summary",
    domain: str | None = None,
    method: str | None = None,
    status: int | None = None,
) -> str:
    """List recent HTTP requests captured by ProxyPin."""
    normalized_limit = _bounded_limit(limit, default=20, maximum=100)
    normalized_detail = detail.lower().strip()
    detail_level = (
        DetailLevel(normalized_detail)
        if normalized_detail in VALID_DETAILS
        else DetailLevel.SUMMARY
    )

    requests = reader.get_requests(
        limit=normalized_limit,
        detail_level=detail_level,
        domain=domain,
        method=method,
        status_code=status,
    )
    return _json_response([request.model_dump() for request in requests])


@mcp.tool()
def get_request(
    request_id: str,
    include_body: bool = True,
) -> str:
    """Get detailed information for a single request."""
    if not request_id.strip():
        return _json_response({"error": "request_id is required"})

    detail_level = DetailLevel.FULL if include_body else DetailLevel.KEY
    request = reader.get_request_by_id(request_id, detail_level)
    if request is None:
        return _json_response({"error": f"Request {request_id} not found"})

    result = request.model_dump()
    if isinstance(request, RequestFull):
        result["curl_command"] = request.to_curl()
    return _json_response(result)


@mcp.tool()
def search_requests(
    keyword: str,
    search_in: str = "all",
    limit: int = 20,
) -> str:
    """Search requests by keyword."""
    if not keyword.strip():
        return _json_response({"error": "keyword is required"})

    normalized_search_in = search_in if search_in in VALID_SEARCH_AREAS else "all"
    normalized_limit = _bounded_limit(limit, default=20, maximum=100)
    results = reader.search(keyword, normalized_search_in, normalized_limit)
    return _json_response(results)


@mcp.tool()
def analyze_api(domain: str) -> str:
    """Analyze API structure for a domain."""
    normalized_domain = domain.strip()
    if not normalized_domain:
        return _json_response({"error": "domain is required"})

    requests = reader.get_requests(
        limit=300,
        detail_level=DetailLevel.KEY,
        domain=normalized_domain,
    )

    endpoints: dict[str, dict[str, Any]] = {}
    for req in requests:
        path = req.path or "/"
        normalized = re.sub(r"/\d+", "/{id}", path)
        normalized = re.sub(r"/[a-f0-9-]{32,}", "/{uuid}", normalized, flags=re.IGNORECASE)

        key = f"{req.method} {normalized}"
        endpoint = endpoints.setdefault(
            key,
            {
                "method": req.method,
                "path": normalized,
                "count": 0,
                "statuses": set(),
                "has_auth": False,
                "request_structure": None,
                "response_structure": None,
                "sample_url": req.url,
            },
        )
        endpoint["count"] += 1
        if req.status is not None:
            endpoint["statuses"].add(req.status)
        if req.has_auth:
            endpoint["has_auth"] = True
        if req.request_body_structure and not endpoint["request_structure"]:
            endpoint["request_structure"] = req.request_body_structure
        if req.response_body_structure and not endpoint["response_structure"]:
            endpoint["response_structure"] = req.response_body_structure

    endpoints_list: list[dict[str, Any]] = []
    result: dict[str, Any] = {
        "domain": normalized_domain,
        "total_requests": len(requests),
        "endpoints_count": len(endpoints),
        "endpoints": endpoints_list,
    }
    for _, endpoint in sorted(endpoints.items(), key=lambda item: -item[1]["count"]):
        endpoints_list.append(
            {
                "method": endpoint["method"],
                "path": endpoint["path"],
                "count": endpoint["count"],
                "statuses": sorted(endpoint["statuses"]),
                "has_auth": endpoint["has_auth"],
                "request_structure": endpoint["request_structure"],
                "response_structure": endpoint["response_structure"],
                "sample_url": endpoint["sample_url"],
            }
        )
    return _json_response(result)


@mcp.tool()
def get_domains() -> str:
    """Get list of all captured domains with request counts."""
    requests = reader.get_requests(limit=500, detail_level=DetailLevel.SUMMARY)

    domains: dict[str, dict[str, Any]] = {}
    for req in requests:
        if not isinstance(req, RequestSummary) or not req.host:
            continue
        entry = domains.setdefault(req.host, {"count": 0, "methods": set()})
        entry["count"] += 1
        entry["methods"].add(req.method)

    result = [
        {
            "domain": domain,
            "count": info["count"],
            "methods": sorted(info["methods"]),
        }
        for domain, info in sorted(domains.items(), key=lambda item: -item[1]["count"])
    ]
    return _json_response(result)


@mcp.tool()
def generate_code(
    request_id: str,
    language: str = "python",
    framework: str = "requests",
) -> str:
    """Generate API call code from a captured request."""
    normalized_language = language.lower().strip()
    if normalized_language not in VALID_LANGUAGES:
        return f"# Error: unsupported language '{language}'. Use one of {sorted(VALID_LANGUAGES)}"

    request = reader.get_request_by_id(request_id, DetailLevel.FULL)
    if request is None:
        return f"# Error: Request {request_id} not found"

    if normalized_language == "curl":
        return request.to_curl()
    if normalized_language == "python":
        normalized_framework = framework.lower().strip()
        if normalized_framework not in VALID_PYTHON_FRAMEWORKS:
            normalized_framework = "requests"
        return _gen_python(request, normalized_framework)

    normalized_framework = framework.lower().strip()
    if normalized_framework not in VALID_JS_FRAMEWORKS:
        normalized_framework = "fetch"
    return _gen_js(request, normalized_framework)


def _safe_headers(req: RequestFull) -> dict[str, str]:
    return {
        key: values[0]
        for key, values in req.request_headers.items()
        if values and key.lower() not in ("host", "content-length", "connection")
    }


def _gen_python(req: RequestFull, framework: str) -> str:
    """Generate Python code."""
    lines = []
    headers = _safe_headers(req)
    method = req.method.upper()

    if framework == "httpx":
        lines.extend(["import asyncio", "import httpx", "", "async def main():"])
        indent = "    "
    else:
        lines.extend(["import requests", ""])
        indent = ""

    lines.append(f"{indent}method = {json.dumps(method)}")
    lines.append(f"{indent}url = {json.dumps(req.url, ensure_ascii=False)}")
    if headers:
        lines.append(f"{indent}headers = {json.dumps(headers, ensure_ascii=False)}")

    payload_param = ""
    if req.request_body_json is not None:
        lines.append(f"{indent}payload = {json.dumps(req.request_body_json, ensure_ascii=False)}")
        payload_param = ", json=payload"
    elif req.request_body:
        lines.append(f"{indent}payload = {json.dumps(req.request_body, ensure_ascii=False)}")
        payload_param = ", data=payload"

    headers_param = ", headers=headers" if headers else ""
    lines.append("")

    if framework == "httpx":
        lines.append(f"{indent}async with httpx.AsyncClient(timeout=30) as client:")
        lines.append(
            f"{indent}    response = await client.request("
            f"method, url{headers_param}{payload_param})"
        )
        lines.append(f"{indent}    print(response.status_code)")
        lines.append(f"{indent}    print(response.text)")
        lines.append("")
        lines.append("asyncio.run(main())")
    else:
        lines.append(
            f"response = requests.request(method, url{headers_param}{payload_param}, timeout=30)"
        )
        lines.append("print(response.status_code)")
        lines.append("print(response.text)")

    return "\n".join(lines)


def _gen_js(req: RequestFull, framework: str) -> str:
    """Generate JavaScript/TypeScript code."""
    lines = []
    headers = _safe_headers(req)
    method = req.method.upper()

    if framework == "axios":
        lines.append("import axios from 'axios';")
        lines.append("")
        config: dict[str, Any] = {"method": method, "url": req.url}
        if headers:
            config["headers"] = headers
        if req.request_body_json is not None:
            config["data"] = req.request_body_json
        elif req.request_body:
            config["data"] = req.request_body

        lines.append(f"const config = {json.dumps(config, indent=2, ensure_ascii=False)};")
        lines.append("")
        lines.append("axios(config)")
        lines.append("  .then((response) => console.log(response.data))")
        lines.append("  .catch((error) => console.error(error));")
        return "\n".join(lines)

    lines.append(f"const url = {json.dumps(req.url, ensure_ascii=False)};")
    options: dict[str, Any] = {"method": method}
    if headers:
        options["headers"] = headers
    lines.append(f"const options = {json.dumps(options, indent=2, ensure_ascii=False)};")

    if req.request_body_json is not None:
        lines.append(
            "options.body = JSON.stringify("
            f"{json.dumps(req.request_body_json, ensure_ascii=False)});"
        )
    elif req.request_body:
        lines.append(f"options.body = {json.dumps(req.request_body, ensure_ascii=False)};")

    lines.append("")
    lines.append("fetch(url, options)")
    lines.append("  .then((response) => response.text())")
    lines.append("  .then((text) => console.log(text))")
    lines.append("  .catch((error) => console.error('Error:', error));")
    return "\n".join(lines)


# ==================== Resources ====================


@mcp.resource("proxypin://requests/recent")
def recent_requests_resource() -> str:
    """Recent requests summary."""
    requests = reader.get_requests(limit=30, detail_level=DetailLevel.SUMMARY)
    return json.dumps([r.model_dump() for r in requests], ensure_ascii=False, indent=2)


@mcp.resource("proxypin://domains")
def domains_resource() -> str:
    """List of captured domains."""
    return get_domains()


# ==================== Prompts ====================


@mcp.prompt()
def analyze_api_prompt(domain: str) -> str:
    """Prompt for API analysis."""
    return f"""Analyze the API structure for domain: {domain}

Steps:
1. Use analyze_api tool to get endpoint list
2. Identify RESTful patterns and resources
3. Analyze authentication methods
4. Document request/response structures
5. Generate API documentation outline

Start analysis."""


@mcp.prompt()
def debug_request_prompt(request_id: str) -> str:
    """Prompt for debugging a request."""
    return f"""Debug request: {request_id}

Steps:
1. Use get_request tool to get full details
2. Check request parameters and headers
3. Analyze response status and body
4. Identify potential issues
5. Suggest fixes

Start debugging."""


# ==================== Main ====================


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
