=====
Usage
=====

To use asyncio Time Machine in a project::

    >>> from asynciotimemachine import TimeMachine
    >>> from asyncio import get_event_loop
    >>> event_loop = get_event_loop()
    >>> original_time = event_loop.time
    >>> tm = TimeMachine(event_loop=event_loop)

The `~asynciotimemachine.TimeMachine.advance_by()` method fast-forwards the
event loop's time reference by the specified number of seconds::

    >>> from math import isclose
    >>> tm.advance_by(10)
    >>> isclose(event_loop.time() - original_time(), 10.0, abs_tol=0.001)
    True

The `~asynciotimemachine.TimeMachine.advance_to()` method fast-forwards the
event loop's time reference to the specified timestamp::

    >>> tm.advance_to(original_time() + 20)
    >>> isclose(event_loop.time() - original_time(), 20.0, abs_tol=0.001)
    True

Since the :py:meth:`asyncio.BaseEventLoop.time` method is the authoritative
timestamp source for all operations of the loop, fast-forwarding the timestamp
at the right place can eliminate the real-time delay.  For example, the
`hello_world()` function in the following example runs immediately, despite
being scheduled 30 seconds from now::

    >>> def hello_world():
    ...     print("Hello world")
    ...     event_loop.stop()
    >>> now = event_loop.time()
    >>> timer_handle = event_loop.call_at(now + 30, hello_world)
    >>> tm.advance_by(30)
    >>> event_loop.run_forever()
    Hello world
