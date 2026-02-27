"""Data models for ProxyPin MCP Server - Token-efficient design."""

import shlex
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DetailLevel(str, Enum):
    """Data detail level for token efficiency."""

    SUMMARY = "summary"  # ~50 tokens per request
    KEY = "key"  # ~200 tokens per request
    FULL = "full"  # ~2000+ tokens per request


class RequestSummary(BaseModel):
    """Minimal request info - for listing (low token cost)."""

    id: str
    method: str
    url: str
    host: str | None = None
    path: str | None = None
    status: int | None = None
    duration_ms: int | None = None
    timestamp: str | None = None
    app_name: str | None = None

    def to_line(self) -> str:
        """One-line summary."""
        status = self.status or "pending"
        duration = f"{self.duration_ms}ms" if self.duration_ms else "N/A"
        return f"[{self.method}] {self.url} -> {status} ({duration})"


class RequestKey(BaseModel):
    """Key request info - for initial analysis (medium token cost)."""

    id: str
    method: str
    url: str
    host: str | None = None
    path: str | None = None
    status: int | None = None
    duration_ms: int | None = None
    timestamp: str | None = None

    # Key info only
    query_params: dict[str, str] = Field(default_factory=dict)
    content_type: str | None = None
    request_body_preview: str | None = None
    request_body_structure: Any | None = None  # JSON structure only
    response_body_preview: str | None = None
    response_body_structure: Any | None = None

    # Flags
    has_auth: bool = False
    is_json: bool = False
    body_truncated: bool = False


class RequestFull(BaseModel):
    """Full request info - for deep debugging (high token cost)."""

    id: str
    method: str
    url: str
    protocol: str = "HTTP/1.1"
    host: str | None = None
    port: int | None = None
    path: str | None = None
    query_string: str | None = None
    query_params: dict[str, str] = Field(default_factory=dict)

    status: int | None = None
    status_text: str | None = None
    duration_ms: int | None = None
    timestamp: str | None = None

    # Full headers
    request_headers: dict[str, list[str]] = Field(default_factory=dict)
    response_headers: dict[str, list[str]] = Field(default_factory=dict)

    # Full body
    request_body: str | None = None
    request_body_json: Any | None = None
    response_body: str | None = None
    response_body_json: Any | None = None

    # Connection info
    remote_ip: str | None = None
    is_https: bool = False

    # Client app info
    app_id: str | None = None
    app_name: str | None = None
    app_path: str | None = None

    # Metadata
    cookies: list[str] = Field(default_factory=list)
    body_truncated: bool = False

    def to_curl(self) -> str:
        """Generate cURL command."""
        parts = [f"curl -X {shlex.quote(self.method.upper())}"]
        parts.append(shlex.quote(self.url))

        for name, values in self.request_headers.items():
            if name.lower() not in ("host", "content-length"):
                for value in values:
                    parts.append(f"-H {shlex.quote(f'{name}: {value}')}")

        if self.request_body:
            parts.append(f"--data-raw {shlex.quote(self.request_body)}")

        return " \\\n  ".join(parts)


def extract_json_structure(data: Any, max_depth: int = 3, current_depth: int = 0) -> Any:
    """Extract JSON structure without actual values (for token efficiency).

    Example: {"users": [{"id": 1, "name": "John"}]}
          -> {"users": [{"id": "int", "name": "string"}]}
    """
    if current_depth >= max_depth:
        return "..."

    if data is None:
        return "null"
    elif isinstance(data, bool):
        return "bool"
    elif isinstance(data, int):
        return "int"
    elif isinstance(data, float):
        return "float"
    elif isinstance(data, str):
        return "string"
    elif isinstance(data, list):
        if not data:
            return []
        # Only show structure of first item
        return [extract_json_structure(data[0], max_depth, current_depth + 1)]
    elif isinstance(data, dict):
        return {
            k: extract_json_structure(v, max_depth, current_depth + 1)
            for k, v in list(data.items())[:10]  # Limit to 10 keys
        }
    else:
        return str(type(data).__name__)


def truncate_body(body: str, max_length: int) -> tuple[str, bool]:
    """Truncate body and return (truncated_body, was_truncated)."""
    if len(body) <= max_length:
        return body, False
    return body[:max_length] + "...[truncated]", True
