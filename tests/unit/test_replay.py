"""Replay and trace log tests."""

from pathlib import Path
import tempfile

from core.models.actions import Action, ActionType
from core.models.traces import DecisionTrace
from replay.trace_log import TraceLog


class TestTraceLog:
    def test_write_and_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "traces.jsonl"
            log = TraceLog(path)
            traces = [
                DecisionTrace(tick=1, selected_action=Action(action_type=ActionType.MOVE)),
                DecisionTrace(tick=2, selected_action=Action(action_type=ActionType.WAIT)),
            ]
            log.write(traces)
            loaded = log.read()
            assert len(loaded) == 2
            assert loaded[0].tick == 1
            assert loaded[1].selected_action.action_type == ActionType.WAIT

    def test_read_empty(self) -> None:
        log = TraceLog(Path("/nonexistent/traces.jsonl"))
        assert log.read() == []

    def test_compare_identical(self) -> None:
        log = TraceLog(Path("/dev/null"))
        traces = [DecisionTrace(tick=1, selected_action=Action(action_type=ActionType.MOVE))]
        assert log.compare(traces, traces) == []

    def test_compare_divergent(self) -> None:
        log = TraceLog(Path("/dev/null"))
        a = [DecisionTrace(tick=1, selected_action=Action(action_type=ActionType.MOVE))]
        b = [DecisionTrace(tick=1, selected_action=Action(action_type=ActionType.RETREAT))]
        divergences = log.compare(a, b)
        assert len(divergences) == 1
        assert divergences[0]["reason"] == "Action mismatch"
