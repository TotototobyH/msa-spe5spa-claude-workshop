# Module 2: Your first Claude Code conversation

**Time: 15 minutes**

## Why this module exists

Before you type a single instruction to Claude, you need a clean mental model of **what Claude Code actually is** and how it differs from the ChatGPT-style window you are used to. Otherwise you will either undersell it ("it's just a chatbot in my terminal") or oversell it ("it can do anything") and both mistakes cost you hours.

## What Claude is (60 seconds)

Claude is a large language model made by Anthropic. You can think of it as a very well-read reader/writer. It has no memory between conversations, no body, no real-time internet access unless given one. It is a function: text in, text out.

You have probably used Claude at **claude.ai** - the chat interface on the web. You type, it replies, the conversation lives in a tab.

## What Claude Code is (90 seconds)

**Claude Code** is the same Claude model, but running as an agent inside your computer. "Agent" is a word we will earn in a moment. For now, three things are different from the chat window:

1. **Claude Code can read and write files on your machine.** It can open your CSVs, edit your R scripts, create new folders. Nothing uploads to the cloud in the clumsy copy-paste sense - the file stays local, but its *contents* get sent to Claude as part of the conversation.

2. **Claude Code can run commands.** It can execute `python`, `Rscript`, `git`, `typst`, shell commands. Each time it wants to run something, it asks you (the first time, at least). You approve or deny.

3. **Claude Code has tools.** Tools are named capabilities Claude can call - things like `Read`, `Edit`, `Bash`, `Grep`. When Claude decides a tool would help, it calls it, gets the result, and continues reasoning. You do not prompt the tools directly; Claude orchestrates them.

Put together, these three points are what people mean when they call Claude Code an **agent**. An agent is an LLM plus the ability to take actions in the world (read your files, run your code) in a loop until the task is done.

## Why this matters for analysts

A chat window is a **brain in a jar**. You read out your problem, it gives advice, you copy and paste.

Claude Code is a **teammate with hands**. You say "clean this GPS file, flag any session where a unit dropped, and summarise the result", and it opens the file, writes a script, runs the script, reads the output, tells you what it found. You review, correct, iterate. The end product is still your work - you are directing it - but you are no longer the one typing `import pandas`.

For a Northfield FC analyst, this turns a 45-minute cleaning chore into a 5-minute review.

## Setup: authenticate Claude Code

Your Codespace already has the Claude Code CLI installed. You need to connect it to your account.

If `claude` returns `command not found`, the Codespace setup did not finish or the CLI was not added to the terminal path. Run:

```bash
curl -fsSL https://claude.ai/install.sh | bash
source ~/.bashrc 2>/dev/null || true
export PATH="$HOME/.local/bin:$HOME/.claude/local:$PATH"
claude --version
```

If that still fails, rebuild the Codespace or ask for help before continuing.

### 3.1 Start Claude Code

In the terminal, at the repo root:

```
claude
```

The first time you run this, Claude Code will ask you to authenticate. A URL appears. Click it (Ctrl+click), sign in to your Claude account in the browser, copy the code it gives you back to the terminal, and press Enter.

If you see `> ` (an input prompt inside a box), you are in. Type `exit` and press Enter to leave - we will come back in a moment.

> **Plan note:** if authentication warns you that your plan does not include Claude Code, you are on the free tier. Upgrade to Pro or use a Claude Console API key. Talk to the instructor if this blocks you.

## Your first conversation

Now we are going to do something small to build intuition. Start Claude Code again:

```
claude
```

At the prompt, ask:

```
What files are in the data/ folder? Describe them briefly.
```

Watch what happens. You should see Claude announce what it is about to do ("I'll list the data folder and peek at each file"), then you will see **tool calls** appear in the transcript - something like `Bash(ls data/)` followed by `Read(data/squad_roster.csv)`. Those are the tools at work. Then Claude gives you a summary.

**Pause and look at that.** This is the loop: Claude plans, calls a tool, reads the result, plans the next step. You did not have to tell it *how* to look at files. It chose the tools.

### 4.2 Ask for something slightly harder

```
Which squads are represented in the roster, and how many players in each?
```

Claude will likely run a quick Python snippet or a `grep`/`awk` pipeline. Notice that you get a number, not a vague description. You can verify it yourself if you want (`grep -c U23 data/squad_roster.csv`).

### 4.3 Ask something it cannot answer

```
What was the Premier League result last weekend?
```

Claude Code does not have live internet by default. It will tell you it cannot browse, or that the information is outside its training data. **This is good.** Knowing where the edges are is half the skill.

## How to end a session

Type `exit` and press Enter. Or press Ctrl+D.

## What you should now believe

- Claude is a reader/writer you can converse with.
- Claude Code is Claude with hands: it reads your files, runs your commands, reports back.
- Tools are how Claude takes actions. You do not call them; Claude does, and you review.
- Claude Code stays local-first: files are read into prompts, nothing magical uploads unless *you* ask it to.

If any of the above is still fuzzy, ask the person next to you or raise a hand. Do not move on until this clicks.

## Done

```
cd /workspaces/msa-spe5spa-claude-workshop/module-3-claude-md
```

Open `module-3-claude-md/README.md`.
