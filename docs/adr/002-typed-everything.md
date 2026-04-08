# ADR-002: Typed State Models and Decision Traces

## Status

Accepted

## Context

Agent systems often pass unvalidated dictionaries between components, making debugging difficult and errors silent. The game AI tradition uses strongly typed state models where every piece of data has a known structure.

## Decision

All data structures that cross module boundaries must be typed:

- `WorldState` — observable environment state (authoritative)
- `AgentState` — agent's internal state (authoritative)
- `Action` — what the agent wants to do
- `ActionResult` — what happened when it tried
- `Goal` — what the agent is trying to achieve
- `Anomaly` — unexpected observations or failures
- `DecisionTrace` — full record of why a decision was made

Observed facts, inferred state, hypotheses, and model suggestions are kept in distinct data structures — never mixed.

## Consequences

- Every bug is reproducible with a trace
- Type checkers catch integration errors at build time
- Replay is straightforward — traces contain all decision context
- No "what was this dict supposed to contain?" debugging sessions
