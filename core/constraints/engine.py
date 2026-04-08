"""Constraint Engine.

Hard safety limits that run BEFORE any policy evaluation.
Constraints are the first gate in the decision order:
  constraints → interrupts → FSM → utility → planner → LLM → escalation

A constraint that fails blocks the action. Period. No override.
See ADR-001 and AGENTS.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from core.models.state import AgentState, WorldState, Position
from core.models.actions import Action, ActionType
from core.events.bus import EventBus, Event, EventType


@dataclass(frozen=True)
class ConstraintResult:
    """Result of evaluating a single constraint."""

    name: str
    passed: bool
    reason: str = ""


ConstraintFn = Callable[[Action, AgentState, WorldState], ConstraintResult]


class ConstraintEngine:
    """Evaluates all registered constraints against a proposed action.

    All constraints run. If any fail, the action is blocked.
    Results are emitted as events for tracing.
    """

    def __init__(self, event_bus: EventBus) -> None:
        self._constraints: list[ConstraintFn] = []
        self._bus = event_bus

    def register(self, constraint: ConstraintFn) -> None:
        """Register a constraint function."""
        self._constraints.append(constraint)

    def evaluate(
        self,
        action: Action,
        agent: AgentState,
        world: WorldState,
    ) -> list[ConstraintResult]:
        """Evaluate all constraints. Returns results (may include failures)."""
        results: list[ConstraintResult] = []
        for constraint in self._constraints:
            result = constraint(action, agent, world)
            results.append(result)

            event_type = (
                EventType.CONSTRAINT_CHECKED
                if result.passed
                else EventType.CONSTRAINT_VIOLATED
            )
            self._bus.emit(Event(
                event_type=event_type,
                tick=world.tick,
                data={
                    "constraint": result.name,
                    "passed": result.passed,
                    "reason": result.reason,
                    "action": action.action_type.value,
                },
            ))

        return results

    def is_allowed(
        self,
        action: Action,
        agent: AgentState,
        world: WorldState,
    ) -> bool:
        """Check if an action passes ALL constraints."""
        results = self.evaluate(action, agent, world)
        return all(r.passed for r in results)

    @property
    def constraint_count(self) -> int:
        """Number of registered constraints."""
        return len(self._constraints)


# ============================================================================
# Built-in Constraints
# ============================================================================


def alive_constraint(
    action: Action, agent: AgentState, world: WorldState
) -> ConstraintResult:
    """Dead agents cannot act."""
    if not agent.alive:
        return ConstraintResult(name="alive", passed=False, reason="Agent is dead")
    return ConstraintResult(name="alive", passed=True)


def energy_constraint(
    action: Action, agent: AgentState, world: WorldState
) -> ConstraintResult:
    """Actions require minimum energy."""
    min_energy: dict[ActionType, int] = {
        ActionType.MOVE: 5,
        ActionType.ATTACK: 15,
        ActionType.RETREAT: 5,
        ActionType.SCAN: 10,
        ActionType.WAIT: 0,
    }
    required = min_energy.get(action.action_type, 0)
    if agent.energy < required:
        return ConstraintResult(
            name="energy",
            passed=False,
            reason=f"Need {required} energy, have {agent.energy}",
        )
    return ConstraintResult(name="energy", passed=True)


def bounds_constraint(
    action: Action, agent: AgentState, world: WorldState
) -> ConstraintResult:
    """Movement must stay within world bounds."""
    if action.action_type != ActionType.MOVE or action.target is None:
        return ConstraintResult(name="bounds", passed=True)
    t = action.target
    if t.x < 0 or t.x >= world.width or t.y < 0 or t.y >= world.height:
        return ConstraintResult(
            name="bounds",
            passed=False,
            reason=f"Target ({t.x},{t.y}) outside world bounds",
        )
    return ConstraintResult(name="bounds", passed=True)


def obstacle_constraint(
    action: Action, agent: AgentState, world: WorldState
) -> ConstraintResult:
    """Cannot move into obstacles."""
    if action.action_type != ActionType.MOVE or action.target is None:
        return ConstraintResult(name="obstacle", passed=True)
    if action.target in world.obstacles:
        return ConstraintResult(
            name="obstacle",
            passed=False,
            reason=f"Target ({action.target.x},{action.target.y}) is blocked",
        )
    return ConstraintResult(name="obstacle", passed=True)


def create_default_engine(event_bus: EventBus) -> ConstraintEngine:
    """Create a constraint engine with all built-in constraints."""
    engine = ConstraintEngine(event_bus)
    engine.register(alive_constraint)
    engine.register(energy_constraint)
    engine.register(bounds_constraint)
    engine.register(obstacle_constraint)
    return engine
