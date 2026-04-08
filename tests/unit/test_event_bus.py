"""Event bus tests."""

from core.events.bus import EventBus, Event, EventType


class TestEventBus:
    def test_emit_and_subscribe(self) -> None:
        bus = EventBus()
        received: list[Event] = []
        bus.subscribe(EventType.TICK, lambda e: received.append(e))
        bus.emit(Event(event_type=EventType.TICK, tick=1))
        assert len(received) == 1
        assert received[0].tick == 1

    def test_subscribe_all(self) -> None:
        bus = EventBus()
        received: list[Event] = []
        bus.subscribe_all(lambda e: received.append(e))
        bus.emit(Event(event_type=EventType.TICK, tick=1))
        bus.emit(Event(event_type=EventType.AGENT_MOVED, tick=2))
        assert len(received) == 2

    def test_history(self) -> None:
        bus = EventBus()
        bus.emit(Event(event_type=EventType.TICK, tick=1))
        bus.emit(Event(event_type=EventType.TICK, tick=2))
        bus.emit(Event(event_type=EventType.AGENT_MOVED, tick=3))
        assert bus.history_size == 3
        ticks = bus.get_history(event_type=EventType.TICK)
        assert len(ticks) == 2

    def test_history_since_tick(self) -> None:
        bus = EventBus()
        bus.emit(Event(event_type=EventType.TICK, tick=1))
        bus.emit(Event(event_type=EventType.TICK, tick=5))
        bus.emit(Event(event_type=EventType.TICK, tick=10))
        recent = bus.get_history(since_tick=5)
        assert len(recent) == 2

    def test_bounded_history(self) -> None:
        bus = EventBus(max_history=5)
        for i in range(10):
            bus.emit(Event(event_type=EventType.TICK, tick=i))
        assert bus.history_size == 5
        assert bus.get_history()[0].tick == 5

    def test_no_subscribers(self) -> None:
        bus = EventBus()
        bus.emit(Event(event_type=EventType.TICK, tick=1))
        assert bus.history_size == 1
