# Module 7: Multi-Bot Ecosystem

**Time: 15 minutes - optional extension**

## Why Another Bot?

Your load bot from Module 6 is for people who need the technical report: Pat, the sport scientist, and the S&C lead. It can use GPS language, send PDFs, and include player-level tables.

That is not the same as a coach update.

Different people at a club need different outputs:

| Audience | What they need | Good bot behaviour |
|----------|----------------|--------------------|
| S&C lead | Player-level load, spikes, and thresholds | Technical, detailed, happy to send PDFs |
| Head coach | A fast read before training | Brief, direct, no unnecessary tables |
| Academy director | Monthly trend and risk narrative | Squad-level, low jargon, board-safe |
| Parents of U16s | Opt-in wellbeing and involvement updates | Carefully worded, no private medical claims |
| Recruitment staff | Talent ID combine summaries | Searchable, comparison-focused, no coaching chatter |

If one bot tries to serve every audience, it has to ask "who am I talking to?" before almost every useful answer. A cleaner pattern is **one bot per audience**, each with its own context, permissions, and skill scope.

## The Pattern

```text
shared repo + data + skills
        |
        +-- load-bot context   -> weekly-load-report skill -> PDF for technical staff
        |
        +-- comms-bot context  -> coach-brief skill        -> short message for coaches
        |
        +-- future bot context -> future skill             -> audience-specific output
```

The data can be the same. The model can be the same. The output changes because the bot is given different context and a different job.

Open these files and compare them:

```bash
cat module-7-multi-bot/load-bot/CLAUDE.md
cat module-7-multi-bot/comms-bot/CLAUDE.md
```

Notice the differences:

- `load-bot` speaks to technical staff and defaults to report detail.
- `comms-bot` speaks to the head coach and defaults to short, decision-ready language.
- Both are grounded in the same Northfield FC project.

That is the lesson: **context shapes behaviour**.

## Step 1: Create A Second Telegram Bot

Use BotFather again:

```text
/newbot
```

Give the second bot a coach-facing name, for example:

- Name: `Northfield Coach Brief Bot`
- Username: `northfield_coach_nf123_bot`

Save the token. It is a separate secret from the load bot token.

## Step 2: Keep State Separate

The Telegram channel plugin stores token and allowlist state locally. For two bots on one machine, use separate state directories so the tokens and allowlists do not overwrite each other.

If your Module 6 load bot is already running, leave it alone. It can keep using the default Telegram state directory.

For a clean two-bot setup, configure each bot from a terminal that has its own `TELEGRAM_STATE_DIR`. For the load bot:

```bash
export TELEGRAM_STATE_DIR="$HOME/.claude/channels/telegram-load"
claude
```

Then, inside Claude Code:

```text
/plugin install telegram@claude-plugins-official
/reload-plugins
/telegram:configure 7891234567:AAH...load-bot-token...
exit
```

Restart it with the same state directory and the channel enabled:

```bash
export TELEGRAM_STATE_DIR="$HOME/.claude/channels/telegram-load"
claude --channels plugin:telegram@claude-plugins-official
```

For the coach comms bot, open a second terminal:

```bash
export TELEGRAM_STATE_DIR="$HOME/.claude/channels/telegram-comms"
claude
```

Each terminal runs one bot session. Each state directory needs its own token configuration and allowlist pairing.

## Step 3: Configure The Comms Bot

In the second Claude Code session, install/reload the plugin if needed:

```text
/plugin install telegram@claude-plugins-official
/reload-plugins
```

Configure the coach bot token:

```text
/telegram:configure 7891234567:AAH...coach-bot-token...
```

Restart the second session with the same state directory:

```bash
export TELEGRAM_STATE_DIR="$HOME/.claude/channels/telegram-comms"
claude --channels plugin:telegram@claude-plugins-official
```

Message the coach bot from Telegram, then pair and lock it down:

```text
/telegram:access pair <code>
/telegram:access policy allowlist
```

## Step 4: Give The Comms Bot Its Role

At the Claude Code prompt for the comms bot, send:

```text
Use the comms-bot context in module-7-multi-bot/comms-bot/CLAUDE.md. When I ask for the weekly coach brief, use the coach-brief skill and reply with a short coach-facing message only. No PDF unless I explicitly ask for one.
```

Then test the skill in the terminal before using Telegram:

```text
Produce the coach brief for this week using the coach-brief skill.
```

If the answer is too long, tell Claude to tighten it. The whole point of this bot is that the coach can read it quickly.

## Step 5: Compare The Two Bots

Send a similar request to each bot:

```text
weekly report
```

Expected result:

| Bot | Expected output |
|-----|-----------------|
| Load bot | PDF report plus short technical summary |
| Coach comms bot | Three-sentence coach brief, no PDF |

Same project. Same data. Different audience.

## Why This Matters

In a real club, the danger is not only bad data. It is the right data sent to the wrong audience in the wrong form.

The S&C lead may want thresholds and player-level detail. The head coach may want three clear sentences. Parents may need careful wording and a much narrower scope. A board report may need trends without tactical detail.

Separate bots make those boundaries visible:

- **Scope:** what the bot is allowed to answer
- **Tone:** how the bot speaks to its audience
- **Permissions:** who can trigger the bot
- **Outputs:** whether it sends PDFs, short messages, or summaries
- **Safety:** what it should refuse or redirect

## Production Notes

For a real deployment, do not run long-lived club bots from a class Codespace. Use an always-on environment and document:

- who owns each bot
- who is on each allowlist
- which data each bot can access
- what each bot is allowed to send
- how tokens are rotated
- what to do when the bot gives an unexpected answer

The technical setup is only half the work. The professional work is deciding who should receive which information, in what form, and with what safeguards.

## Done

You now have the pattern for an analyst-owned bot ecosystem: one shared workflow, multiple audience-specific front doors.

Return to the root README for the workshop recap.
