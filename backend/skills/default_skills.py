"""Default skill presets for NexusMind Agents.

This file provides declarative default skill definitions used when creating
new agents (e.g. Customer Service Agent, PMC Assistant).
Replace all {{placeholders}} with your tenant-specific settings before use.
"""

from dataclasses import dataclass, field
from typing import Literal


SkillLevel = Literal["L1", "L2", "L3"]


@dataclass
class SkillSpec:
    key: str
    name: str
    description: str
    level: SkillLevel
    enabled: bool = True
    config: dict = field(default_factory=dict)


# ─────────────────────────────────────────────────────────────
# Base skills for all agents
# ─────────────────────────────────────────────────────────────
BASE_DEFAULT_SKILLS: list[SkillSpec] = [
    SkillSpec(
        key="kb_retrieval",
        name="Knowledge Base Retrieval",
        description="Read and cite enterprise knowledge files using citation format 【来源: 文件名#章节】.",
        level="L1",
        config={
            "kb_paths": [
                "enterprise_info/{{kb_business_file}}",
                "enterprise_info/{{kb_policy_file}}",
                "workspace/knowledge_base/{{team_kb_file}}",
            ],
            "citation_required": True,
        },
    ),
    SkillSpec(
        key="structured_response",
        name="Structured Response",
        description="Respond with fixed structure: 结论 -> 依据 -> 步骤 -> 风险 -> 下一步.",
        level="L1",
    ),
    SkillSpec(
        key="collaboration_handoff",
        name="Collaboration Handoff",
        description="Escalate and hand off with complete context package to human/agent collaborators.",
        level="L2",
        config={
            "handoff_targets": ["{{owner_name}}", "{{reviewer_name}}", "{{backup_owner_name}}"],
            "required_fields": ["summary", "impact", "attempted_actions", "risk_level"],
        },
    ),
    SkillSpec(
        key="permission_guard",
        name="Permission Guard",
        description="Block prohibited actions and require approval for L2 operations.",
        level="L1",
        config={
            "approval_required_actions": [
                "external_commitment",
                "refund_or_compensation",
                "sensitive_data_export",
            ],
            "forbidden_actions": [
                "secret_exfiltration",
                "policy_bypass",
                "unauthorized_data_change",
            ],
        },
    ),
]


# ─────────────────────────────────────────────────────────────
# Customer service agent skill bundle
# ─────────────────────────────────────────────────────────────
CUSTOMER_SERVICE_SKILLS: list[SkillSpec] = [
    SkillSpec(
        key="intent_classification",
        name="Customer Intent Classification",
        description="Classify customer issue type, urgency and route to proper queue.",
        level="L1",
        config={
            "categories": [
                "{{category_account}}",
                "{{category_billing}}",
                "{{category_technical}}",
                "{{category_other}}",
            ],
            "priority_rule": "{{priority_rule}}",
        },
    ),
    SkillSpec(
        key="customer_reply_playbook",
        name="Customer Reply Playbook",
        description="Generate empathetic, policy-compliant responses with SLA awareness.",
        level="L1",
        config={
            "sla_first_response_minutes": "{{first_response_sla}}",
            "sla_resolution_hours": "{{resolution_sla}}",
            "tone": "friendly_professional",
        },
    ),
    SkillSpec(
        key="ticket_escalation",
        name="Ticket Escalation",
        description="Escalate complex/high-risk cases to L2 support with full context.",
        level="L2",
        config={
            "escalation_targets": {
                "support_l1": "{{support_l1_owner}}",
                "support_l2": "{{support_l2_owner}}",
                "tech_support": "{{tech_support_owner}}",
            },
            "escalation_conditions": [
                "security_incident",
                "refund_over_threshold",
                "unresolved_after_n_attempts",
            ],
        },
    ),
]


# ─────────────────────────────────────────────────────────────
# PMC assistant skill bundle (Planning / Monitoring / Coordination)
# ─────────────────────────────────────────────────────────────
PMC_ASSISTANT_SKILLS: list[SkillSpec] = [
    SkillSpec(
        key="plan_breakdown",
        name="Plan Breakdown",
        description="Break goals into milestones, owners, dependencies and due dates.",
        level="L1",
        config={
            "milestone_template": "{{milestone_template}}",
            "default_cycle": "{{planning_cycle}}",
        },
    ),
    SkillSpec(
        key="risk_tracking",
        name="Risk Tracking",
        description="Track project risks and generate mitigation actions with owner assignment.",
        level="L1",
        config={
            "risk_matrix": "{{risk_matrix_rule}}",
            "alert_threshold": "{{risk_alert_threshold}}",
        },
    ),
    SkillSpec(
        key="progress_reporting",
        name="Progress Reporting",
        description="Generate weekly/daily progress summary for stakeholders.",
        level="L1",
        config={
            "report_audience": ["{{pm_owner}}", "{{biz_owner}}", "{{tech_owner}}"],
            "report_format": "summary_with_blockers_and_next_steps",
        },
    ),
    SkillSpec(
        key="cross_team_coordination",
        name="Cross-team Coordination",
        description="Synchronize dependencies across teams and trigger escalation when blocked.",
        level="L2",
        config={
            "dependency_timeout_hours": "{{dependency_timeout_hours}}",
            "escalation_to": "{{program_manager}}",
        },
    ),
]


DEFAULT_SKILL_BUNDLES = {
    "base": BASE_DEFAULT_SKILLS,
    "customer_service": CUSTOMER_SERVICE_SKILLS,
    "pmc_assistant": PMC_ASSISTANT_SKILLS,
}
