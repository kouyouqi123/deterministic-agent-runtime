# Anti-Patterns — What This Project Must Never Become

## Model as Runtime Brain

The LLM does not decide what happens. It advises. The runtime's constraint engine, FSM, and utility scoring make the actual decisions. If the LLM says "attack" but constraints say "retreat", the agent retreats.

## Giant Abstract Framework Before Use Case

One scenario must work end-to-end before any generalization. If you're building an abstraction and can't point to two working use cases that need it, you're over-engineering.

## God Plugins

Plugins have narrow, explicit contracts. A plugin that can read all state, emit arbitrary events, and bypass constraints is not a plugin — it's a backdoor.

## Loose JSON Blobs Instead of Typed Models

Every data structure that crosses a module boundary must be typed. No `dict[str, Any]`. No `kwargs`. No "flexible" schemas that defer validation to runtime.

## Replay as an Afterthought

If replay doesn't work after your change, your change is broken. Decision traces are first-class. The replay log is not optional logging — it's a core data structure.

## "Smart" Adapters That Make Decisions

Adapters translate between the runtime and external systems. They do not decide what to do. Adapters are dumb pipes. Decision logic lives in policies.

## Policy Changes Without Tests

Every policy (FSM transition, utility function, constraint rule) must have a test that verifies its behavior. Untested policies are bugs waiting to happen.

## Hidden Global State

State is explicit, owned by the runtime, and passed through typed interfaces. No module-level globals. No singletons that accumulate state. No implicit context.

## Prompt Soup

Prompts are versioned, schema-validated, and logged. No prompt construction via string concatenation. No prompts that embed decision logic. The runtime decides — prompts are input to a bounded advisory layer.

## Unreviewed LLM Policy Improvements

If the LLM suggests a policy change, it is a **candidate** that must be tested, reviewed, and approved. LLM suggestions never auto-deploy.
