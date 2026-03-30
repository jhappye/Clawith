"""Seed team collaboration templates and trigger examples into system settings."""

import json
from pathlib import Path

from loguru import logger
from sqlalchemy import select

from app.database import async_session
from app.models.system_settings import SystemSetting


_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"


def _load_json(filename: str) -> dict:
    p = _TEMPLATE_DIR / filename
    return json.loads(p.read_text(encoding="utf-8"))


async def seed_team_collaboration_templates() -> None:
    """Upsert team collaboration templates into `system_settings`.

    Keys:
    - team_collaboration_template_v1
    - team_collaboration_rules_v1
    - team_trigger_examples_v1
    """

    payloads = {
        "team_collaboration_template_v1": _load_json("team_collaboration_template.json"),
        "team_collaboration_rules_v1": _load_json("team_collaboration_rules.json"),
        "team_trigger_examples_v1": _load_json("task_flow_triggers_example.json"),
    }

    async with async_session() as db:
        for key, value in payloads.items():
            result = await db.execute(select(SystemSetting).where(SystemSetting.key == key))
            existing = result.scalar_one_or_none()
            if existing:
                existing.value = value
            else:
                db.add(SystemSetting(key=key, value=value))
        await db.commit()

    logger.info("[TeamCollabSeeder] Team collaboration templates seeded")
