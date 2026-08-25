=======
History
=======

0.4.0 (2026-08-25)
------------------

* Resolve the default event loop explicitly: prefer the running loop, fall
  back to the thread's current loop, and raise a `RuntimeError` telling the
  caller to pass ``event_loop=`` when there is neither.  ``TimeMachine()``
  with no argument used to call `asyncio.get_event_loop()`, which raises on
  Python 3.14 and has warned since 3.12.
* Drop support for Python 3.6 through 3.9; support 3.10 through 3.14.
* Move packaging to ``pyproject.toml`` built by ``flit_core``, and CI from
  the long-defunct travis-ci.org to GitHub Actions.

0.3.0 (2021-09-14)
------------------

* Support use as a context manager, to restore the time method at exit.
* Use the main asyncio event loop by default.

0.2.0 (2021-09-14)
------------------

* Drop support for Python 3.4/3.5; add 3.7/3.8/3.9.
* Update the dev requirements.

0.1.0 (2017-07-24)
------------------

* First release on PyPI.
