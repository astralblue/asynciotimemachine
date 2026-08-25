.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/astralblue/asynciotimemachine/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

asyncio Time Machine could always use more documentation, whether as part of the
official asyncio Time Machine docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/astralblue/asynciotimemachine/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `asynciotimemachine` for local development.

1. Fork the `asynciotimemachine` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/asynciotimemachine.git

3. Install `uv <https://docs.astral.sh/uv/>`_ if you don't have it, then create
   the development environment from the committed lockfile::

    $ cd asynciotimemachine/
    $ uv sync

   This creates ``.venv/`` with ``asynciotimemachine`` installed in editable
   mode alongside the ``dev`` dependency group.  You do not need to activate
   it: prefix commands with ``uv run``.

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the linter and
   the tests::

    $ uv run ruff check .
    $ uv run ruff format --check .
    $ uv run pytest

   ``uv run ruff check --fix .`` and ``uv run ruff format .`` apply what those
   first two report.

   To run the tests against another supported interpreter, name it: ``uv``
   downloads one on demand, so this works on a machine with a single Python
   installed::

    $ uv run --python 3.14 pytest

   If you changed ``[project]`` or ``[dependency-groups]`` in
   ``pyproject.toml``, regenerate the lockfile and commit it with your
   change; CI runs ``uv lock --check`` and fails on a stale one::

    $ uv lock

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.10, 3.11, 3.12, 3.13, and 3.14.
   Check
   https://github.com/astralblue/asynciotimemachine/actions/workflows/test.yml
   and make sure that the checks pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ uv run pytest tests/test_asynciotimemachine.py::TestTimeMachine::test_advance_by
    $ uv run pytest -k advance_to

Other common tasks::

    $ uv run coverage run -m pytest && uv run coverage report -m
    $ uv run --group docs sphinx-build -b html docs docs/_build/html
    $ uv run --group docs sphinx-autobuild docs docs/_build/html
    $ uv build

Deploying
---------

A reminder for the maintainers on how to deploy.  Make sure all your changes
are committed, including an entry in ``HISTORY.rst``.  Then::

    $ uv run bump-my-version bump minor   # or patch / major
    $ git push --follow-tags

``bump-my-version`` rewrites ``__version__`` in ``asynciotimemachine.py``,
commits, and creates a ``vX.Y.Z`` tag.  Pushing that tag triggers
``.github/workflows/release.yml``, which re-runs the test matrix, builds the
sdist and wheel with ``uv build``, and uploads them to PyPI using Trusted
Publishing -- there is no PyPI credential stored in this repository.

