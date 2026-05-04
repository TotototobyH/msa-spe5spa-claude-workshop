# Module 3: CLAUDE.md and giving context

**Time: 10 minutes**

## Why this module exists

Claude Code is only as useful as the context it has. The model has no idea that Northfield FC uses metres (not yards), that Pat is the sport scientist, that `NF###` is your player ID scheme, or that the coach hates emoji in reports. If you have to explain these conventions at the start of every conversation, you lose half your time to re-briefing.

**CLAUDE.md** is the answer. It is a plain-text file that Claude Code reads automatically at the start of every session in that folder, and uses as background knowledge for the rest of the conversation.

Think of it as an onboarding document for a new team member - except you write it once and it is read every single day forever.

## What you already have

Open the file at the repo root:

```
cat /workspaces/msa-spe5spa-claude-workshop/CLAUDE.md
```

You will see the project-level CLAUDE.md we wrote for Northfield FC. It tells Claude:

- What the club is (fictional academy-level soccer club)
- Who the staff are (Pat the sport scientist, etc.)
- The data conventions (metres, ISO dates, `NF###` IDs)
- The end-state pipeline students are working towards
- How to behave with students (explain before acting, never commit secrets)

Read it. Notice it is not a wall of text. It is short, specific, and written for a reader who has never seen this project.

## Why files nested below matter

Claude Code reads **CLAUDE.md files hierarchically**. If you start a Claude Code session in `module-4-build-a-tool/`, Claude reads:

1. The root `CLAUDE.md` (global project context)
2. The `module-4-build-a-tool/CLAUDE.md` (module-specific context)

More specific context wins when they conflict. This means you can have a general "we use metres" rule at the project level, and a module-specific "for this exercise, convert to kilometres for display" rule that overrides it.

## Writing one yourself

Open `module-3-claude-md/CLAUDE.md` (already in this folder). It is a skeleton. Fill in the blanks.

This is a Markdown (`.md`) file. Markdown is plain text with light formatting:

- `#` and `##` make headings.
- `-` makes bullet points.
- Backticks mark commands, filenames, or code.
- `<!-- ... -->` marks a comment. The comments in this file are prompts for you; replace them with your own text.

You do not need a strict syntax for `CLAUDE.md`. Claude reads normal sentences. Headings and bullets just make the context easier to scan. Do not put secrets in comments; comments are still part of the raw file.

The skeleton asks you to describe:

1. **Your role in the club**: analyst? intern? performance scientist? One sentence.
2. **Your preferred working style**: do you want short summaries or long explanations? Do you want Claude to ask before running destructive commands?
3. **What "done" looks like** for your version of the report: headline number? Player table? Traffic-light grading?

For example:

```markdown
## About me

I am a junior performance analyst at Northfield FC. I mostly work with the U23 squad, and I am still learning sport-science terminology, so explain acronyms the first time you use them.

## How I like to receive output

- Start with the answer, then give the reasoning.
- Keep summaries short enough for a coach to read quickly.
- Use British English.
- A little dry humour is fine when we are discussing workflow or mistakes, but keep coach-facing reports professional.
- Ask before running destructive commands or deleting files.
- Show me the important code changes before applying them.

## What "done" looks like for this module

Done means I have a cleaning script that can be run again on a messy GPS export, produces a tidy CSV, and prints a short summary showing how many rows were read, written, dropped, and why.

## Any domain quirks specific to this exercise

Northfield uses metres and metres per second. Player IDs should stay in the `NF###` format. If a value looks physically impossible, flag it rather than silently accepting it.
```

Save the file. Then start a Claude Code session inside this folder:

```
cd /workspaces/msa-spe5spa-claude-workshop/module-3-claude-md
claude
```

At the prompt, ask:

```
Who am I, what is my role, and how do I like to receive output?
```

If your CLAUDE.md is well-written, Claude will quote it back to you accurately. If it is vague, Claude will guess. This is the fastest way to tell whether your context file is doing its job.

## What goes in, what stays out

**Good things to put in CLAUDE.md:**

- Domain conventions (units, naming schemes, ID formats)
- Key people and their roles
- The "why" behind unusual choices in the codebase
- Non-obvious constraints ("reports must be under 500 words because the coach reads them on his phone")
- Safety rules ("never email raw data, always aggregate")

**Things to keep out:**

- Code that can be read directly (Claude can read it)
- Things that change every week (put these in a ticket or task list)
- Secrets, tokens, passwords - **never**, this file is committed to Git
- Wishy-washy style guidance ("please write clean code") - does nothing

## A pattern you will reuse

A useful habit: when you find yourself typing the same 3-line clarification into Claude twice in a week, that clarification belongs in CLAUDE.md. You are training your own future sessions.

## Done

You now know:

- Claude reads CLAUDE.md automatically
- It works hierarchically from root to current folder
- It is for stable context, not ephemeral state

Move on:

```
cd /workspaces/msa-spe5spa-claude-workshop/module-4-build-a-tool
```
