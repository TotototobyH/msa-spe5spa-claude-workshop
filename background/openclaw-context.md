# Optional Background: OpenClaw

Last checked: 2 May 2026

This note is background reading for the workshop. It is not an installation guide, and we will not use OpenClaw in the practical modules.

## What OpenClaw Is

OpenClaw is an open-source, self-hosted personal AI assistant. It is designed to run on a machine you control and connect a language model to real tools: messaging apps, files, shell commands, browser control, APIs, memory, and skills.

That makes it different from ordinary chat. A chat interface mostly answers what you ask in the moment. A self-hosted agent can sit near your tools and act across them, sometimes on a schedule or in response to messages from apps like Telegram, WhatsApp, Discord, Slack, Signal, or iMessage.

That is the appeal: it feels closer to an always-on assistant than a question-answer box.

## Why It Became Popular

OpenClaw became popular because it combines several ideas that many AI users want at the same time:

- It is open source, so people can inspect, change, and extend it.
- It is self-hosted, so people can run it on a personal machine, VPS, private server, or local workstation.
- It works through familiar chat apps rather than requiring a new interface.
- It has persistent memory, so context can continue across sessions.
- It can use skills and plugins, so the community can add new capabilities.
- It can control files, browsers, shell commands, and APIs, which makes it feel practical rather than purely conversational.

The OpenClaw homepage reports more than 180,000 GitHub stars. The OpenClaw docs describe a rapid early history, including more than 100,000 stars in about two days. A 2026 security paper describes OpenClaw as the most widely deployed personal AI agent in early 2026.

That does not mean it is one of the most-used software products in the world. A more careful claim is that it became one of the fastest-growing and most widely discussed open-source personal-agent projects of early 2026.

## Short History

The public OpenClaw docs describe this timeline:

- November 2025: created by Peter Steinberger as Clawdbot.
- 27 January 2026: renamed to Moltbot after trademark complaints relating to the similarity between "Clawd" and "Claude".
- 28 January 2026: Moltbook launched as a social network for AI agents.
- 30 January 2026: renamed again to OpenClaw.
- Late January 2026: went viral and, according to the OpenClaw docs, gained more than 100,000 GitHub stars in about two days.
- February 2026 onwards: rapid community growth, security scrutiny, and increased discussion about how to run self-hosted agents safely.

The names matter less than the pattern. OpenClaw became a symbol of a broader shift: people want AI agents that can do work across tools, not only answer questions in a chat window.

## Why We Are Not Using It In This Workshop

OpenClaw is interesting, but it is not the right starting point for this class.

The main issue is security. A self-hosted agent with persistent memory, messaging access, browser control, file access, shell access, and community skills has a large attack surface. If it runs on a personal laptop, it can sit close to personal files, browser sessions, developer credentials, cloud accounts, and local configuration.

Microsoft's security guidance says OpenClaw should be treated as untrusted code execution with persistent credentials and should only be evaluated in an isolated environment with dedicated credentials and non-sensitive data.

Cisco's AI security research also highlights the risk of community skills. Skills are not just friendly descriptions; they can include code, prompts, and files that influence agent behaviour. Cisco reported a third-party OpenClaw skill behaving like malware, including silent data exfiltration and prompt injection.

OpenClaw's own security docs make the same basic point in a more practical way: there is no perfectly secure setup. The safest pattern is to start with the smallest access that works, use allowlists, deny broad tools by default, sandbox where possible, and keep secrets outside the agent's reach.

For a sport analytics teaching repo, that matters. A future club workflow might involve sensitive athlete data, private staff communication, and production systems. The beginner version should therefore be narrow:

- one repo
- synthetic data
- one Telegram bot
- an allowlisted sender
- a clear cleaning/reporting workflow
- no real athlete data
- no broad personal-computer access

That is why this workshop uses GitHub Codespaces and Claude Code Channels instead. It still teaches the core pattern: a project-aware agent connected to a phone-friendly interface. It just keeps the first version bounded and easier to review.

## Cost And Model Access

Open source does not automatically mean free to run.

The OpenClaw code may be free, but model calls, hosted APIs, web search, transcription, image analysis, embeddings, and long-running background jobs can still cost money. Always-on agents can also create much more usage than normal chat because they may check messages, run scheduled tasks, read files, and call models repeatedly.

The current OpenClaw docs say OpenClaw can use API keys, local models, and some subscription or OAuth-style provider paths. They also say API keys are usually the most predictable option for long-lived gateway hosts.

So the accurate point is not "OpenClaw can no longer use Claude or OpenAI." The accurate point is that model access, provider terms, subscription rules, and billing can change, and production users need to check those details before building around any provider.

## How This Relates To Northfield FC

The Northfield FC workflow is a safer, smaller version of the same idea.

Instead of building an always-on personal operating system, we build one repeatable analytics workflow:

1. receive a messy GPS CSV
2. clean it with clear rules
3. generate a standard report
4. return the PDF through Telegram

The lesson is not "avoid all personal agents forever". The lesson is: match the agent architecture to the task, the data, the audience, and the risk.

## Sources

- OpenClaw homepage: <https://openclaw.ai/>
- OpenClaw introduction docs: <https://clawdocs.org/getting-started/introduction/>
- OpenClaw FAQ: <https://docs.openclaw.ai/faq>
- OpenClaw authentication docs: <https://docs.openclaw.ai/gateway/authentication>
- OpenClaw API usage and costs: <https://docs.openclaw.ai/reference/api-usage-costs>
- OpenClaw security docs: <https://docs.openclaw.ai/security>
- Microsoft Security Blog, "Running OpenClaw safely: identity, isolation, and runtime risk": <https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/>
- Cisco Blogs, "Personal AI Agents like OpenClaw Are a Security Nightmare": <https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare>
- Wang et al., "A Systematic Security Evaluation of OpenClaw and Its Variants": <https://arxiv.org/abs/2604.03131>
- UCSC VLAA, "Your Agent, Their Asset: A Real-World Safety Analysis of OpenClaw": <https://arxiv.org/abs/2604.04759>
