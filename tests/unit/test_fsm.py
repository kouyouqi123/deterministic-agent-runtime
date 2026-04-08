"""Agent FSM tests."""

from core.models.state import AgentState, WorldState, Position
from core.models.actions import ActionType
from policies.fsm.agent_fsm import AgentFSM, AgentMode


class TestAgentFSM:
    def test_starts_exploring(self) -> None:
        fsm = AgentFSM()
        assert fsm.mode == AgentMode.EXPLORE

    def test_retreats_on_low_health(self) -> None:
        fsm = AgentFSM()
        agent = AgentState(health=20, position=Position(x=5, y=5))
        world = WorldState(threats=[Position(x=8, y=8)])
        mode = fsm.update(agent, world)
        assert mode == AgentMode.RETREAT

    def test_retreats_on_low_energy(self) -> None:
        fsm = AgentFSM()
        agent = AgentState(energy=5, position=Position(x=5, y=5))
        world = WorldState(threats=[Position(x=8, y=8)])
        mode = fsm.update(agent, world)
        assert mode == AgentMode.RETREAT

    def test_engages_nearby_threat(self) -> None:
        fsm = AgentFSM()
        agent = AgentState(position=Position(x=5, y=5))
        world = WorldState(threats=[Position(x=6, y=5)])
        mode = fsm.update(agent, world)
        assert mode == AgentMode.ENGAGE

    def test_explores_when_threats_far(self) -> None:
        fsm = AgentFSM()
        agent = AgentState(position=Position(x=0, y=0))
        world = WorldState(threats=[Position(x=9, y=9)])
        mode = fsm.update(agent, world)
        assert mode == AgentMode.EXPLORE

    def test_done_when_no_threats(self) -> None:
        fsm = AgentFSM()
        agent = AgentState(position=Position(x=0, y=0))
        world = WorldState(threats=[])
        mode = fsm.update(agent, world)
        assert mode == AgentMode.DONE

    def test_done_when_dead(self) -> None:
        fsm = AgentFSM()
        agent = AgentState(alive=False)
        world = WorldState(threats=[Position(x=5, y=5)])
        mode = fsm.update(agent, world)
        assert mode == AgentMode.DONE

    def test_retreat_action(self) -> None:
        fsm = AgentFSM()
        agent = AgentState(health=10)
        world = WorldState(threats=[Position(x=5, y=5)])
        fsm.update(agent, world)
        action = fsm.select_action(agent, world)
        assert action.action_type == ActionType.RETREAT

    def test_engage_attacks_adjacent(self) -> None:
        fsm = AgentFSM()
        agent = AgentState(position=Position(x=5, y=5))
        world = WorldState(threats=[Position(x=5, y=6)])
        fsm.update(agent, world)
        action = fsm.select_action(agent, world)
        assert action.action_type == ActionType.ATTACK
