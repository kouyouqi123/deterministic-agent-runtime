"""Evaluation Harness — Seeded scenario execution and metrics.

Runs deterministic scenarios with seeded configurations and
collects metrics: success rate, recovery rate, constraint violations,
action counts, and decision trace quality.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.events.bus import EventBus, EventType
from core.constraints.engine import create_default_engine
from core.runtime.loop import RuntimeLoop
from adapters.simulation.grid import GridSimulation, SimulationConfig
from policies.fsm.agent_fsm import AgentFSM
from replay.trace_log import TraceLog

from pathlib import Path


@dataclass
class ScenarioResult:
    """Result of a single scenario run."""

    seed: int
    ticks: int
    threats_remaining: int
    agent_alive: bool
    agent_health: int
    decision_count: int
    constraint_violations: int
    success: bool  # All threats cleared and agent alive


@dataclass
class EvalMetrics:
    """Aggregate metrics across multiple scenario runs."""

    total_runs: int = 0
    successes: int = 0
    failures: int = 0
    total_decisions: int = 0
    total_violations: int = 0
    agent_deaths: int = 0
    results: list[ScenarioResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Fraction of successful runs."""
        return self.successes / self.total_runs if self.total_runs > 0 else 0.0

    @property
    def avg_decisions(self) -> float:
        """Average decisions per run."""
        return self.total_decisions / self.total_runs if self.total_runs > 0 else 0.0


def run_scenario(seed: int, max_ticks: int = 50) -> ScenarioResult:
    """Run a single seeded scenario and return metrics."""
    bus = EventBus()
    config = SimulationConfig(
        seed=seed, width=8, height=8,
        num_obstacles=4, num_threats=2,
    )
    sim = GridSimulation(config, bus)
    constraints = create_default_engine(bus)
    fsm = AgentFSM()
    runtime = RuntimeLoop(sim, constraints, fsm, bus, max_ticks=max_ticks)
    traces = runtime.run()

    violations = len(bus.get_history(event_type=EventType.CONSTRAINT_VIOLATED))

    return ScenarioResult(
        seed=seed,
        ticks=sim.world.tick,
        threats_remaining=len(sim.world.threats),
        agent_alive=sim.agent.alive,
        agent_health=sim.agent.health,
        decision_count=len(traces),
        constraint_violations=violations,
        success=len(sim.world.threats) == 0 and sim.agent.alive,
    )


def run_eval(seeds: list[int], max_ticks: int = 50) -> EvalMetrics:
    """Run evaluation harness across multiple seeds."""
    metrics = EvalMetrics()
    for seed in seeds:
        result = run_scenario(seed, max_ticks)
        metrics.total_runs += 1
        metrics.total_decisions += result.decision_count
        metrics.total_violations += result.constraint_violations
        if result.success:
            metrics.successes += 1
        else:
            metrics.failures += 1
        if not result.agent_alive:
            metrics.agent_deaths += 1
        metrics.results.append(result)
    return metrics
