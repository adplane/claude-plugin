---
description: Review connected Google Ads and Meta Ads accounts for a period versus the previous one
argument-hint: <period, e.g. "last 7 days" or "this month">
---
Run an account review for $ARGUMENTS (default: last 7 days versus the 7 before), following the `adplane-account-review` skill.

1. Call `google_list_accounts` and `meta_list_accounts` in parallel. Only pull platforms that came back connected. If a list is empty, relay its `notice` as written.
2. Google: `google_run_report` on `resource: "campaign"` for the period and for the previous equivalent period, with campaign name, status, cost, clicks, impressions, conversions, and conversion value. Call `google_get_report_schema` first for any field not yet used in this conversation.
3. Meta: `meta_run_report` at `level: "campaign"` for both periods with spend, impressions, clicks, ctr, cpc, and the conversion the user cares about via `action_types`. Call `meta_get_schema` first for any field not yet used.
4. Present one scorecard: per platform, then total. Spend, conversions, cost per conversion or ROAS, CTR and CPC as diagnostics, and the change versus the previous period. State the exact dates the tools echoed.
5. Lead with the answer: the biggest problem, the biggest opportunity, one recommendation with the number attached. Offer to act; applying changes belongs to `/wasted-spend` or the `adplane-optimize` skill, not this command.
