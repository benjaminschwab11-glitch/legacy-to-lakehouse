# Git mental model

Git is a small database of snapshots plus a few text files that point into it.

## Commit = snapshot + parent + metadata

`git cat-file -p HEAD` shows that a commit is a short text object:

```
tree 8833afb...        # root directory snapshot (full state, not a diff)
parent 74903ae...      # previous commit; first commit has none, merges have two
author Name <email> 1793676982 -0800
committer Name <email> 1793676982 -0800

L1.1: add terminal cheatsheet and learning log entry
```

- **tree** lists blobs (file contents) and sub-trees (directories). Filenames live in the tree.
- **author** wrote the change; **committer** last created this commit object. They differ after `commit --amend`, `rebase`, or `cherry-pick`.
- Unchanged files reuse the same blob, so a full snapshot per commit stays cheap.

## Hash = fingerprint

A hash is the SHA-1 of the object's contents. Change one byte (message, timestamp, parent, tree) and the hash changes. Because `parent` is inside the commit, each hash also locks in all history before it. Rewriting a commit always creates a new hash. Short hashes (default 7 chars) work while unique in the repo.

## Branch = a file with one hash; HEAD = where you are

```
.git/HEAD             ->  ref: refs/heads/main
.git/refs/heads/main  ->  ec00613805a5d94ea2ed574eb6e5d530ac97688c
```

- Creating a branch writes one ~41-byte file. No project files are copied.
- `HEAD` is a symbolic ref: it names a branch, and committing moves that branch.
- Detached HEAD: `.git/HEAD` holds a raw hash instead of a branch name.

## Three areas

| Area | What it holds | Oracle analogy |
|---|---|---|
| Working directory | Files as you edit them | Uncommitted edits in your SQL*Plus session |
| Staging area (index) | What the next commit will contain | Pending DML before `COMMIT` |
| Repository (`.git`) | Permanent commits, trees, blobs | Committed rows in an append-only audit table |

## Cheat sheet

| Command | What it shows or does |
|---|---|
| `git log --oneline --graph --all --decorate` | History of all branches, with branch labels |
| `git log --format='%h %an <%ae> \| committer: %cn <%ce>'` | Author vs committer per commit |
| `cat .git/HEAD` | Which branch you are on |
| `cat .git/refs/heads/main` | The commit a branch points to |
| `git cat-file -p <hash>` | Pretty-print any object (commit, tree, blob) |
| `git branch <name>` / `git branch -d <name>` | Create / safely delete a branch pointer |
| `git switch <name>` | Move HEAD and update files to that commit's tree |
| `git rev-parse --short HEAD~1` | Resolve any name or expression to a hash |
| `git status -sb` | Short status plus branch and remote tracking |
