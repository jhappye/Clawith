"""Enterprise internal knowledge base retrieval tool."""

from __future__ import annotations

from typing import Any

import requests
from requests import RequestException

from .base_tool import BaseTool


class KnowledgeBaseRetrievalTool(BaseTool):
    name = "enterprise_kb_retrieval"
    description = "Search and retrieve knowledge snippets from enterprise internal knowledge base service."
    parameters = {
        "type": "object",
        "properties": {
            "base_url": {
                "type": "string",
                "description": "Knowledge base API base URL, e.g. https://kb.internal/api",
            },
            "api_key": {
                "type": "string",
                "description": "Bearer API key for internal KB service.",
            },
            "query": {
                "type": "string",
                "description": "Search query text.",
            },
            "top_k": {
                "type": "integer",
                "description": "Number of results to retrieve.",
                "default": 5,
                "minimum": 1,
                "maximum": 20,
            },
            "filters": {
                "type": "object",
                "description": "Optional metadata filters such as department, product, language.",
                "default": {},
            },
            "timeout_seconds": {
                "type": "integer",
                "default": 15,
            },
        },
        "required": ["base_url", "api_key", "query"],
    }

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        base_url = (kwargs.get("base_url", "") or "").rstrip("/")
        api_key = kwargs.get("api_key", "")
        query = kwargs.get("query", "")
        top_k = int(kwargs.get("top_k", 5))
        filters = kwargs.get("filters") or {}
        timeout_seconds = int(kwargs.get("timeout_seconds", 15))

        try:
            if not base_url or not api_key or not query:
                return {
                    "ok": False,
                    "data": None,
                    "error": "base_url, api_key, and query are required",
                }

            safe_top_k = max(1, min(top_k, 20))
            url = f"{base_url}/search"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "query": query,
                "top_k": safe_top_k,
                "filters": filters,
            }

            resp = requests.post(url, headers=headers, json=payload, timeout=timeout_seconds)
            resp.raise_for_status()
            data = resp.json()

            return {
                "ok": True,
                "data": {
                    "query": query,
                    "top_k": safe_top_k,
                    "results": data.get("results", []),
                },
                "error": None,
            }

        except RequestException as e:
            return {"ok": False, "data": None, "error": f"KB service request failed: {str(e)[:300]}"}
        except ValueError as e:
            return {"ok": False, "data": None, "error": f"KB response parse error: {str(e)[:300]}"}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "data": None, "error": f"Unexpected error: {str(e)[:300]}"}
