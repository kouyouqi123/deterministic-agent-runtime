# Architecture Principles

## 1. Runtime Owns Control

The runtime — not the LLM — makes all authoritative decisions. The LLM is a bounded advisor that proposes options, but the runtime evaluates, constrains, and executes.

## 2. Deterministic Before Probabilistic

Every decision path tries deterministic logic first: constraints, FSM transitions, utility scoring, planning. LLM advisory is the last resort before operator escalation.

## 3. Typed Everything

All data flows through typed models: WorldState, AgentState, Action, ActionResult, Goal, Anomaly, DecisionTrace. No loose dictionaries, no unvalidated JSON blobs.

## 4. Replayability is a Product Feature

Every meaningful run produces a decision trace that can be replayed, inspected, and compared. Replay is not an afterthought — it's built into the core loop from day one.

## 5. Behavior is Code

Policies (FSM transitions, utility functions, constraint rules) are versioned, tested, and reviewed like code. No "magic" behavior that exists only in prompts or configuration that can't be tested.

## 6. Separation of Observed and Inferred

- **Observed facts**: sensor data, action results, timestamps — authoritative
- **Inferred state**: derived from observations via deterministic rules — secondary
- **Hypotheses**: speculative state from heuristics — clearly labeled
- **Model suggestions**: LLM output — never authoritative, always logged

## 7. Small, Focused Modules

Each module does one thing. Composability over monoliths. Narrow interfaces over wide ones. Plugins have explicit contracts — no god objects.

## 8. Earn Abstractions

Don't build frameworks before use cases. Start with one scenario. Extract patterns only after they appear in working code at least twice.
