# CCA-F Hands-On Track — Project List & 1-Month Study Plan

> **Source of truth:** `guide_en.MD` (official exam guide). Every project below maps to specific practice questions (marked **Q#**, referring to the 76-question set) and to the guide's exam scenarios. Implementation reference: official Anthropic docs listed in the guide (Agent SDK, Claude Code, MCP, Claude API).
>
> **Prime directive of this track:** No theory chapter is "done" until its project checkpoint is built and working. Reading twice is forbidden; building twice is encouraged.

---

# PART A — Hands-On Projects by Domain

Seven projects. Each one lists: goal, docs, concrete steps, exam mapping, and a "you're done when" checkpoint. Projects 1–2 (Domain 1) are the core — they carry 27% of the exam and target your biggest gap (Agent SDK).

---

## Project 1 — Support Agent with Full Agentic Loop (Domain 1, core)

**Exam scenario:** Customer Support Agent (Scenario 1)
**Question mapping:** Q46–Q60 — especially Q58 (loop control via `stop_reason`), Q53 (parallel tool calls per loop), Q48 (loop efficiency), Q47 (multi-issue requests), Q54 (context loss across turns)
**Docs:** Agent SDK Overview · Claude API Tool Use · Messages API

**Build:**

1. Define 4 mock MCP-style tools: `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`. Implement them as simple Python functions returning canned JSON (no real backend needed — the exam tests architecture, not infra).
2. Write the raw agent loop yourself first (plain Messages API, no SDK): call → inspect `stop_reason` → if `"tool_use"`, execute every `tool_use` block in the response, return results as `tool_result` blocks with matching `tool_use_id`, loop; if `"end_turn"`, stop. This is Q58 verbatim.
3. Deliberately break it three ways and observe: (a) return results for only one of two tool calls, (b) mismatch a `tool_use_id`, (c) treat `max_tokens` stop as `end_turn`. Log what the API returns each time.
4. Test with a multi-issue message ("refund order #1234 AND update my address") — verify the agent handles both aspects (Q47).
5. Add escalation: a rule that routes to `escalate_to_human` on policy exceptions but NOT on standard cases (the 55%→80% resolution problem, Q49/Q3).
6. Re-implement the same agent with the Claude Agent SDK using `AgentDefinition` + `allowedTools`. Compare: what does the SDK handle for you that you wrote by hand in step 2?

**Done when:** you can explain, without notes, what happens after each of the three deliberate breaks in step 3, and your agent resolves a multi-issue request in one conversation.

---
