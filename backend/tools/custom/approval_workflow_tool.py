"""Enterprise approval workflow tool: submit and track approvals."""

from __future__ import annotations

from typing import Any, Literal

import requests
from requests import RequestException

from .base_tool import BaseTool


class ApprovalWorkflowTool(BaseTool):
    name = "enterprise_approval_workflow"
    description = "Submit approval requests and query approval status from enterprise approval system."
    parameters = {
        "type": "object",
        "properties": {
            "base_url": {"type": "string", "description": "Approval API base URL"},
            "api_token": {"type": "string", "description": "API token for approval service"},
            "action": {
                "type": "string",
                "enum": ["submit", "status"],
                "description": "submit: initiate approval; status: query approval status",
            },
            "title": {"type": "string", "description": "Approval title (submit)"},
            "form_data": {
                "type": "object",
                "description": "Approval form payload (submit)",
                "default": {},
            },
            "approvers": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of approver IDs (submit)",
                "default": [],
            },
            "request_id": {"type": "string", "description": "Approval request ID (status)"},
            "timeout_seconds": {"type": "integer", "default": 15},
        },
        "required": ["base_url", "api_token", "action"],
    }

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        base_url = (kwargs.get("base_url", "") or "").rstrip("/")
        api_token = kwargs.get("api_token", "")
        action: Literal["submit", "status"] = kwargs.get("action", "status")
        timeout_seconds = int(kwargs.get("timeout_seconds", 15))

        try:
            if not base_url or not api_token:
                return {"ok": False, "data": None, "error": "base_url and api_token are required"}

            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            }

            if action == "submit":
                title = kwargs.get("title", "")
                form_data = kwargs.get("form_data") or {}
                approvers = kwargs.get("approvers") or []
                if not title or not approvers:
                    return {
                        "ok": False,
                        "data": None,
                        "error": "title and approvers are required for submit action",
                    }

                payload = {
                    "title": title,
                    "form_data": form_data,
                    "approvers": approvers,
                    "requester": kwargs.get("requester", "{{requester_id}}"),
                }
                resp = requests.post(
                    f"{base_url}/approvals",
                    headers=headers,
                    json=payload,
                    timeout=timeout_seconds,
                )
                resp.raise_for_status()
                return {"ok": True, "data": resp.json(), "error": None}

            if action == "status":
                request_id = kwargs.get("request_id", "")
                if not request_id:
                    return {
                        "ok": False,
                        "data": None,
                        "error": "request_id is required for status action",
                    }

                resp = requests.get(
                    f"{base_url}/approvals/{request_id}",
                    headers=headers,
                    timeout=timeout_seconds,
                )
                resp.raise_for_status()
                return {"ok": True, "data": resp.json(), "error": None}

            return {"ok": False, "data": None, "error": f"Unsupported action: {action}"}

        except RequestException as e:
            return {"ok": False, "data": None, "error": f"Approval service request failed: {str(e)[:300]}"}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "data": None, "error": f"Unexpected error: {str(e)[:300]}"}
