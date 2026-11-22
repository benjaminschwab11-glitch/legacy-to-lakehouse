# ADR 0001: One Python package in a src layout

- **Status:** Accepted
- **Date:** 2026-11-21

## Context

The project has three Python components (ingestion, the AI Ops Assistant, and
synthetic data generators) alongside non-Python assets (SQL, dbt, Airflow DAGs,
Databricks notebooks). The original plan put each Python component in its own
top-level folder. `uv init --package` instead created a single package at
`src/legacy_to_lakehouse/`.

## Decision

All Python code lives in one installable package, `legacy_to_lakehouse`, under
`src/`. Each component is a subpackage (`ingestion`, `ai_ops`, `data_gen`) and is
imported as `legacy_to_lakehouse.<subpackage>`. Non-Python assets stay in
top-level folders.

## Consequences

- Python can only import the package after it is installed (`uv sync`), so tests
  and DAGs run against the installed code, not whatever is in the working folder.
- One `pyproject.toml` and one build target; no multi-package build config.
- Package-qualified names avoid collisions with third-party packages (a bare
  `ingestion` module could clash).
- Import paths are longer.
- Components share one dependency set. If one later needs isolated dependencies,
  it can be split out as a uv workspace member.
