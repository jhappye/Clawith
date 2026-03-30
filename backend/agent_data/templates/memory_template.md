# Memory Template — {{agent_name}}

## A. Agent Profile Snapshot
- Agent Name: {{agent_name}}
- Role: {{agent_role}}
- Team: {{team_name}}
- Owner: {{owner_name}}
- Last Updated At: {{updated_at}}

## B. Long-term Stable Facts
> 存储长期有效、复用频率高的信息。

### B1. Business Context
- Company Goal: {{company_goal}}
- Core Product: {{core_product}}
- Target Users: {{target_users}}

### B2. Operating Constraints
- Compliance Requirements: {{compliance_rules}}
- Data Security Level: {{data_security_level}}
- Hard Boundaries: {{hard_boundaries}}

## C. Collaboration Memory
> 记录与人类或其他 Agent 的协作偏好与协议。

- Preferred Stakeholders: {{preferred_stakeholders}}
- Escalation Path: {{escalation_path}}
- Decision Makers: {{decision_makers}}
- Communication Preferences: {{communication_preferences}}

## D. Task Memory (Rolling)
> 记录任务级记忆，用于跨会话连续性。

### D1. Active Goals
- [ ] {{active_goal_1}}
- [ ] {{active_goal_2}}

### D2. Blockers
- {{blocker_1}}
- {{blocker_2}}

### D3. Recent Decisions
- {{decision_1}} (by {{decision_owner_1}} at {{decision_time_1}})
- {{decision_2}} (by {{decision_owner_2}} at {{decision_time_2}})

## E. Knowledge Base References
> 用于建立“记忆 ↔ 知识库”映射，避免凭空生成。

- Primary KB: `enterprise_info/{{primary_kb_file}}`
- Policy KB: `enterprise_info/{{policy_kb_file}}`
- Team KB: `workspace/knowledge_base/{{team_kb_file}}`
- Citation Rule: `【来源: 文件名#章节】`

## F. Memory Write Rules
1. 只写入已确认信息，不记录猜测。
2. 每条关键记忆必须标注来源和时间。
3. 可过期信息必须标注有效期：`valid_until={{valid_until}}`。
4. 涉及敏感信息仅记录摘要，不存原始密钥/隐私数据。

## G. Memory Cleanup Rules
- 每 {{cleanup_cycle}} 天回顾一次：
  - 删除过期策略
  - 合并重复条目
  - 标记待确认条目
- 清理责任人: {{memory_maintainer}}

---

> 使用说明：该模板适合作为每个 Agent 的 `memory.md` 初始结构。
