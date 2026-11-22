# Python project setup

The Python package is managed with [uv](https://docs.astral.sh/uv/).

## What is committed

| Path | Git | Why |
|---|---|---|
| `pyproject.toml` | commit | Declares the project: metadata, Python range, dependencies |
| `uv.lock` | commit | Exact resolved versions, so every machine installs the same set |
| `.python-version` | commit | Interpreter used for local development (3.12) |
| `src/legacy_to_lakehouse/` | commit | Package source |
| `.venv/` | ignore | Derived; rebuilt from the files above by `uv sync` |

## Commands

| Command | Purpose |
|---|---|
| `uv init --package --python 3.12 --no-readme` | Scaffold the project (run once) |
| `uv sync` | Create or update `.venv` to match `uv.lock` |
| `uv run <cmd>` | Run a command in the project environment, syncing first |
| `uv add <pkg>` | Add a dependency and update `uv.lock` |
| `uv lock` | Re-resolve `uv.lock` without installing |

## Why a src layout

Code under `src/` is importable only once installed, so tests and DAGs run against the installed package, not stray files in the working folder. See [ADR 0001](adr/0001-python-package-layout.md).

## Why Python 3.12

Supported across the stack (Airflow, dbt, PySpark with delta-spark) and by recent Databricks runtimes. Newer versions often lag in library support.
