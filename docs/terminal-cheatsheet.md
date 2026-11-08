# Terminal Cheatsheet

Quick reference for the shell commands used throughout this project (macOS, zsh).

## Where am I / what's here

| Command | What it does | Oracle / Unix-ops analogy |
|---|---|---|
| `pwd` | Print the current (working) directory as an absolute path. | Like `show user` — "who/where am I" before doing anything risky. |
| `ls -la` | List all files, including hidden dotfiles (`-a`), with permissions, owner, size, date (`-l`). | Like querying `all_objects` instead of `user_objects` — you see what's normally hidden. |
| `cd <dir>` | Change directory. `cd ..` = up one, `cd ~` = home, `cd -` = previous dir. | Like `alter session set current_schema` — changes context for everything after. |
| `mkdir -p a/b/c` | Create a directory and any missing parents; no error if it already exists. | Idempotent, like `create table if not exists` (or a guarded `execute immediate`). |

## Reading files

| Command | What it does | Oracle / Unix-ops analogy |
|---|---|---|
| `cat file` | Print a whole file to the screen. Best for short files. | |
| `less file` | Page through a file; `/text` to search, `q` to quit. | |
| `head -n 20 file` | Show the first 20 lines (default 10). | Like `fetch first 20 rows only`. |
| `tail -f file` | Show the end of a file and keep following new lines as they're written. | Classic `tail -f alert.log` while a load proc runs. |

## Moving things around

| Command | What it does | Oracle / Unix-ops analogy |
|---|---|---|
| `cp src dest` | Copy a file (`cp -r` for directories). | Like `create table x as select * from y`. |
| `mv src dest` | Move or rename. Overwrites `dest` silently if it exists. | Like `rename` / `alter table ... rename to`. |
| `rm file` | Delete a file (`rm -r` for directories). No trash, no undo. | `drop table ... purge` — no recycle bin, no flashback. |

## Searching and combining

| Command | What it does | Oracle / Unix-ops analogy |
|---|---|---|
| `grep "text" file` | Print lines matching a pattern. `-i` ignore case, `-r` recurse, `-n` line numbers. | `where line like '%text%'`. Great for `grep ORA- load.log`. |
| `cmd1 \| cmd2` | Pipe: send cmd1's output as cmd2's input. | Like an inline view — each stage feeds the next. |
| `cmd > file` | Redirect output to a file, **overwriting** it. | `spool file replace`. |
| `cmd >> file` | Redirect output to a file, **appending** to it. | `spool file append` — how log files grow. |

## Environment

| Command | What it does | Oracle / Unix-ops analogy |
|---|---|---|
| `which python3` | Show the full path of the program that will actually run. | Like checking which `$ORACLE_HOME` your `sqlplus` comes from. |
| `echo $PATH` | The ordered, colon-separated list of directories the shell searches for commands. First match wins. | Like `$ORACLE_HOME/bin` order deciding which client you get. |

## Keyboard

| Key | What it does |
|---|---|
| `Tab` | Autocomplete file/command names; press twice to list options. Saves typos. |
| `Ctrl-C` | Interrupt (kill) the running command. |
| `Ctrl-R` | Reverse-search your command history; keep pressing to cycle back. |
