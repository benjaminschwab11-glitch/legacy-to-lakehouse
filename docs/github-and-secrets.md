# GitHub, remotes, and secrets

## Remotes and `origin`
A remote is a named URL for another copy of the repo. `origin` is the conventional
name for the main one. Adding it moves no data, like creating a database link.

    git remote add origin git@github.com:<user>/<repo>.git
    git remote -v

## push vs fetch vs pull
| Command | Does |
|---|---|
| `git push` | Sends local commits the remote doesn't have |
| `git fetch` | Downloads remote commits and updates `origin/*`; doesn't touch your branches |
| `git pull` | `fetch` and then merge (or rebase) into the current branch |

## `origin/main`
A local, read-only snapshot of where `main` was on `origin` at the last
push, fetch, or pull. It isn't live. `git push -u origin main` makes local `main` track it,
so `git branch -vv` can report `ahead N` / `behind N`, and a plain `git push` / `git pull` works.

## Auth (SSH)
- `ssh-keygen -t ed25519` creates `id_ed25519` (private, never leaves this machine)
  and `id_ed25519.pub` (public, pasted into GitHub settings).
- GitHub sends a challenge that only the private key can answer. No secret crosses the network.
- `known_hosts` stores GitHub's host key, so later impersonation is detected.
- Test with `ssh -T git@github.com`.

## A pushed secret is a compromised secret
Bots scrape public repos within minutes, and forks or caches may keep copies. Deleting
the secret in a new commit leaves it in history. **Rotate it** (revoke it and issue a new one),
then clean up.

## Tracked a file by mistake?
`.gitignore` only affects untracked files. To stop tracking one, keeping it on disk:

    echo ".env" >> .gitignore
    git rm --cached .env
    git commit -m "chore: stop tracking .env"

If it was already pushed, rotate whatever it contained.

## Pre-push checklist
    git status                                         # clean
    git ls-files                                       # only intended files
    git grep -n -I -i -E 'api[_-]?key|secret|token|passw(or)?d|private key|sk-ant-|dapi[0-9a-f]{32}|ghp_|AKIA'
    git log --format='%h author=%ae committer=%ce'     # noreply only
    git log --all -- LEARNING_LOG.md                   # empty
    git check-ignore -v .env LEARNING_LOG.md           # both ignored

Also turn on GitHub's "Block command line pushes that expose my email" setting.
