---
name: adplane-account-review
argument-hint: <period, e.g. "last 7 days" or "this month">
description: Review how Google Ads and Meta Ads accounts are doing, with spend, conversions, cost per result, ROAS, and what changed versus the previous period. Use when the user asks "how are my ads doing", "check my Google Ads account", "check my Facebook ads", "weekly report", "what's my ROAS", "why did CPA go up", or wants a scorecard across both platforms, even when they don't say Adplane. Read-only, changes nothing. Not for building campaigns or applying changes, use adplane-build-campaign or adplane-optimize.
---

# Account review

Follow `adplane-agent` first. This skill only reads. When invoked directly,
$ARGUMENTS is the period (default: last 7 days against the 7 before).

## Get the numbers

1. Resolve accounts with `google_list_accounts` and `meta_list_accounts`
   (parallel). Only pull platforms that came back connected; do not fire
   calls that will fail and then report the failures.
2. **Google.** `google_run_report` on `resource: "campaign"` with
   `date_range` for the period and again for the previous equivalent period.
   Fields to start with: `campaign.name`, `campaign.status`,
   `metrics.cost_micros`, `metrics.clicks`, `metrics.impressions`,
   `metrics.conversions`, `metrics.conversions_value`. Money comes back
   already in the account currency; the `cost_micros` column arrives as
   `cost`. Call `google_get_report_schema` before using any field you have
   not already used in this conversation.
3. **Meta.** `meta_run_report` with `level: "campaign"`, the same two date
   ranges, and fields such as `campaign_name`, `spend`, `impressions`,
   `clicks`, `ctr`, `cpc`. Pass `action_types` (for example `["lead"]` or
   `["purchase"]`) to get the conversion the user cares about as its own
   count and cost columns. Call `meta_get_schema` for the field list before
   using a name you have not used yet.
4. `date_range` on both platforms takes a preset like `LAST_7_DAYS` or
   `LAST_30_DAYS`, or an explicit `2026-06-01..2026-06-30`. The response
   echoes the dates it used; always state them.

Compare like with like: last 7 days against the 7 before, never against a
partial week. Today is always partial and Google data can lag about three
hours, so a "drop" that is really an unfinished day is the most common false
alarm in this job.

## Before you trust a conversion number

Ask what a conversion is here and whether tracking is known to work. A
campaign that appears to convert nothing very often converts fine and
reports nothing. If the user is unsure, say that the conversion columns are
only as good as the tracking, and lead with spend, clicks, and click cost,
which are always real.

## The scorecard

Per platform, then in total when both are present:

- spend, and pace against the monthly budget if the user has one
- conversions and cost per conversion (or ROAS where revenue is tracked)
- CTR and CPC as diagnostics, not goals
- change versus the previous period, as a percentage with the absolute
  numbers next to it

Do not average CPA across platforms with very different volumes and call it
"blended" without saying so.

## Say what it means

A table is not a review. Lead with the answer, for example: "Google is doing
the work: 34 leads at 41, under your 50 target. Meta spent 890 for 3 leads,
and its CTR halved over two weeks." Name the biggest problem and the biggest
opportunity, give one recommendation with the number attached, and offer to
act. Applying a change belongs to `adplane-optimize`; do not do it here.

Keep it short: at most three examples per finding, and the whole review
under about 60 lines. If it is longer, it is repeating itself.

## When something moved sharply

Before blaming the algorithm, look for the boring cause. On Google, a
`change_event` report shows who changed what and when: `google_run_report`
with `resource: "change_event"`, fields such as
`change_event.change_date_time`, `change_event.change_resource_type`,
`change_event.changed_fields`, `change_event.user_email`, and an explicit
date range covering the last few days. On Meta, `meta_list_objects` shows
`effective_status`, which reflects the parent's state and any review
outcome; a review outcome is per object, so for a disapproved ad call it
with `object_type: "ad"` (narrowed by `campaign_id`), not the campaign.
Disapprovals do not show in the insights.

## Make it easier to look at, and recurring

If this host can publish an artifact and the review spans several campaigns
or both platforms, offer a one-page scorecard with a spend-versus-conversions
chart. If the user liked the review and the host can schedule work, offer a
weekly rerun. Weekly is the right default; daily only for accounts spending
enough to earn it. Each run uses the account's daily operation budget, so say
that before setting it up.
