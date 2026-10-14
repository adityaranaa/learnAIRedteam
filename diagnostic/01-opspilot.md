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
