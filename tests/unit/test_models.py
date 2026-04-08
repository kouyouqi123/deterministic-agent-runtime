"""Tests for core typed models.

Verifies that all state models, actions, goals, and traces
are correctly typed and behave as expected.
"""

from core.models.state import WorldState, AgentState, Position
from core.models.actions import Action, ActionResult, ActionType
from core.models.goals import Goal, GoalStatus
from core.models.traces import DecisionTrace, DecisionReason


class TestPosition:
    def test_default_origin(self) -> None:
        pos = Position()
        assert pos.x == 0
        assert pos.y == 0

    def test_custom_position(self) -> None:
        pos = Position(x=5, y=3)
        assert pos.x == 5
        assert pos.y == 3


class TestWorldState:
    def test_default_state(self) -> None:
        state = WorldState()
        assert state.tick == 0
        assert state.width == 10
        assert state.height == 10
        assert state.obstacles == []
        assert state.threats == []

    def test_with_obstacles(self) -> None:
        state = WorldState(obstacles=[Position(x=1, y=2), Position(x=3, y=4)])
        assert len(state.obstacles) == 2


class TestAgentState:
    def test_default_alive(self) -> None:
        agent = AgentState()
        assert agent.alive is True
        assert agent.health == 100
        assert agent.energy == 100

    def test_damaged_agent(self) -> None:
        agent = AgentState(health=50, energy=30)
        assert agent.health == 50
        assert agent.energy == 30


class TestAction:
    def test_move_action(self) -> None:
        action = Action(
            action_type=ActionType.MOVE,
            target=Position(x=1, y=0),
            reason="Moving toward objective",
        )
        assert action.action_type == ActionType.MOVE
        assert action.target is not None
        assert action.target.x == 1


class TestActionResult:
    def test_successful_result(self) -> None:
        action = Action(action_type=ActionType.WAIT)
        result = ActionResult(action=action, success=True, message="Waited", tick=5)
        assert result.success is True
        assert result.tick == 5


class TestGoal:
    def test_active_goal(self) -> None:
        goal = Goal(name="clear_area", description="Clear all threats")
        assert goal.status == GoalStatus.ACTIVE

    def test_completed_goal(self) -> None:
        goal = Goal(name="retreat", status=GoalStatus.COMPLETED)
        assert goal.status == GoalStatus.COMPLETED


class TestDecisionTrace:
    def test_trace_records_decision(self) -> None:
        action = Action(action_type=ActionType.RETREAT, reason="Low health")
        trace = DecisionTrace(
            tick=42,
            selected_action=action,
            reasons=[
                DecisionReason(stage="constraint", description="Health below 20%"),
            ],
            constraints_checked=["min_health"],
            constraints_violated=[],
        )
        assert trace.tick == 42
        assert trace.selected_action.action_type == ActionType.RETREAT
        assert len(trace.reasons) == 1
        assert trace.constraints_violated == []
