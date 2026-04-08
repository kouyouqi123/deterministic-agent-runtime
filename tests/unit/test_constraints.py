"""Constraint engine tests."""

from core.events.bus import EventBus, EventType
from core.constraints.engine import (
    ConstraintEngine,
    alive_constraint,
    energy_constraint,
    bounds_constraint,
    obstacle_constraint,
    create_default_engine,
)
from core.models.state import AgentState, WorldState, Position
from core.models.actions import Action, ActionType


def make_world(tick: int = 0) -> WorldState:
    return WorldState(tick=tick, width=10, height=10)


def make_agent(**kwargs: object) -> AgentState:
    return AgentState(**kwargs)  # type: ignore[arg-type]


def make_move(x: int, y: int) -> Action:
    return Action(action_type=ActionType.MOVE, target=Position(x=x, y=y))


class TestAliveConstraint:
    def test_alive_agent_passes(self) -> None:
        result = alive_constraint(
            Action(action_type=ActionType.WAIT),
            make_agent(),
            make_world(),
        )
        assert result.passed is True

    def test_dead_agent_fails(self) -> None:
        result = alive_constraint(
            Action(action_type=ActionType.WAIT),
            make_agent(alive=False),
            make_world(),
        )
        assert result.passed is False
        assert "dead" in result.reason.lower()


class TestEnergyConstraint:
    def test_enough_energy(self) -> None:
        result = energy_constraint(make_move(1, 0), make_agent(energy=50), make_world())
        assert result.passed is True

    def test_insufficient_energy(self) -> None:
        result = energy_constraint(
            Action(action_type=ActionType.ATTACK),
            make_agent(energy=5),
            make_world(),
        )
        assert result.passed is False
        assert "energy" in result.reason.lower()

    def test_wait_needs_no_energy(self) -> None:
        result = energy_constraint(
            Action(action_type=ActionType.WAIT),
            make_agent(energy=0),
            make_world(),
        )
        assert result.passed is True


class TestBoundsConstraint:
    def test_within_bounds(self) -> None:
        result = bounds_constraint(make_move(5, 5), make_agent(), make_world())
        assert result.passed is True

    def test_out_of_bounds(self) -> None:
        result = bounds_constraint(make_move(10, 5), make_agent(), make_world())
        assert result.passed is False

    def test_negative_bounds(self) -> None:
        result = bounds_constraint(make_move(-1, 0), make_agent(), make_world())
        assert result.passed is False

    def test_non_move_skips(self) -> None:
        result = bounds_constraint(
            Action(action_type=ActionType.WAIT), make_agent(), make_world()
        )
        assert result.passed is True


class TestObstacleConstraint:
    def test_clear_path(self) -> None:
        result = obstacle_constraint(make_move(1, 0), make_agent(), make_world())
        assert result.passed is True

    def test_blocked_by_obstacle(self) -> None:
        world = WorldState(obstacles=[Position(x=1, y=0)])
        result = obstacle_constraint(make_move(1, 0), make_agent(), world)
        assert result.passed is False


class TestConstraintEngine:
    def test_all_pass(self) -> None:
        bus = EventBus()
        engine = create_default_engine(bus)
        allowed = engine.is_allowed(make_move(1, 0), make_agent(), make_world())
        assert allowed is True

    def test_dead_blocks(self) -> None:
        bus = EventBus()
        engine = create_default_engine(bus)
        allowed = engine.is_allowed(
            make_move(1, 0), make_agent(alive=False), make_world()
        )
        assert allowed is False

    def test_emits_events(self) -> None:
        bus = EventBus()
        engine = create_default_engine(bus)
        engine.evaluate(make_move(1, 0), make_agent(), make_world())
        checks = bus.get_history(event_type=EventType.CONSTRAINT_CHECKED)
        assert len(checks) == engine.constraint_count

    def test_violation_emits_event(self) -> None:
        bus = EventBus()
        engine = create_default_engine(bus)
        engine.evaluate(make_move(1, 0), make_agent(alive=False), make_world())
        violations = bus.get_history(event_type=EventType.CONSTRAINT_VIOLATED)
        assert len(violations) >= 1
