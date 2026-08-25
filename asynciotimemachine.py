"""Main module."""

import asyncio

__author__ = "Eugene M. Kim"
__email__ = "astralblue@gmail.com"
__version__ = "0.4.0"


class TimeMachine:
    """A monkey-patch helper to advance an event loop's time.

    :param event_loop: the event loop to monkey-patch; if omitted or `None`,
        the running event loop is used, falling back to the current event
        loop of this thread.
    :raise `RuntimeError`: if *event_loop* is omitted or `None` and there is
        neither a running nor a current event loop.
    """

    def __init__(
        self,
        *poargs,
        event_loop: asyncio.AbstractEventLoop | None = None,
        **kwargs,
    ):
        """Initialize this instance."""
        super().__init__(*poargs, **kwargs)
        if event_loop is None:
            try:
                event_loop = asyncio.get_running_loop()
            except RuntimeError:
                try:
                    event_loop = asyncio.get_event_loop()
                except RuntimeError:
                    raise RuntimeError(
                        "no running or current event loop; "
                        "pass event_loop= explicitly"
                    ) from None
        self.__loop = event_loop
        self.__original_time = event_loop.time
        self.__delta = 0
        self.__loop.time = self.__time

    def __enter__(self):
        """Return this instance; the loop is already patched."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore the event loop's original time method."""
        self.__loop.time = self.__original_time

    def __time(self):
        return self.__original_time() + self.__delta

    def advance_by(self, amount: float):
        """Advance the time reference by the given amount.

        :param amount: number of seconds to advance.
        :raise `ValueError`: if *amount* is negative.
        """
        if amount < 0:
            raise ValueError(
                f"cannot retreat time reference: amount {amount} < 0"
            )
        self.__delta += amount

    def advance_to(self, timestamp: float):
        """Advance the time reference so that now is the given timestamp.

        :param timestamp: the new current timestamp.
        :raise `ValueError`: if *timestamp* is in the past.
        """
        now = self.__original_time()
        if timestamp < now:
            raise ValueError(
                f"cannot retreat time reference: target {timestamp} < "
                f"now {now}"
            )
        self.__delta = timestamp - now
