# Claude Code working habits

How I work with Claude Code in this repo: habits that keep an AI assistant fast without letting it be wrong quietly.

## The habits

| Habit | Why | Oracle / Zena analogy |
|---|---|---|
| Launch `claude` from the project root; confirm with `pwd` | `CLAUDE.md`, relative paths, and git all resolve from where you start | Connect to the right schema before running DDL |
| `CLAUDE.md` is read at session start | Edits to it apply after a restart or `/clear`, not mid-session | `login.sql` runs once when SQL*Plus connects |
| Plan mode (Shift+Tab) before multi-file edits | Review the approach while changing it is still free | `explain plan` before executing the statement |
| Read every permission prompt; approve small diffs | You can only approve what you actually read | Review the change ticket before the DBA runs it |
| Verify claims with real tools | "Done" or "Correct" from the assistant is a claim, not a result | Query `user_errors` instead of trusting "procedure compiled" |
| `/clear` between unrelated tasks | Stale context leads to confident wrong answers | Start a fresh session instead of reusing dirty package state |
| `Esc`, `!cmd`, `@file` | Interrupt; run a shell command in-session; attach a file | Cancel a query; `host` in SQL*Plus; `@script.sql` |
| Never paste secrets into the prompt | Prompts leave your machine; use `.env` and placeholders | Use a wallet, never a password in a Zena job definition |

## Started in the wrong directory

If `pwd` shows a subfolder (or `.git/`), Claude Code misses `CLAUDE.md` and runs git and file paths against the wrong root. Don't work around it. Exit, `cd` to the project root, and relaunch.

## Trust, then verify

After any claim about state, check it yourself:

```
git status                    # what changed?
git ls-files | grep <name>    # is it really tracked or untracked?
ls <file>                     # is it really on disk?
```
