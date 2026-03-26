"""Enterprise ticket system tool: create/query tickets."""

from __future__ import annotations

from typing import Any, Literal

import requests
from requests import RequestException

from .base_tool import BaseTool


class TicketSystemTool(BaseTool):
    name = "enterprise_ticket_system"
    description = "Create or query tickets in enterprise ticketing system."
    parameters = {
        "type": "object",
        "properties": {
            "base_url": {"type": "string", "description": "Ticket system API base URL"},
            "api_token": {"type": "string", "description": "API token for ticket system"},
            "action": {
                "type": "string",
                "enum": ["create", "query"],
                "description": "create: create a ticket; query: query existing ticket(s)",
            },
            "title": {"type": "string", "description": "Ticket title (required for create)"},
            "description": {"type": "string", "description": "Ticket description (required for create)"},
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "urgent"],
                "default": "medium",
            },
            "assignee": {"type": "string", "description": "Optional assignee identifier"},
            "ticket_id": {"type": "string", "description": "Ticket ID for query by id"},
            "query_params": {
                "type": "object",
                "description": "Optional query filters, e.g. status/owner/date_range",
                "default": {},
            },
            "timeout_seconds": {"type": "integer", "default": 15},
        },
        "required": ["base_url", "api_token", "action"],
    }

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        base_url = (kwargs.get("base_url", "") or "").rstrip("/")
        api_token = kwargs.get("api_token", "")
        action: Literal["create", "query"] = kwargs.get("action", "query")
        timeout_seconds = int(kwargs.get("timeout_seconds", 15))

        try:
            if not base_url or not api_token:
                return {"ok": False, "data": None, "error": "base_url and api_token are required"}

            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            }

            if action == "create":
                title = kwargs.get("title", "")
                description = kwargs.get("description", "")
                if not title or not description:
                    return {
                        "ok": False,
                        "data": None,
                        "error": "title and description are required for create action",
                    }

                payload = {
                    "title": title,
                    "description": description,
                    "priority": kwargs.get("priority", "medium"),
                    "assignee": kwargs.get("assignee"),
                }
                resp = requests.post(
                    f"{base_url}/tickets",
                    headers=headers,
                    json=payload,
                    timeout=timeout_seconds,
                )
                resp.raise_for_status()
                return {"ok": True, "data": resp.json(), "error": None}

            if action == "query":
                ticket_id = kwargs.get("ticket_id")
                if ticket_id:
                    resp = requests.get(
                        f"{base_url}/tickets/{ticket_id}",
                        headers=headers,
                        timeout=timeout_seconds,
                    )
                else:
                    params = kwargs.get("query_params") or {}
                    resp = requests.get(
                        f"{base_url}/tickets",
                        headers=headers,
                        params=params,
                        timeout=timeout_seconds,
                    )
                resp.raise_for_status()
                return {"ok": True, "data": resp.json(), "error": None}

            return {"ok": False, "data": None, "error": f"Unsupported action: {action}"}

        except RequestException as e:
            return {"ok": False, "data": None, "error": f"Ticket system request failed: {str(e)[:300]}"}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "data": None, "error": f"Unexpected error: {str(e)[:300]}"}
