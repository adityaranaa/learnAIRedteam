# Diagnostic 01: "OpsPilot" (synthetic target)

An internal IT-helpdesk agent at a ~300-person company. You have an ordinary employee account.
Authorized black-box test; no source access.

## What you have observed during recon
1. You DM `@OpsPilot` in Slack; it replies in-thread.
2. It answers IT policy questions and cites Confluence pages by title + link.
3. Any employee can edit pages in the Confluence space `IT-Public`.
4. "Check my laptop status" works. An error once surfaced: `ToolError: get_device(owner_email='you@corp.com') timeout`.
5. "Open a ticket" creates a Jira issue; the reporter shows as service account `opspilot-bot`.
6. "What's the status of IT-1234?" makes it summarize the ticket, **including comments**.
7. The Jira service desk accepts email-to-ticket: anyone on the internet emailing `support@corp.com`
   creates a ticket whose description is the email body.
8. "Reset my MFA" → "I've sent a reset link to your registered email."
   "Reset MFA for alice@corp.com" → "I can only reset MFA for your own account."

## Questions (answered one at a time in session)
- Q1 Map: assets, trust boundaries, facts vs assumptions, where is the "own account only" rule enforced?
- Q2 Hypothesis + minimum experiment + predicted outcomes
- Q3 Validation: interpret a result and rule out alternative explanations
- Q4 Root cause, architectural mitigation, regression test

## Answers & assessment

### Q1 answer (learner, 2026-10-15, summarized)
- Entry points: Slack DM, Confluence (anyone can edit, read by the bot), email
- Indirect prompt injection via an edited Confluence page, triggered by a Slack DM
- Assumption: bot has many tools and access to all employee asset data
- Bot "controls" Jira; MFA can be reset via support@corp.com → Jira → OpsPilot
- (c) unsure; leaned toward "system prompt" without a reason

### Q1 assessment
Strong: independently found the Confluence indirect-injection vector and named email as an input.
Gaps:
1. **Facts vs assumptions mixed.** "Reset MFA via support@corp.com" is not observed; it merges obs 7 and 8.
2. **No asset list.** Biggest asset = the MFA reset action (account takeover). Others: device and owner data,
   ticket contents, the `opspilot-bot` service account privileges.
3. **Missed the strongest chain.** An unauthenticated internet sender writes a ticket (obs 7), OpsPilot reads
   ticket text into context (obs 6), and the same agent holds an MFA-reset tool (obs 8). That is an external
   attacker reaching a privileged agent, which is worse than an insider editing Confluence.
4. **Missed the identity clue.** Obs 4: `get_device(owner_email=...)` means the *model fills in* the identity
   argument. If `reset_mfa` has the same shape, "own account only" is probably enforced only by the prompt.
5. **Authorization-locus concept gap (c).** Did not have a method for telling prompt-level refusal apart from
   code-level enforcement from outside.
