"""Enterprise internal database query tool."""

from __future__ import annotations

from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from .base_tool import BaseTool


class DatabaseQueryTool(BaseTool):
    name = "enterprise_database_query"
    description = "Query enterprise internal database with read-only SQL and optional bind params."
    parameters = {
        "type": "object",
        "properties": {
            "database_url": {
                "type": "string",
                "description": "SQLAlchemy database URL, e.g. postgresql+psycopg://user:pass@host:5432/db",
            },
            "sql": {
                "type": "string",
                "description": "Read-only SQL query. Only SELECT statements are allowed.",
            },
            "params": {
                "type": "object",
                "description": "Optional named parameters for SQL query.",
                "default": {},
            },
            "limit": {
                "type": "integer",
                "description": "Max rows to return (safety cap).",
                "default": 200,
                "minimum": 1,
                "maximum": 1000,
            },
        },
        "required": ["database_url", "sql"],
    }

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        database_url = kwargs.get("database_url", "")
        sql = (kwargs.get("sql", "") or "").strip()
        params = kwargs.get("params") or {}
        limit = int(kwargs.get("limit", 200))

        try:
            if not database_url:
                return {"ok": False, "data": None, "error": "database_url is required"}
            if not sql:
                return {"ok": False, "data": None, "error": "sql is required"}

            # Basic safety guard: enforce read-only query
            lowered = sql.lower().lstrip()
            if not lowered.startswith("select"):
                return {"ok": False, "data": None, "error": "Only SELECT queries are allowed"}

            safe_limit = max(1, min(limit, 1000))
            wrapped_sql = f"SELECT * FROM ({sql}) AS _q LIMIT {safe_limit}"

            engine = create_engine(database_url, pool_pre_ping=True)
            with engine.connect() as conn:
                result = conn.execute(text(wrapped_sql), params)
                rows = [dict(row._mapping) for row in result.fetchall()]

            return {
                "ok": True,
                "data": {
                    "row_count": len(rows),
                    "rows": rows,
                    "limit": safe_limit,
                },
                "error": None,
            }

        except SQLAlchemyError as e:
            return {"ok": False, "data": None, "error": f"Database error: {str(e)[:300]}"}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "data": None, "error": f"Unexpected error: {str(e)[:300]}"}
