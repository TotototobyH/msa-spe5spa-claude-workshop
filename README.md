# MSA Claude Code Workshop

**Master of Sport Analytics, La Trobe University**
**Subject:** SPE5SPA - Sports Project A
**Session:** Week 8, Wednesday AM (29 April 2026)

This workshop is a practical first pass at using Claude Code in a sport analytics workflow. You will start in the terminal, work through a messy GPS export, turn that process into a repeatable report, and finish with a phone-fronted analyst agent that can receive a file and send back a coach-ready PDF.

## The Lesson

You work as a performance analyst at **Northfield FC**, a fictional academy-level soccer club.

Pat, the sport scientist, exports GPS data after training. The file is messy: dates are inconsistent, session names do not match, some GPS units drop fields, and a few rows are clearly wrong. Your job is to build a workflow that checks the file, cleans it, rolls it up, flags load spikes, and produces a standard weekly report.

By the end, Pat can send the CSV through Telegram and get help from something that behaves less like a normal chatbot and more like a junior sport analyst: it receives the file, checks it, cleans it, runs the report workflow, and replies with a PDF and a short summary.

That is the bigger idea behind the workshop. The first version is one small analyst focused on GPS reporting. Over time, the same pattern could become a small team of specialist analyst agents: one for training load, one for coach briefings, one for wellness, one for talent ID, and one for operations. In a real organisation, access to a service like Claude should ideally be paid for and governed by the organisation, not improvised through individual student or staff accounts.

## What You Will Learn

| # | Module | Purpose | What you do | What you produce | Time |
|---|--------|---------|-------------|------------------|------|
| 1 | Terminal basics | Get comfortable moving around a code project | Use `pwd`, `ls`, `cd`, `head`, `grep`, and `git status` | Confidence using the terminal without guessing where you are | 10 min |
| 2 | First Claude Code conversation | Understand Claude Code as an agent, not just chat | Start Claude Code, ask it to inspect files, watch tool calls | A clear mental model of tools, files, commands, and limits | 15 min |
| 3 | `CLAUDE.md` and context | Learn how stable project context changes Claude's behaviour | Read the project `CLAUDE.md`, then write a small module-level one | A context file that tells Claude who you are and what "done" means | 10 min |
| 4 | Build a GPS cleaning tool | Turn messy sport data into a deterministic process | Ask Claude to inspect the CSV, agree cleaning rules, review and run the script | `clean_gps.py` and a cleaned GPS CSV | 20 min |
| 5 | Automate the weekly report | Use a skill and Typst template for repeatable reporting | Invoke the weekly-load-report skill and compile a PDF | A one-page Northfield FC training-load report | 20 min |
| 6 | Analyst agent on Telegram | Put the report workflow behind a phone chat | Create a bot, configure Claude Code Channels, allowlist yourself, send a CSV | A junior analyst-style agent that returns the report PDF | 20 min |
| 7 | Optional multi-agent extension | Separate audiences by bot, context, and skill | Compare load-bot and comms-bot roles, then optionally test a second audience-specific brief | A pattern for coach, S&C, board, or parent-facing analyst agents | Self-guided |

The main workshop ends at Module 6. Module 7 is there if you want to explore the next pattern after class.

## Why These Tools?

We use **GitHub Codespaces** so everyone starts from the same environment, but the bigger reason is safety. Claude Code can read files, run commands, edit code, and use tools inside a workspace. That is useful, but it is not something you should first try in a personal laptop folder full of unrelated documents, browser sessions, SSH keys, cloud-sync folders, and private files.

Codespaces keeps this workshop inside a repo-specific cloud development environment. You can make mistakes, run commands, and test the bot workflow without giving the agent broad access to your own computer. It is not the production setup a club would run forever, but it gives us a safer and more consistent learning boundary.

We use **Claude Code** because it can work inside the project: it can read files, edit scripts, run commands, use skills, and check its own output. The point is not to stop thinking. The point is to move from typing every line yourself to directing, reviewing, and verifying the work.

We use **Skills** because a sport analytics team needs repeatable workflows. A weekly report should not depend on which analyst happened to be on shift.

We use **Claude Code Channels with Telegram** because the final workflow should feel like the way staff already communicate. Pat sends a file from his phone; the analyst agent replies with the report. Telegram is the front door; Claude Code is the project-aware analyst doing the work behind it.

## What You Need Before Class

- A **GitHub account**: <https://github.com/signup>
- A **Claude account that can use Claude Code**. Claude Code requires Pro, Max, Team, Enterprise, or Console access; the free Claude.ai plan does not include Claude Code access. Check the current Claude plan details before class because prices and plan features can change. In a real club or organisation, this should ideally be handled as an organisation-paid and governed service rather than a personal workaround.
- A phone with **Telegram** installed for Modules 6 and 7.

Useful current references:

- Claude Code setup: <https://code.claude.com/docs/en/getting-started>
- Claude Code Channels: <https://code.claude.com/docs/en/channels>
- Claude plan guide: <https://support.claude.com/en/articles/11049762-choosing-a-claude-plan>

Optional background reading:

- [OpenClaw context and why we are not using it here](background/openclaw-context.md)

## Start Here

1. Click the green **Code** button at the top of this repo.
2. Select the **Codespaces** tab.
3. If this is your first time, click the **+** button or **Create codespace on main**. If you already see a named Codespace such as `sturdy tribble`, that is an existing workspace; click it only if you want to continue where you previously left off.
4. Check the billing message. It should show your own GitHub account or your organisation's approved billing account. If it says the instructor's name, stop and ask before creating the Codespace.
5. Creating a Codespace gives you your own cloud workspace. It does not change the instructor's Codespace or modify the repo's `main` branch by itself.
6. Wait for the setup to finish. The first launch installs Python libraries, R libraries, Typst, Bun, and Claude Code.
   - This can take several minutes, and in some Codespaces it may take around 15 minutes.
   - If the terminal says `Running postCreateCommand...`, setup is still running.
   - The Explorer panel may show the files before setup has finished. That does not mean Claude Code is ready yet.
   - Do not run `claude` until the setup has finished and you have a normal terminal prompt again.
   - If setup is still printing package-install messages, let it continue.
   - When setup is complete, you should see lines like `Claude Code successfully installed!`, `Installation complete!`, a Claude Code version number, and `Outcome: success`.
7. When the terminal prompt appears, run:

```bash
claude --version
claude doctor
```

If `claude` says `command not found`, the Codespace setup did not finish or the CLI was not added to the terminal path. Run:

```bash
curl -fsSL https://claude.ai/install.sh | bash
source ~/.bashrc 2>/dev/null || true
export PATH="$HOME/.local/bin:$HOME/.claude/local:$PATH"
claude --version
```

If that still does not work, rebuild the Codespace or ask for help before continuing.

8. Start Claude Code:

```bash
claude
```

9. Inside Claude Code, run:

```text
/status
```

If Claude Code says your account does not have access, stop there and ask for help. Do not wait until Module 4 to discover that your plan is blocking you.

## Folder Structure

```text
msa-spe5spa-claude-workshop/
├── .devcontainer/         # Codespace build config
├── CLAUDE.md              # Shared project context for Claude Code
├── background/            # Optional context readings
├── data/                  # Synthetic Northfield FC datasets
├── skills/                # Reusable Claude Code skills
├── module-1-terminal/
├── module-2-first-chat/
├── module-3-claude-md/
├── module-4-build-a-tool/
├── module-5-automate-report/
├── module-6-telegram-bot/
└── module-7-multi-bot/
```

Every module folder has its own `README.md`. From Module 3 onwards, some folders also have a local `CLAUDE.md` so you can see how context changes behaviour.

## Safety Rules

- Tokens, passwords, and API keys never go in Git.
- `.env` is ignored already. Use it for local secrets.
- Player IDs are synthetic (`NF###`). Do not paste real athlete data into this repo.
- Reports are generated artefacts. They are useful outputs, but they do not need to be committed.

## After The Workshop

Codespaces is a teaching environment. A real club bot should run on an always-on controlled machine, not on an analyst's everyday laptop.

A **VPS** means **virtual private server**. In plain English, it is a computer you rent on the internet. It usually runs Linux, often Ubuntu LTS, and you connect to it remotely through a terminal using SSH. For a bot workflow, you clone the repo there, install the tools, store the bot token as a secret, and keep the bot running from that server.

Good production options include:

- a **VPS** such as DigitalOcean Droplets, Hetzner Cloud, Akamai Linode, Vultr Cloud Compute, or AWS Lightsail
- an organisation-approved cloud VM such as Azure Virtual Machines or Google Cloud Compute Engine
- a club-controlled **Mac mini**
- a club-controlled **Linux server**
- an internal university, institute, or club server managed by IT

The point is isolation. The machine should contain only the project files, packages, secrets, and data needed for the workflow. It should not contain your personal downloads, unrelated projects, browser sessions, cloud-sync folders, or private SSH keys.

Production adds extra work: access control, monitoring, backups, token rotation, data governance, and a clear policy for athlete information.
