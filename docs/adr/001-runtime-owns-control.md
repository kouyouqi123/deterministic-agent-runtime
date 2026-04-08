# ADR-001: Runtime Owns Execution Control

## Status

Accepted

## Context

Modern agent frameworks often give LLMs direct control over execution — the model decides what to do, tools execute it, and the model decides again. This creates non-deterministic, hard-to-debug, hard-to-audit systems.

Pre-agentic automation (game AI, robotics, industrial control) solved these problems decades ago with deterministic runtimes that use explicit state machines, constraint engines, and utility scoring.

## Decision

The runtime — not the LLM — owns execution control. The decision order is:

1. Constraints (hard safety limits)
2. Interrupts (time-critical overrides)
3. FSM / Behavior Tree (deterministic policy selection)
4. Utility Scoring (ranked option evaluation)
5. Planner (multi-step action planning)
6. LLM Advisory (bounded, schema-validated suggestions)
7. Operator Escalation (human-in-the-loop)

The LLM is treated as a bounded advisor that cannot:
- Manage authoritative state
- Directly execute actions
- Bypass constraints
- Override the FSM or constraint engine

## Consequences

- System is fully functional without any LLM attached
- Every decision is traceable and replayable
- Safety constraints are guaranteed, not probabilistic
- LLM integration is additive, not foundational
- Development starts with deterministic scenarios before any model integration
