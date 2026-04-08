# Agent & Contributor Non-Negotiables

This file is authoritative. It applies to all contributors — human and AI.

## Runtime Owns Control

The runtime makes decisions. The LLM advises. This is not negotiable.

- The system MUST be fully usable without any LLM attached
- The LLM MUST NOT manage authoritative state
- The LLM MUST NOT directly execute arbitrary actions
- The LLM MUST NOT bypass constraints

## Decision Order (mandatory)

Every decision follows this order. No exceptions.

1. **Constraints** — hard safety limits, always checked first
2. **Interrupts** — time-critical overrides
3. **FSM / Behavior Tree** — deterministic policy selection
4. **Utility Scoring** — ranked option evaluation
5. **Planner** — multi-step action planning
6. **LLM Advisory** — bounded, schema-validated suggestions
7. **Operator Escalation** — human-in-the-loop fallback

## What This Project Is NOT

- NOT a prompt-driven autonomous agent
- NOT a framework that lets models "think" their way to actions
- NOT a place for "clever" abstractions before working code exists
- NOT a playground for trendy agent-framework patterns

## Banned Patterns

- Model as runtime brain
- Giant abstract framework before one scenario works
- God plugins with wide interfaces
- Loose JSON blobs instead of typed models
- Replay as an afterthought
- "Smart" adapters that make decisions autonomously
- Policy changes without tests
- Hidden global state
- Unreviewed LLM-generated policy changes

## Required for Every PR

- [ ] Tests pass (unit + integration + scenario)
- [ ] Type checks clean
- [ ] Lint clean
- [ ] Decision traces work for affected paths
- [ ] Replay not broken
- [ ] No new untyped data structures
- [ ] No constraint bypasses

## Standards

Follow `nexus-agents/CODING_STANDARDS.md` for all implementation decisions.
When in doubt: correctness > simplicity > performance > cleverness.
