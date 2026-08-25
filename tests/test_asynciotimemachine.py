"""Tests for `asynciotimemachine` package."""

import asyncio

import pytest

from asynciotimemachine import TimeMachine


class TestTimeMachine:
    """Tests for `TimeMachine`."""

    @pytest.fixture
    def event_loop(self):
        """Return a fresh event loop, closed after the test."""
        loop = asyncio.new_event_loop()
        try:
            yield loop
        finally:
            loop.close()

    @pytest.fixture
    def current_event_loop(self, event_loop):
        """Return an event loop installed as this thread's current one."""
        asyncio.set_event_loop(event_loop)
        try:
            yield event_loop
        finally:
            asyncio.set_event_loop(None)

    @pytest.fixture
    def no_event_loop(self):
        """Ensure this thread has no current event loop."""
        asyncio.set_event_loop(None)
        yield

    @pytest.fixture
    def time_machine(self, event_loop):
        """Return the time machine fixture."""
        return TimeMachine(event_loop=event_loop)

    @pytest.mark.parametrize("amount", [0, 0.1, 1, 60, 3600, 86400])
    def test_advance_by(self, time_machine, event_loop, amount):
        """Test `TimeMachine.advance_by()` fast-forwards timestamp."""
        time1 = event_loop.time()
        time_machine.advance_by(amount)
        time2 = event_loop.time()
        assert time2 - time1 == pytest.approx(amount, abs=0.01)

    @pytest.mark.parametrize("amount", [0.1, 1, 60, 3600, 86400])
    def test_advance_to(self, time_machine, event_loop, amount):
        """Test `TimeMachine.advance_to()` fast-forwards timestamp."""
        time1 = event_loop.time()
        time_machine.advance_to(time1 + amount)
        time2 = event_loop.time()
        assert time2 - time1 == pytest.approx(amount, abs=0.01)

    @pytest.mark.parametrize("amount", [-0.1, -1, -60, -3600, -86400])
    def test_advance_by_backward(self, time_machine, amount):
        """Test ``advance_by()`` raises `ValueError` for backward amount."""
        with pytest.raises(ValueError):
            time_machine.advance_by(amount)

    @pytest.mark.parametrize("amount", [-0.1, -1, -60, -3600, -86400])
    def test_advance_to_past(self, time_machine, event_loop, amount):
        """Test ``advance_to()`` raises `ValueError` for travel into past."""
        with pytest.raises(ValueError):
            time_machine.advance_to(event_loop.time() + amount)

    def test_as_context_manager(self, event_loop):
        """Test the time method is restored upon context exit."""
        original_time = event_loop.time
        with TimeMachine(event_loop=event_loop) as tm:
            assert event_loop.time != original_time
            assert event_loop.time == tm._TimeMachine__time
        assert event_loop.time == original_time

    def test_with_default_loop(self, current_event_loop):
        """Test the current event loop is used by default."""
        original_time = current_event_loop.time
        with TimeMachine() as tm:
            assert current_event_loop.time != original_time
            assert current_event_loop.time == tm._TimeMachine__time
        assert current_event_loop.time == original_time

    def test_with_running_loop(self, no_event_loop):
        """Test the running event loop is preferred by default."""

        async def main():
            loop = asyncio.get_running_loop()
            original_time = loop.time
            with TimeMachine() as tm:
                assert loop.time != original_time
                assert loop.time == tm._TimeMachine__time
            assert loop.time == original_time

        asyncio.run(main())

    def test_without_any_loop(self, no_event_loop):
        """Test `RuntimeError` is raised without a running/current loop."""
        with pytest.raises(RuntimeError, match=r"pass event_loop="):
            TimeMachine()
