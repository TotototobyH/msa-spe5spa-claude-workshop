# Module 7: Multi-Bot Extension

**Time: 15-20 minutes, optional self-guided extension**

Module 6 is the end of the main workshop. You already built the important workflow: a Telegram bot can receive a GPS CSV, Claude Code can run the report workflow, and the bot can return the PDF.

Module 7 is the next idea: what happens when one club workflow needs different front doors for different audiences?

## Why Another Bot?

The Module 6 load bot is for technical staff. Pat and the S&C lead can handle GPS language, player-level tables, thresholds, and PDF reports.

A head coach usually needs something different: a short message before training, not a full technical report.

| Audience | What they need | Better bot behaviour |
|----------|----------------|----------------------|
| S&C lead | Player-level load, spikes, and thresholds | Technical, detailed, PDF-friendly |
| Head coach | A fast read before training | Brief, direct, no unnecessary tables |
| Academy director | Squad trends and risk narrative | Squad-level, low jargon, board-safe |
| Parents of U16s | Carefully controlled updates | Narrow scope, no private medical detail |
| Recruitment staff | Talent ID combine summaries | Searchable, comparison-focused |

If one bot tries to serve every audience, it has to keep asking who it is talking to. A cleaner pattern is **one bot per audience**, each with its own context, permissions, tone, and skill scope.

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

The data can be the same. The model can be the same. The output changes because each bot has a different job.

## Step 1: Compare The Bot Contexts

From the repo root, run:

```bash
cat module-7-multi-bot/load-bot/CLAUDE.md
cat module-7-multi-bot/comms-bot/CLAUDE.md
```

Look for the differences:

- `load-bot` talks to technical staff and sends detailed reports.
- `comms-bot` talks to the head coach and sends short decision-ready messages.
- Both are grounded in the same Northfield FC project.

That is the key lesson: **context shapes behaviour**.

## Step 2: Inspect The Coach Brief Skill

Open:

```bash
cat skills/coach-brief/SKILL.md
```

Notice how the skill is narrower than the weekly PDF report. It asks for:

- exactly three sentences
- no PDF
- no tables
- no jargon
- only the players the coach needs to know about

That is what makes it useful as a coach-facing bot.

## Step 3: Test The Comms Behaviour Locally

Before connecting another Telegram bot, test the idea inside Claude Code.

From the comms bot folder, start Claude Code:

```bash
cd /workspaces/msa-spe5spa-claude-workshop/module-7-multi-bot/comms-bot
claude
```

Then ask:

```text
Produce the weekly coach brief using the coach-brief skill.
```

Expected result:

- a short coach-facing message
- no PDF
- no table
- no raw CSV dump
- no long explanation of the method

If the answer is too long, ask Claude to tighten it. The point of this bot is that the coach can read it quickly.

## Step 4: Optional Telegram Version

Only do this if you have time and are comfortable managing another bot token.

The official Telegram channel setup stores the configured token in local Claude Code channel state. That means if you configure a second Telegram bot in the same Codespace, you may replace the token used by the Module 6 load bot in that environment.

For learning, that is fine if you are testing **one bot at a time**.

For a real two-bot setup running at the same time, use separate controlled environments, for example:

- one Codespace or VPS for the load bot, and another for the coach bot
- one club-controlled Linux server service per bot
- one Mac mini service per bot, with separate secret storage and logs

Do not casually mix multiple bot tokens and allowlists in the same terminal session.

## Step 5: Create A Coach Bot

Use BotFather again:

```text
/newbot
```

Example:

- Name: `Northfield Coach Brief Bot`
- Username: `northfield_coach_nf123_bot`

Save the token privately. It is a separate secret from the Module 6 load bot token.

## Step 6: Configure The Coach Bot

Stop any currently running Telegram channel session first.

From the comms bot folder:

```bash
cd /workspaces/msa-spe5spa-claude-workshop/module-7-multi-bot/comms-bot
claude
```

Inside Claude Code:

```text
/plugin install telegram@claude-plugins-official
/reload-plugins
/telegram:configure 7891234567:AAH...coach-bot-token...
exit
```

Restart with the Telegram channel enabled:

```bash
claude --channels plugin:telegram@claude-plugins-official
```

Open the coach bot in Telegram, send `hello`, copy the pairing code, then run:

```text
/telegram:access pair <code>
/telegram:access policy allowlist
```

## Step 7: Test The Coach Bot

In Telegram, send:

```text
weekly coach brief
```

Expected result:

| Bot | Expected output |
|-----|-----------------|
| Load bot | PDF report plus short technical summary |
| Coach comms bot | Three-sentence coach brief, no PDF |

Same project. Same data. Different audience.

## Why This Matters

In a real club, the danger is not only bad data. It is the right data sent to the wrong audience in the wrong form.

Separate bots make those boundaries visible:

- **Scope:** what the bot is allowed to answer
- **Tone:** how the bot speaks to its audience
- **Permissions:** who can trigger the bot
- **Outputs:** whether it sends PDFs, short messages, or summaries
- **Safety:** what it should refuse or redirect

## Production Notes

For a real deployment, do not run long-lived club bots from a class Codespace. Use an always-on controlled machine and document:

- who owns each bot
- who is on each allowlist
- which data each bot can access
- what each bot is allowed to send
- where each token is stored
- how tokens are rotated
- what to do when the bot gives an unexpected answer

The technical setup is only half the work. The professional work is deciding who should receive which information, in what form, and with what safeguards.

## Done

You now have the pattern for an analyst-owned bot ecosystem: one shared workflow, multiple audience-specific front doors.
