# Module 1: Terminal basics

**Time: 10 minutes**

## Why this module exists

Everything you will do in this workshop - and in a lot of modern sport-analytics work - happens at a **terminal**. It is the prompt you type commands into. It feels intimidating for about ten minutes and then it becomes the most efficient tool you own.

There is a second reason for starting here: **Claude Code lives in the terminal**. In this Codespace, Claude Code has already been installed for you by the setup script, so you do not need to install it yourself today. Later, if you want to install it on another machine, the official Claude Code setup command is in the docs: <https://code.claude.com/docs/en/getting-started>.

You start Claude Code by typing `claude`. Once it is running, it uses many of the same kinds of actions you are learning here: listing files, reading files, searching text, running scripts, and checking what changed. You are learning the basic moves so that when the agent does them under the hood, the transcript is not mysterious.

This module is the ten-minute vaccine.

## 1. Find your terminal

In your Codespace, look at the bottom of the VS Code window. You should see a panel labelled **TERMINAL**. If you cannot see it, press **Ctrl + `** (the backtick, top-left of your keyboard).

You should see a prompt that looks something like:

```
vscode ➜ /workspaces/msa-spe5spa-claude-workshop $
```

That is the shell. The `$` is where your typing appears.

## 2. Where am I?

Type:

```
pwd
```

`pwd` = **print working directory**. The terminal always has a "current location" in the filesystem. Every command you type runs from that location. Think of it as which folder a file explorer has open.

You should see `/workspaces/msa-spe5spa-claude-workshop`.

## 3. What is in this folder?

```
ls
```

`ls` = **list**. You will see the module folders, the `data/` folder, and the README. Want more detail?

```
ls -la
```

The `-la` adds "long format" and "all files including hidden ones". You will now see `.devcontainer`, `.gitignore`, `CLAUDE.md`. Files starting with `.` are hidden by default.

## 4. Move around

```
cd data
ls
```

`cd` = **change directory**. You are now in `data/`, and `ls` shows the CSV files. To go back up one level:

```
cd ..
```

Two dots means "parent". One dot means "here". To jump back to the repo root from anywhere:

```
cd /workspaces/msa-spe5spa-claude-workshop
```

## 5. Peek at a file

```
head data/squad_roster.csv
```

`head` shows the first ten lines of a file. Add `-20` to see twenty:

```
head -20 data/gps_training_messy.csv
```

## 6. Count things

```
wc -l data/gps_training_messy.csv
```

`wc` = **word count**. With `-l`, it counts lines instead of words. For a CSV, this gives you a quick sense of file size before you analyse it properly.

This matters because analysts often receive files before they know whether the export is complete. A line count will not tell you whether the data is clean, but it can quickly reveal that a file is empty, tiny, or much larger than expected.

## 7. Search

```
grep "NF015" data/gps_training_messy.csv
```

`grep` searches for text inside a file and prints every matching line.

Here we are searching for player ID `NF015`. In a small file, you could scroll manually. In a real export with thousands of rows, `grep` is faster and less error-prone.

Claude Code often uses the same idea through its search tools. When it needs to find a function, a player ID, a file path, or a phrase, it will search rather than read every file line by line.

## 8. Git - your safety net

This repo is a Git repository. Git tracks every change you make, and lets you undo anything. You do not need to become a Git expert today, but you should know one command:

```
git status
```

This tells you what files have changed since the last committed version.

You do not need `git status` because this is a Git class. You need it because coding agents can edit files quickly. Before and after you ask Claude Code to change anything, `git status` tells you what changed. That makes your work reviewable and recoverable.

If you ever break something and want to start fresh, Claude Code can help you recover using `git restore`, but you should first know what Git thinks has changed.

## Cheat sheet

| Command | What it does |
|---------|--------------|
| `pwd` | Where am I? |
| `ls` / `ls -la` | List files (hidden too) |
| `cd folder` | Move into a folder |
| `cd ..` | Move up one folder |
| `head file` | First ten lines |
| `cat file` | Whole file |
| `wc -l file` | Count lines |
| `grep "text" file` | Search for text |
| `git status` | What have I changed? |
| `clear` | Wipe the terminal screen |

## What Claude Code Does With These Skills

When Claude Code works as an agent, it does not magically "see" the whole project at once. It uses tools.

For example, it may:

- use a list command to see which files exist
- read a `README.md` to understand the task
- search files for a column name or player ID
- run a Python script
- check `git status` to see what changed

That is why we start with the terminal. You are learning the moves that the agent will later perform faster and more fluently.

## Done

You can move around, peek at files, and search. That is enough.

```
cd /workspaces/msa-spe5spa-claude-workshop/module-2-first-chat
cat README.md
```

Or just open `module-2-first-chat/README.md` in the editor sidebar.
