# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

**Legacy-to-Lakehouse with an AI Ops Assistant** is a public portfolio project. It tells a migration story in two halves:

1. **Legacy (simulated):** a multi-tenant bank reporting platform. It has a PostgreSQL source written in Oracle-style patterns (PL/pgSQL load procedures, sequences, staging tables, `MERGE`/upsert loads, audit/control tables), and nightly fixed-width or delimited extract files that those procedures load.
2. **Modern:** the same platform rebuilt with Python ingestion, Airflow orchestration, dbt models with tests, and Databricks/Delta Lake (bronze → silver → gold).
3. **AI Ops Assistant:** a tool that reads failed-run logs (Airflow task logs, dbt test failures, load-procedure errors) and drafts a root-cause analysis for a human to review.

Multi-tenancy is a core theme. Every table, file, and model carries a tenant identifier (e.g. `tenant_id`), and tenant isolation has its own tests.

The repo is new. The layout below is the **intended** structure; build it up as you go and propose updates to this file whenever reality changes.

```
legacy/            # Postgres DDL, PL/pgSQL load procs, extract-file generators
  sql/
  extracts/        # generated sample files (small samples committed; bulk output gitignored)
ingestion/         # Python ingestion (files/DB -> bronze)
orchestration/     # Airflow DAGs, docker-compose for local Airflow
transform/         # dbt project (staging -> intermediate -> marts) + tests
lakehouse/         # Delta Lake / Databricks notebooks, jobs, configs
ai_ops/            # RCA assistant: log parsing, prompt, CLI
data_gen/          # synthetic data generators (single source of fake data)
docs/              # architecture notes, ADRs, migration write-up
```

## Hard rules

- **Synthetic data only.** All data comes from generators in this repo (e.g. Faker with a fixed seed). Never add real customer, account, or transaction data. Never add real company code, schemas, table names, or internal identifiers, even "anonymized." If something looks like it came from a real employer, stop and ask. Generic Oracle patterns are fine, but don't recreate schemas, table names, or logic remembered from a real employer.
- **No secrets in git.** Credentials go in `.env` (gitignored) with a committed `.env.example`. This includes Databricks tokens and the LLM API key.
- **Public-repo hygiene.** Assume everything committed is read by recruiters and strangers. Keep it clean, with no TODO dumps and no dead code.
- **AI assistant inputs are synthetic too.** Only synthetic logs go to the LLM, and the RCA output is always labeled as a draft for human review.

## How to work with me

I'm refreshing my skills and want to learn, not just receive code.

- **Explain your reasoning as you go.** Before a change, say what you're about to do and why. After it, point out the key idea, such as why a dbt incremental strategy fits, or what Airflow's `catchup` does. Keep explanations short and concrete.
- **Name the trade-offs** when there's a real choice, give a recommendation, and say what the alternative would teach or cost.
- **Small, reviewable steps.** Make one logical change at a time, sized so I can read the whole diff. Stop at natural checkpoints so I can review or try it myself before we continue.
- **Prefer my understanding over speed.** If I could reasonably write a piece myself, offer to let me try first or to scaffold it with the key part left for me.
- **Show me how to verify.** For each step, give the command to run and what correct output looks like.
- When I ask for a commit, suggest a clear, conventional commit message and the commands for me to run.

## Teaching rules

These rules override any looser guidance elsewhere in this file.

- **Small pieces.** Write one function or one file section at a time. Before writing, say what you'll write and why.
- **Explain-back gate.** After each piece, stop and ask me to explain it in my own words. Don't continue until I approve.
- **Who writes first.** If a piece is mostly SQL or PL/SQL, offer me the first attempt. If the tooling is new to me, write it yourself.
- **Map to what I know.** When it helps, relate new concepts to Oracle, PL/SQL, Zena, or star schemas.
- **I run git.** Don't run git commands. Tell me the command and what it does, and I'll type it.
- **No secrets in files.** Never write secrets or credentials into files. Use environment variables or placeholders.
- **Ask first.** Ask before installing anything or using anything that costs money.
- **Simple over clever.** Prefer simple, readable code, and explain any library choice.
- **Learning log.** After each build step, append quick-check Q&A to `LEARNING_LOG.md`. This file is private and gitignored, so never commit it. Record my answers verbatim, with corrections.
- **Edits to this file.** Propose changes to `CLAUDE.md` and wait for my approval before applying them.
- **Graded answer checks.** When checking my answers or predictions, start with "Correct:", "Partly correct:", or "Incorrect:", then give the right answer. Never mark a wrong answer as fine.
- **Session start check.** At the start of each session, ask me to run `! pwd` and `! git status`. If `pwd` is not the project root, or the branch is not the one we're working on, stop and tell me before doing anything else. If you don't know the expected branch, ask.

## Environment

- **Intel Mac (x86_64), Docker Desktop with the HyperKit VM backend.**
  - Images run natively as `linux/amd64`, so there's no ARM emulation to worry about.
  - Docker Desktop's VM has a fixed memory cap. Airflow's official compose stack wants about 4 GB, and 8 GB is better. Keep the local stack lean: use `LocalExecutor` rather than Celery+Redis, and run only the services the current step needs.
  - Bind-mounted file I/O is slow under HyperKit. Use named volumes for database data, and only bind-mount code (DAGs, dbt project).
  - Newer Docker Desktop releases have deprecated HyperKit in favor of Apple's Virtualization framework. If something Docker-related breaks oddly, check this first and mention it rather than guessing.
- **Databricks can't run locally.** For local development, use PySpark with `delta-spark` so the Delta logic stays testable offline. Use a free Databricks workspace (Free Edition) for the "real" deployment step. Keep code portable between the two (config-driven paths, no hard-coded workspace URLs).
- Python: pin versions (`pyproject.toml` or `requirements.txt`) and use a virtualenv. Pin Docker image tags; never use `latest`.

## Conventions

- **SQL:** lowercase keywords are fine; be consistent within a file. Legacy SQL should *look* legacy (Oracle-flavored procs, control tables, row-by-row-ish patterns) because that's the point. Comment where a pattern mimics Oracle (e.g. "emulates `MERGE` / `NVL` / autonomous-transaction logging").
- **dbt:** use `stg_` → `int_` → `fct_`/`dim_` naming. Every model gets at least `not_null`/`unique` on its key, and tenant-isolation tests where relevant.
- **Airflow:** DAGs should be idempotent and re-runnable for a given logical date. Keep no business logic in DAG files; DAGs call into `ingestion/` or dbt.
- **Failures are features.** Some steps should be able to fail on purpose (bad extract file, schema drift, failed dbt test, duplicate tenant keys), so the AI Ops Assistant has realistic logs to analyze. Keep these failure scenarios reproducible and documented.
- **Docs:** record significant decisions as short ADRs in `docs/adr/`.
