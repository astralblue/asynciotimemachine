=====
Usage
=====

Use `~asynciotimemachine.TimeMachine` as a context manager.  Its
`~asynciotimemachine.TimeMachine.advance_by()` and
`~asynciotimemachine.TimeMachine.advance_to()` methods fast-forward the
event loop's time reference by the specified number of seconds and to the
specified timestamp respectively::

    >>> import asyncio
    >>> import math
    >>> from asynciotimemachine import TimeMachine
    >>> event_loop = asyncio.new_event_loop()
    >>> asyncio.set_event_loop(event_loop)
    >>> original_time = event_loop.time
    >>> with TimeMachine() as tm:
    ...     tm.advance_by(10.0)
    ...     assert math.isclose(event_loop.time() - original_time(), 10.0,
    ...                         abs_tol=0.001)
    ...     tm.advance_to(original_time() + 20.0)
    ...     assert math.isclose(event_loop.time() - original_time(), 20.0,
    ...                         abs_tol=0.001)
    >>> asyncio.set_event_loop(None)
    >>> event_loop.close()

Without an explicit *event_loop* argument, `~asynciotimemachine.TimeMachine`
uses the running event loop if there is one, and otherwise the current event
loop of the calling thread—the one most recently passed to
:py:func:`asyncio.set_event_loop`.  If there is neither, it raises
:py:exc:`RuntimeError`; note that :py:func:`asyncio.get_event_loop` no longer
creates an event loop on demand as of Python 3.14.

Since the :py:meth:`asyncio.BaseEventLoop.time` method is the authoritative
timestamp source for all operations of the loop, fast-forwarding the timestamp
at the right place can eliminate the real-time delay.  For example, the
`hello_world()` function in the following example runs immediately, despite
being scheduled 30 seconds from now::

    >>> def hello_world():
    ...     print("Hello world")
    ...     asyncio.get_running_loop().stop()
    >>> event_loop = asyncio.new_event_loop()
    >>> with TimeMachine(event_loop=event_loop) as tm:
    ...     now = event_loop.time()
    ...     timer_handle = event_loop.call_at(now + 30, hello_world)
    ...     tm.advance_by(30)
    ...     event_loop.run_forever()
    Hello world

The example above also illustrates the ability to use a custom event loop with
the `~asynciotimemachine.TimeMachine`.

Note: For historic reason, the time method is patched at the initialization
time, not when the context manager is entered.
