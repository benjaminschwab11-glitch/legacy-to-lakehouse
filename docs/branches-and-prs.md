# Branches and pull requests

A branch is a cheap, isolated line of work. A pull request is how that work gets reviewed and promoted to `main`.

## Why branch

`main` is PROD: it should always work. A branch is a DEV schema cloned from PROD, except the clone is one ~41-byte pointer file, so it's instant. Experiment freely; `main` doesn't change until a reviewed merge.

## The feature-branch loop

```
git switch main && git pull           # 1. start from current main
git switch -c docs/topic              # 2. create the branch and move HEAD to it
# edit files                          # 3. make one logical change
git add <files> && git commit         # 4. commit (repeat 3-4 as needed)
git push -u origin docs/topic         # 5. publish; -u links it to origin/docs/topic
# open, review, and merge the PR      # 6. on GitHub
git switch main && git pull           # 7. sync main, then clean up (below)
```

## What a PR is

A pull request is a GitHub feature, not a Git one. Git only knows commits and branches. A PR is a delivery ticket with the diff attached: title, description, review comments, and a Merge button. The merge happens on GitHub, so your laptop doesn't see it until you fetch.

## Three ways to merge

| Option | Result on `main` |
|---|---|
| Fast-forward | `main` slides forward to the branch tip; no new commit |
| Merge commit | New commit with two parents; branch commits kept as they are |
| Squash | All branch commits combined into one new single-parent commit |

## origin/main is a cached copy

`origin/main` is your local, read-only copy of GitHub's `main` as of your last fetch. Think of it as a materialized view of a remote table: fast to query, silently stale.

- `git fetch` refreshes it (like `DBMS_MVIEW.REFRESH`). Your own `main` does not move.
- `git pull` is `git fetch` plus merging `origin/main` into your current branch.
- "Your branch is up to date with 'origin/main'" compares against the cached copy, not live GitHub.

## Cleanup

- `git branch -d <name>` deletes a local branch, but refuses if it holds unmerged commits. `-D` forces it.
- `git fetch --prune` removes `origin/<name>` refs for branches deleted on GitHub.
- `git branch -a` lists local and remote-tracking branches to confirm.

## Zena mapping

| Zena | Git / GitHub |
|---|---|
| Authoring change | Commits on a feature branch |
| Promotion request | Pull request |
| Promotion | Merging the PR into `main` |
