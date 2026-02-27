"""HAR file reader for ProxyPin."""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Generator
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .config import config
from .models import (
    DetailLevel,
    RequestFull,
    RequestKey,
    RequestSummary,
    extract_json_structure,
    truncate_body,
)

LOGGER = logging.getLogger(__name__)
VALID_SEARCH_AREAS = {"all", "url", "request_body", "response_body"}


def _as_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _entry_id(entry: dict[str, Any]) -> str:
    raw_id = _as_text(entry.get("_id"))
    if raw_id:
        return raw_id

    request = entry.get("request", {}) or {}
    response = entry.get("response", {}) or {}
    seed = "|".join(
        [
            _as_text(request.get("method", "GET")),
            _as_text(request.get("url", "")),
            _as_text(entry.get("startedDateTime", "")),
            _as_text(response.get("status", "")),
        ]
    )
    digest = hashlib.sha1(seed.encode("utf-8", errors="ignore")).hexdigest()[:20]
    return f"auto-{digest}"


def _duration_ms(entry: dict[str, Any]) -> int | None:
    time_value = entry.get("time")
    if time_value in (None, ""):
        return None
    try:
        return int(float(str(time_value)))
    except (ValueError, TypeError):
        return None


def _parse_query_params(parsed_url: Any) -> dict[str, str]:
    if not parsed_url.query:
        return {}

    result: dict[str, str] = {}
    for key, values in parse_qs(parsed_url.query).items():
        result[key] = values[0] if len(values) == 1 else str(values)
    return result


def _build_headers(items: list[dict[str, Any]]) -> dict[str, list[str]]:
    headers: dict[str, list[str]] = {}
    for item in items:
        name = _as_text(item.get("name")).strip()
        value = _as_text(item.get("value"))
        if not name:
            continue
        headers.setdefault(name, []).append(value)
    return headers


def _domain_matches(filter_text: str, url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    needle = filter_text.lower()
    if host:
        return needle in host
    return needle in url.lower()


class HarReader:
    """Read and parse ProxyPin HAR files."""

    def __init__(self, data_dir: Path | None = None):
        self.data_dir = data_dir or config.data_dir

    def get_har_files(self) -> list[Path]:
        """Get HAR files sorted by modification time (newest first)."""
        if not self.data_dir.exists():
            LOGGER.debug("ProxyPin data dir does not exist: %s", self.data_dir)
            return []

        files = list(self.data_dir.glob("*.txt")) + list(self.data_dir.glob("*.har"))
        files.sort(key=lambda path: path.stat().st_mtime, reverse=True)
        return files[: config.har_files_limit]

    def read_entries(self, limit: int = 100) -> Generator[dict[str, Any], None, None]:
        """Read HAR entries from files."""
        if limit <= 0:
            return

        count = 0
        for har_file in self.get_har_files():
            if count >= limit:
                break

            for entry in self._parse_file(har_file):
                if not isinstance(entry, dict):
                    continue
                yield entry
                count += 1
                if count >= limit:
                    break

    def _parse_file(self, file_path: Path) -> Generator[dict[str, Any], None, None]:
        """Parse a single HAR/txt file."""
        try:
            with file_path.open("r", encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    normalized = line.strip().rstrip(",")
                    if not normalized:
                        continue
                    try:
                        yield json.loads(normalized)
                    except json.JSONDecodeError:
                        continue
        except OSError as exc:
            LOGGER.warning("Failed to read %s: %s", file_path, exc)
            return

    def get_requests(
        self,
        limit: int = 20,
        detail_level: DetailLevel = DetailLevel.SUMMARY,
        domain: str | None = None,
        method: str | None = None,
        status_code: int | None = None,
    ) -> list[Any]:
        """Get requests with specified detail level."""
        normalized_limit = max(1, min(limit, 500))
        results: list[Any] = []

        read_limit = min(normalized_limit * 5, 2500)
        for entry in self.read_entries(limit=read_limit):
            req = entry.get("request", {}) or {}
            resp = entry.get("response", {}) or {}
            url = _as_text(req.get("url"))

            if domain and not _domain_matches(domain, url):
                continue
            if method and _as_text(req.get("method")).upper() != method.upper():
                continue
            if status_code is not None and resp.get("status") != status_code:
                continue

            if detail_level == DetailLevel.SUMMARY:
                results.append(self._to_summary(entry))
            elif detail_level == DetailLevel.KEY:
                results.append(self._to_key(entry))
            else:
                results.append(self._to_full(entry))

            if len(results) >= normalized_limit:
                break

        return results

    def get_request_by_id(
        self,
        request_id: str,
        detail_level: DetailLevel = DetailLevel.FULL,
    ) -> Any | None:
        """Get a single request by ID."""
        for entry in self.read_entries(limit=2000):
            if _entry_id(entry) != request_id:
                continue

            if detail_level == DetailLevel.SUMMARY:
                return self._to_summary(entry)
            if detail_level == DetailLevel.KEY:
                return self._to_key(entry)
            return self._to_full(entry)
        return None

    def search(
        self,
        keyword: str,
        search_in: str = "all",
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Search requests by keyword."""
        normalized_limit = max(1, min(limit, 500))
        scope = search_in if search_in in VALID_SEARCH_AREAS else "all"
        needle = keyword.lower()
        results = []

        for entry in self.read_entries(limit=2500):
            matches = []
            req = entry.get("request", {}) or {}
            resp = entry.get("response", {}) or {}

            url = _as_text(req.get("url")).lower()
            if scope in ("all", "url") and needle in url:
                matches.append("url")

            req_body = _as_text((req.get("postData", {}) or {}).get("text"))
            if scope in ("all", "request_body") and needle in req_body.lower():
                matches.append("request_body")

            resp_body = _as_text((resp.get("content", {}) or {}).get("text"))
            if scope in ("all", "response_body") and needle in resp_body.lower():
                matches.append("response_body")

            if not matches:
                continue

            summary = self._to_summary(entry)
            results.append({**summary.model_dump(), "_matches": matches})
            if len(results) >= normalized_limit:
                break

        return results

    def _to_summary(self, entry: dict[str, Any]) -> RequestSummary:
        """Convert entry to summary."""
        req = entry.get("request", {}) or {}
        resp = entry.get("response", {}) or {}
        url = _as_text(req.get("url"))
        parsed = urlparse(url)

        app_name = None
        app_info = entry.get("_app")
        if isinstance(app_info, dict):
            app_name = _as_text(app_info.get("name")) or None

        return RequestSummary(
            id=_entry_id(entry),
            method=_as_text(req.get("method", "GET")) or "GET",
            url=url,
            host=parsed.hostname,
            path=parsed.path,
            status=resp.get("status"),
            duration_ms=_duration_ms(entry),
            timestamp=_as_text(entry.get("startedDateTime")) or None,
            app_name=app_name,
        )

    def _to_key(self, entry: dict[str, Any]) -> RequestKey:
        """Convert entry to key info."""
        req = entry.get("request", {}) or {}
        resp = entry.get("response", {}) or {}
        url = _as_text(req.get("url"))
        parsed = urlparse(url)

        query_params = _parse_query_params(parsed)

        req_body = _as_text((req.get("postData", {}) or {}).get("text"))
        req_body_preview = None
        req_body_structure = None
        body_truncated = False
        if req_body:
            req_body_preview, body_truncated = truncate_body(
                req_body,
                config.key_body_preview_length,
            )
            try:
                req_body_structure = extract_json_structure(json.loads(req_body))
            except (json.JSONDecodeError, TypeError):
                pass

        resp_body = _as_text((resp.get("content", {}) or {}).get("text"))
        resp_body_preview = None
        resp_body_structure = None
        if resp_body:
            resp_body_preview, _ = truncate_body(resp_body, config.key_body_preview_length)
            try:
                resp_body_structure = extract_json_structure(json.loads(resp_body))
            except (json.JSONDecodeError, TypeError):
                pass

        req_headers = _build_headers(req.get("headers", []) or [])
        lower_headers = {key.lower(): ",".join(values) for key, values in req_headers.items()}
        has_auth = any(key in lower_headers for key in ("authorization", "x-token", "x-api-key"))
        content_type = lower_headers.get("content-type", "")
        is_json = "json" in content_type.lower()

        return RequestKey(
            id=_entry_id(entry),
            method=_as_text(req.get("method", "GET")) or "GET",
            url=url,
            host=parsed.hostname,
            path=parsed.path,
            status=resp.get("status"),
            duration_ms=_duration_ms(entry),
            timestamp=_as_text(entry.get("startedDateTime")) or None,
            query_params=query_params,
            content_type=content_type or None,
            request_body_preview=req_body_preview,
            request_body_structure=req_body_structure,
            response_body_preview=resp_body_preview,
            response_body_structure=resp_body_structure,
            has_auth=has_auth,
            is_json=is_json,
            body_truncated=body_truncated,
        )

    def _to_full(self, entry: dict[str, Any]) -> RequestFull:
        """Convert entry to full info."""
        req = entry.get("request", {}) or {}
        resp = entry.get("response", {}) or {}
        url = _as_text(req.get("url"))
        parsed = urlparse(url)

        req_headers = _build_headers(req.get("headers", []) or [])
        resp_headers = _build_headers(resp.get("headers", []) or [])
        query_params = _parse_query_params(parsed)

        req_body = _as_text((req.get("postData", {}) or {}).get("text"))
        req_body_json = None
        body_truncated = False
        if req_body:
            if len(req_body) > config.max_body_size:
                req_body, body_truncated = truncate_body(req_body, config.max_body_size)
            try:
                req_body_json = json.loads(req_body)
            except (json.JSONDecodeError, TypeError):
                pass

        resp_body = _as_text((resp.get("content", {}) or {}).get("text"))
        resp_body_json = None
        if resp_body:
            if len(resp_body) > config.max_body_size:
                resp_body, body_truncated = truncate_body(resp_body, config.max_body_size)
            try:
                resp_body_json = json.loads(resp_body)
            except (json.JSONDecodeError, TypeError):
                pass

        app_info = entry.get("_app", {}) or {}
        cookies = [
            value
            for key, values in req_headers.items()
            if key.lower() == "cookie"
            for value in values
        ]

        return RequestFull(
            id=_entry_id(entry),
            method=_as_text(req.get("method", "GET")) or "GET",
            url=url,
            protocol=_as_text(req.get("httpVersion", "HTTP/1.1")) or "HTTP/1.1",
            host=parsed.hostname,
            port=parsed.port or (443 if parsed.scheme == "https" else 80),
            path=parsed.path,
            query_string=parsed.query,
            query_params=query_params,
            status=resp.get("status"),
            status_text=_as_text(resp.get("statusText")) or None,
            duration_ms=_duration_ms(entry),
            timestamp=_as_text(entry.get("startedDateTime")) or None,
            request_headers=req_headers,
            response_headers=resp_headers,
            request_body=req_body or None,
            request_body_json=req_body_json,
            response_body=resp_body or None,
            response_body_json=resp_body_json,
            remote_ip=_as_text(entry.get("serverIPAddress")) or None,
            is_https=parsed.scheme == "https",
            app_id=_as_text(app_info.get("id")) or None,
            app_name=_as_text(app_info.get("name")) or None,
            app_path=_as_text(app_info.get("path")) or None,
            cookies=cookies,
            body_truncated=body_truncated,
        )


reader = HarReader()
