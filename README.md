# calcstack

A deliberately over-engineered calculator, built to be a **Graphite stacked-PR
demo**. It is a real, working project — a Typer + Rich command-line calculator
and a FastAPI web app sharing one arithmetic engine — carved into a series of
small, dependent pull requests so you can see how stacking, restacking, and
stack-aware merging behave in practice.

> The narrated tour of the PRs and an evaluation of the review workflow live in
> [`docs/DEMO_GUIDE.md`](docs/DEMO_GUIDE.md).

## What it does

```bash
calcstack calc "2 + 3 * 4"     # -> 14
calcstack calc "2 ^ -2"        # -> 0.25
calcstack history show         # table of past calculations
```

Expressions support `+ - * / % ^`, parentheses, unary minus, operator
precedence and right-associative exponentiation. All arithmetic uses
`decimal.Decimal`, so results are exact.

## Toolchain

| Concern | Tool |
| --- | --- |
| Dependency + venv management | [uv](https://docs.astral.sh/uv/) |
| Build graph, tests, lint, typecheck, packaging | [Pants](https://www.pantsbuild.org/) |
| CLI | [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/) |
| Web API + UI | [FastAPI](https://fastapi.tiangolo.com/) |
| Models / validation | [pydantic](https://docs.pydantic.dev/) |
| Tests / lint / types | pytest, ruff, mypy |

uv and Pants share a single dependency source of truth: the root `BUILD` reads
requirements straight from `pyproject.toml`.

## Quickstart

```bash
# 1. Install deps into a uv-managed venv (Python 3.13 is pinned in .python-version)
uv sync --extra dev

# 2. Run the CLI
uv run calcstack calc "2 + 3 * 4"

# 3. Run the web app, then open http://127.0.0.1:8000
uv run uvicorn calcstack.api.app:app --reload

# 4. Tests / lint / types, either via uv...
uv run pytest
uv run ruff check .
uv run mypy

# ...or via Pants (build-graph aware, incremental, cached)
pants test ::
pants lint ::
pants check ::
pants package src/calcstack/cli:calcstack-bin   # builds a standalone PEX
```

## Layout

```
src/calcstack/
  engine/     # Decimal operations + the operator registry
  parser/     # tokenizer + shunting-yard evaluator
  history.py  # persistent JSON-backed calculation history
  cli/        # Typer + Rich command-line interface
  api/        # FastAPI app + static web UI
tests/        # pytest suites, one per module
docs/         # the Graphite demo tour and evaluation notes
```
