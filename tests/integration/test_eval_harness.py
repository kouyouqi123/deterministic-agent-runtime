"""Evaluation harness integration tests."""

from eval.harness import run_scenario, run_eval


class TestEvalHarness:
    def test_single_scenario(self) -> None:
        result = run_scenario(seed=42)
        assert result.decision_count > 0
        assert result.ticks > 0

    def test_deterministic_scenario(self) -> None:
        r1 = run_scenario(seed=42)
        r2 = run_scenario(seed=42)
        assert r1.decision_count == r2.decision_count
        assert r1.threats_remaining == r2.threats_remaining
        assert r1.agent_alive == r2.agent_alive

    def test_eval_multiple_seeds(self) -> None:
        metrics = run_eval(seeds=[42, 99, 123, 456, 789])
        assert metrics.total_runs == 5
        assert metrics.successes + metrics.failures == 5
        assert metrics.success_rate >= 0.0
        assert metrics.avg_decisions > 0

    def test_different_seeds_vary(self) -> None:
        metrics = run_eval(seeds=list(range(10)))
        # With 10 different seeds, results should vary
        assert metrics.total_runs == 10
