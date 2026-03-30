"""Base class for custom enterprise tools."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Abstract base class for all custom tools.

    Each tool should provide:
    - name
    - description
    - parameters (JSON-schema-like dict)
    - execute() implementation
    """

    name: str = ""
    description: str = ""
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {},
        "required": [],
    }

    @abstractmethod
    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute tool logic and return a structured result.

        Returns:
            dict: {
                "ok": bool,
                "data": Any,
                "error": str | None,
            }
        """
        raise NotImplementedError
