# Module 6: Your Own Telegram Bot

**Time: 20 minutes**

## The Scenario

So far, the workflow still depends on you:

1. Pat sends you the GPS file.
2. You open Claude Code.
3. You ask for the report.
4. You send the PDF back.

This module removes the middle steps. Pat sends the CSV to a Telegram bot. Claude Code receives the message through a channel plugin, runs the same cleaning and reporting workflow, and replies with the PDF.

At the end of this module, you will have a Telegram bot running from your Codespace. Only people you allowlist can use it.

## What Is A Telegram Bot?

A Telegram bot is an account controlled by software. It has:

- a display name, such as `Northfield Load Bot`
- a username ending in `bot`, such as `northfield_load_nf123_bot`
- a token, which is the secret password that lets software act as the bot

Claude Code does not magically live inside Telegram. Instead, we use **Claude Code Channels**. A channel plugin listens for new Telegram messages, passes them into your running Claude Code session, and gives Claude a tool for replying.

That distinction matters: the bot only works while Claude Code is running with the Telegram channel enabled.

## Step 1: Check The Required Tools

From the repo root, run:

```bash
bun --version
claude --version
claude doctor
```

The Telegram channel plugin needs Bun. The Codespace should install it automatically. If `bun --version` fails, stop and ask for help before creating a bot.

Then start Claude Code:

```bash
claude
```

Inside Claude Code, check your account:

```text
/status
```

Claude Code requires Pro, Max, Team, Enterprise, or Console access. The free Claude.ai plan does not include Claude Code access. Plan names, prices, and limits can change, so check the current Claude plan page rather than assuming the cheapest option will support the whole workflow.

## Step 2: Create A Bot With BotFather

On your phone, open Telegram and search for **@BotFather**. Use the verified account with the blue tick.

Send:

```text
/newbot
```

BotFather asks for:

- **Name:** this appears in chat headers, for example `Northfield Load Bot`.
- **Username:** this must be unique and must end in `bot`, for example `northfield_load_nf123_bot`.

BotFather replies with a token that looks like:

```text
7891234567:AAH...long-random-string
```

Treat the token like a password. Anyone with it can act as your bot.

## Step 3: Install The Telegram Channel Plugin

In Claude Code, install the official Telegram plugin:

```text
/plugin install telegram@claude-plugins-official
/reload-plugins
```

If Claude Code says the plugin cannot be found, refresh the official marketplace and retry:

```text
/plugin marketplace update claude-plugins-official
/plugin install telegram@claude-plugins-official
/reload-plugins
```

If the marketplace is still missing, add it and retry:

```text
/plugin marketplace add anthropics/claude-plugins-official
/plugin install telegram@claude-plugins-official
/reload-plugins
```

## Step 4: Configure The Token

Still inside Claude Code, configure the bot token:

```text
/telegram:configure 7891234567:AAH...your-token-here...
```

Paste your real token in that command. The plugin stores it in Claude Code's local channel state, not in the Git repo.

Do not paste the token into `README.md`, `CLAUDE.md`, a Python file, or a GitHub issue.

After the token is accepted, Claude Code may say that the allowlist is empty and tell you to pair your Telegram account. That is expected. Do not test the bot yet. First restart Claude Code with the channel enabled.

## Step 5: Restart With The Telegram Channel Enabled

Exit Claude Code:

```text
exit
```

Then restart it with the Telegram channel enabled:

```bash
claude --channels plugin:telegram@claude-plugins-official
```

You should see Claude Code start normally. This session is now listening for Telegram messages from your bot.

Run this from inside the workshop repo, ideally from the `module-6-telegram-bot` folder, so Claude has the Module 6 `CLAUDE.md` context available.

## Step 6: Pair And Allowlist Yourself

In Telegram, search for the bot username that BotFather gave you. Open the matching bot. If you see a **Start** button, click it. Then send:

```text
hello
```

The bot should reply with a short pairing code.

If the bot does not reply, check that Claude Code is running with:

```bash
claude --channels plugin:telegram@claude-plugins-official
```

Back in Claude Code, run:

```text
/telegram:access pair <code>
```

Replace `<code>` with the code Telegram gave you.

Now lock the bot down so only allowlisted users can talk to it:

```text
/telegram:access policy allowlist
```

This is the security step. Without it, the bot may keep offering pairing codes to people who discover the username.

## Step 7: Test From Your Phone

In Telegram:

1. Send `Please run the Northfield weekly load report for this CSV.`
2. Send `data/gps_training_messy.csv` as a file attachment. In Codespaces, you can right-click the file and download it to your computer or phone first.

Send the CSV as a file/document, not as pasted text. Telegram messages are not a good place for raw CSV content.

You do not need to brief Claude again if it has loaded this repo's `CLAUDE.md` files. The root `CLAUDE.md` describes the workshop workflow, and this module's `CLAUDE.md` says what to do when a GPS file arrives through Telegram.

If Claude seems unsure, send: `Use the Module 6 CLAUDE.md instructions for Telegram GPS files, then run the weekly-load-report skill.`

The bot should:

- acknowledge the file
- clean and aggregate the data
- compile the Typst PDF
- reply with the PDF and a short written summary

Open the PDF and check that it matches the standard report from Module 5.

## What To Do When It Breaks

It will break at some point. That is normal.

| Problem | What to check |
|---------|---------------|
| Bot does not reply | Is Claude Code running with `claude --channels plugin:telegram@claude-plugins-official`? |
| Pairing code never arrives | Did you configure the correct token from BotFather? Did you message the right bot username? |
| Claude receives one message but not the next | Press Enter in the Claude Code terminal and check whether the session is waiting for input or permission. |
| `Not allowed` or ignored messages | Run `/telegram:access pair <code>` again, then `/telegram:access policy allowlist`. |
| PDF is missing or empty | Ask Claude to inspect the CSV schema and compare it with the Module 4 cleaning rules. |
| Telegram says there is a conflict | Make sure the same bot token is not running in another Codespace or terminal. |

## What You Learned

- Telegram bots are accounts controlled by tokens.
- Tokens are secrets and must never be committed.
- Claude Code Channels let external messages enter a running Claude Code session.
- The bot works only while the channel-enabled Claude Code session is running.
- Access control matters because a channel user can trigger work in your session.

## Production Notes

Codespaces is fine for learning, but it pauses when inactive. A real club workflow would run on an always-on machine, usually a VPS or a club-controlled server.

Before using this pattern with real athlete data, you would also need:

- a paid Claude setup with enough usage for the workload
- a data governance review
- clear allowlists for staff accounts
- logging and monitoring
- a plan for what happens when the bot fails

## Done

You have connected a phone chat to a repeatable sport analytics workflow.

This is the end of the main workshop.

If you want to keep going, Module 7 is an optional self-guided extension. It shows why a club might eventually run more than one analyst bot: one for technical load reports, another for short coach briefings, and others for different audiences.

```bash
cd /workspaces/msa-spe5spa-claude-workshop/module-7-multi-bot
```
