---
name: adplane-google-ads
description: Google Ads specifics through Adplane, with reports and raw GAQL, search terms, negative keywords, keyword and bid changes, and campaign settings. Use for anything on Google Ads, AdWords, PPC, Search campaigns, Performance Max, search term reports, quality score, impression share, change history, or GAQL, even when the user doesn't say Adplane. Covers customer IDs, currency handling, the report schema, and the one tool that can make a Google object start spending. Not for Meta or Facebook, use adplane-meta-ads.
---

# Google Ads through Adplane

Follow `adplane-agent` first. Account IDs come from `google_list_accounts`
as `customer_id`; never guess one. All money is in the account's currency,
already converted from micros: a cost of 5.0 is five units, and a
`metrics.cost_micros` field comes back as a `cost` column.

## Reading

**`google_run_report`** is the default. Arguments: `customer_id`,
`resource`, `fields`, `date_range`, optional `filters`, `order_by`, `limit`,
`cursor`.

- `date_range`: a preset such as `LAST_7_DAYS`, `LAST_30_DAYS`, or an
  explicit `2026-06-01..2026-06-30`. The response echoes the dates used;
  state them.
- `filters`: a list of `{field, op, value}` with op one of eq, neq, gt,
  gte, lt, lte, contains, not_contains, in, not_in. Match enums such as
  status with eq or in, not contains.
- `order_by`: `{field, direction}`; the field must be in `fields`.
- `limit` sizes a page; `totals` cover every matched row. Pass the returned
  `cursor` for the next page.
- **Call `google_get_report_schema` before using any field you have not
  already used successfully in this conversation.** Unknown fields are rejected.

Resources worth knowing: `campaign`, `ad_group`, `keyword_view`,
`search_term_view`, `ad_group_ad`, `customer`, `geographic_view`,
`campaign_budget`, `change_event`; for Performance Max, `asset_group`,
`campaign_search_term_insight`, `performance_max_placement_view`.

**`google_run_gaql`** runs a raw SELECT when the report tool lacks what you
need (nested objects, `old_resource`/`new_resource` on change events,
repeated fields such as RSA headlines). It is read-only by construction.
Always include an explicit date bound and a `LIMIT` of at most 10000. See
`references/gaql-cookbook.md` in this skill's folder for queries checked
against the connector's field catalog; if you cannot open it, build the
query from `google_get_report_schema`.

Data reflects the account's time zone and may lag about three hours.

## Search terms and negatives

The search term report is where money leaks: `google_run_report` on
`search_term_view` with `search_term_view.search_term`,
`segments.search_term_match_type`, `metrics.cost_micros`,
`metrics.clicks`, `metrics.conversions`, ordered by cost. Look for
"free", "jobs", "diy", competitor names, wrong locations, and adjacent
products.

Add negatives with `google_add_negative_keywords`: up to 100 items of
`{scope, scope_id, text, match_type}`, scope campaign, ad_group, or
shared_list (an existing list; this tool does not create lists). Negatives
only restrict where ads show and can never spend. The batch is atomic and
each item is one operation against the daily budget. Report the stored
values the response reads back.

## Changing things

**`google_update_object`** is the only tool that can make anything spend
(status ENABLED). By `object_type`:

- `campaign`: name, status, daily_budget, bidding_strategy, target_cpa,
  target_roas
- `ad_group`: name, status, cpc_bid
- `ad`: status only
- `keyword`: status, cpc_bid

Notes the tool enforces: a campaign on a shared budget refuses
`daily_budget`; a campaign on a portfolio bidding strategy refuses strategy
and target changes; changing strategy or targets on a serving campaign
restarts the learning phase, so say so; a target of 0 clears it. For ads
and keywords, `object_id` can be the composite `adGroupId~id` form shown in
report resource names. There is no REMOVED status here; this tool cannot
delete.

Pausing is reversible and is almost always what "stop this" means.

## Building

`google_create_campaign` (Search only, paused, omit `locations` and Google
targets everywhere), `google_create_ad_group`, `google_add_keywords`,
`google_create_ad`. The full order and the copy rules are in
`adplane-build-campaign`.

## Removing

`google_remove_campaign` permanently removes one campaign that has never
spent, only when the user explicitly asks; Google has no undo. Campaigns
only. If the campaign has ever spent, the tool refuses and tells you to
pause instead. Confirm the campaign by name and ID before calling it.

## Budgets and quotas

Every call is one or more operations against a daily budget on the user's
current plan. Reports are cached for a short window, so an identical query
repeated is free. If a tool reports the limit, relay its message as
written; do not estimate what remains.
