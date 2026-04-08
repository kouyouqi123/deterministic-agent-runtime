"""Grid simulation tests."""

from core.events.bus import EventBus
from core.models.actions import Action, ActionType
from core.models.state import Position
from adapters.simulation.grid import GridSimulation, SimulationConfig


class TestGridSimulation:
    def test_deterministic_generation(self) -> None:
        bus = EventBus()
        sim1 = GridSimulation(SimulationConfig(seed=42), bus)
        sim2 = GridSimulation(SimulationConfig(seed=42), bus)
        assert sim1.world.obstacles == sim2.world.obstacles
        assert sim1.world.threats == sim2.world.threats

    def test_tick_advances(self) -> None:
        bus = EventBus()
        sim = GridSimulation(SimulationConfig(seed=1), bus)
        assert sim.world.tick == 0
        sim.tick()
        assert sim.world.tick == 1

    def test_move_changes_position(self) -> None:
        bus = EventBus()
        sim = GridSimulation(SimulationConfig(seed=1, num_obstacles=0), bus)
        result = sim.execute_action(
            Action(action_type=ActionType.MOVE, target=Position(x=1, y=0))
        )
        assert result.success is True
        assert sim.agent.position == Position(x=1, y=0)

    def test_wait_recovers_energy(self) -> None:
        bus = EventBus()
        config = SimulationConfig(seed=1, num_obstacles=0, num_threats=0)
        sim = GridSimulation(config, bus)
        # Drain some energy first
        sim.execute_action(
            Action(action_type=ActionType.MOVE, target=Position(x=1, y=0))
        )
        energy_after_move = sim.agent.energy
        sim.execute_action(Action(action_type=ActionType.WAIT))
        assert sim.agent.energy > energy_after_move

    def test_attack_removes_threat(self) -> None:
        bus = EventBus()
        config = SimulationConfig(seed=1, num_obstacles=0, num_threats=1)
        sim = GridSimulation(config, bus)
        threat = sim.world.threats[0]
        result = sim.execute_action(
            Action(action_type=ActionType.ATTACK, target=threat)
        )
        assert result.success is True
        assert threat not in sim.world.threats
