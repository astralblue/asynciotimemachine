# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`asynciotimemachine` is a single-module PyPI package (`asynciotimemachine.py`, ~60 lines) that
monkey-patches an `asyncio` event loop's `time()` method so the loop believes it is further in the
future than it is. Everything else in the repo is packaging, docs, and CI scaffolding generated from
the `audreyr/cookiecutter-pypackage` template.

## Commands

The dev toolchain is managed by `uv`; `uv.lock` is committed and authoritative.

```sh
uv sync                 # create .venv from uv.lock (project + `dev` group)

uv run pytest           # tests on the default interpreter
uv run --python 3.14 pytest      # ...on any supported version; uv fetches it
uv run ruff check .     # lint
uv run ruff format .    # format (`--check` to verify only)
uv run coverage run -m pytest && uv run coverage report -m
uv run --group docs sphinx-build -b html docs docs/_build/html
uv run --group docs sphinx-autobuild docs docs/_build/html
uv build                # sdist + wheel via flit_core
uv lock                 # re-resolve after editing pyproject.toml; CI runs
                        # `uv lock --check` and fails on a stale lockfile
uv audit --frozen --preview-features audit-command   # known vulnerabilities
```

Vulnerability scanning is deliberately *not* part of the PR gate: it runs
weekly from `.github/workflows/audit.yml`, because every locked package is dev
tooling (zero runtime dependencies) and a fresh advisory should not redden an
unrelated pull request. GitHub's dependency graph does not currently parse
`uv.lock`, so Dependabot alerts cover the workflows' actions but not Python —
`uv audit` is what covers Python.

There is no Makefile and no tox: the version matrix lives in
`.github/workflows/test.yml`, and `uv run --python X.Y` covers it locally.

Single test / subset:

```sh
uv run pytest tests/test_asynciotimemachine.py::TestTimeMachine::test_advance_by
uv run pytest -k advance_to
```

Version bumps are driven by `bump-my-version` (`[tool.bumpversion]` in
`pyproject.toml`); it rewrites `__version__` in `asynciotimemachine.py`, then
commits and tags `vX.Y.Z`. Never edit that version string by hand — the
packaging metadata reads it via `dynamic = ["version"]`, `docs/conf.py` imports
it, and the tool's `search` pattern must keep matching it (note it is
double-quoted, which is what `ruff format` produces). Pushing the tag is what
triggers the release workflow.

## Architecture

`TimeMachine` keeps a `__delta` offset and installs a bound `__time` method onto the loop instance
that returns `original_time() + delta`. Because `loop.time()` is the authoritative clock for every
scheduling decision `asyncio` makes, advancing the delta causes already-scheduled `call_at`/`call_later`
callbacks to fire immediately rather than after a real-time wait.

Two consequences shape the whole design:

- **Patching happens in `__init__`, not in `__enter__`.** `__exit__` restores `loop.time`, so a
  `TimeMachine` constructed but never entered leaves the loop permanently patched. This is
  deliberate (backward compatibility — the context-manager protocol was added in 0.3.0) and is
  called out in `docs/usage.rst`; preserve it unless the version is intentionally breaking.
- **Time may only move forward.** Both `advance_by()` and `advance_to()` raise `ValueError` on
  negative/past targets, since retreating the clock would break monotonicity assumptions that
  `asyncio`'s timer heap relies on.

The constructor takes `*poargs`/`**kwargs` and forwards them to `super().__init__()` so the class
stays cooperative under multiple inheritance; keep that pass-through when adding parameters, and
keep `event_loop` keyword-only.

Tests use a function-scoped `event_loop` fixture that creates and closes a fresh loop, so they never
touch the ambient loop — except `test_with_default_loop`, which deliberately exercises the
`event_loop=None` default path by calling another test method directly.

## Conventions

- `ruff` is the lint gate, configured in `pyproject.toml` with `E`, `W`, `F`,
  `D`, `I`, `UP`, `B` selected and the `pep257` docstring convention: every
  public class and method needs a docstring, and Sphinx-style
  `:param:`/`:raise:` fields are the house style. Do not switch the pydocstyle
  convention to `google` or `numpy` — `D417` would then flag every one of
  those fields.
- `ruff format` owns formatting; 79-column lines, LF endings, no trailing
  whitespace (`.editorconfig`). `docs/` is excluded from both.
- Docs are reStructuredText; `docs/usage.rst` contains doctest-style examples
  that are the de facto spec for behavior — update them alongside API changes,
  and add an entry to `HISTORY.rst`. The Sphinx build is warning-free and
  `.readthedocs.yaml` sets `fail_on_warning: true`, so keep it that way.

## Packaging / CI state

Packaging is PEP 621 metadata in `pyproject.toml` built by `flit_core`, with
zero runtime dependencies and the version single-sourced from `__version__`.

`[tool.flit.sdist]` is load-bearing, not decorative: under a PEP 517 frontend
`flit_core` never consults version control, so the default sdist is only the
module, `pyproject.toml`, the readme and the license. Anything else that should
ship — `tests/`, `docs/`, the three top-level `.rst` files — has to be listed
there. Check `tar -tzf` after touching it.

Because `license = "MIT"` is a PEP 639 expression, a `License :: OSI Approved`
classifier must **not** be added back: `flit_core` errors out when both are
present.

CI is GitHub Actions on the **`master`** default branch (`.github/workflows/`),
and the only git remote is **`astralblue`** — there is no `origin`. The
supported-version list is duplicated in `requires-python`, the `Programming
Language :: Python` classifiers, the `test.yml` matrix, and
`CONTRIBUTING.rst`; a version-support change has to touch all four. Releases go
to PyPI through Trusted Publishing on a pushed `v*` tag — no stored credential.
