---
name: adplane-meta-ads
description: Meta Ads specifics through Adplane, with Facebook and Instagram campaigns, ad sets, creatives, targeting search, insights reports, previews, and account readiness. Use for anything on Meta, Facebook, Instagram, FB ads, ad sets, audiences, interests, pixels, creatives, or Advantage+, even when the user doesn't say Adplane. Covers account and Page selection, the readiness check, budget and enum rules from meta_get_schema, and the one tool that can make a Meta object start spending. Not for Google Ads, use adplane-google-ads.
---

# Meta Ads through Adplane

Follow `adplane-agent` first. Account IDs come from `meta_list_accounts`
as `account_id`; never guess one. Money is in the account's currency: 50
means 50.00, never cents.

## Accounts, Pages, and expiry

`meta_list_accounts` returns the ad accounts, a top-level `pages` list, and
the connection expiry. **Every Page in the top-level list is usable as a
creative's `page_id`**; `promotable_page_ids` on an account is a narrower
promote-flow hint, not a gate. Meta connections lapse after about 60 days;
when the expiry is close, say so and point at https://adplane.ai/accounts
to reconnect. An empty accounts list carries a `notice`; relay it as
written.

## Enums come from the schema

**Call `meta_get_schema` before using any field or enum value you have not
already used successfully in this conversation.** It returns insight levels,
report fields, breakdowns, and the exact values for objectives,
special ad categories, optimization goals, billing events, bid strategies,
statuses, call-to-action types, and object types. Values it does not list
are rejected.

## Reading

**`meta_run_report`**: `account_id`, `level` (account, campaign, adset,
ad), `fields`, `date_range` (a preset such as `LAST_30_DAYS` or an explicit
`2026-06-01..2026-06-30`; the response echoes the dates), optional
`action_types`, `breakdowns`, `filters`, `time_increment`, `limit`,
`cursor`.

- `action_types` such as `["lead"]` or `["purchase"]` pull that conversion's
  count and cost into their own columns. Ask which event matters.
- Rates (`ctr`, `cpc`, `frequency`) are per row; only additive metrics
  (impressions, clicks, spend) total meaningfully.
- Filters are Meta's shape, `{field, operator, value}`, with operators such
  as EQUAL, CONTAIN, IN, GREATER_THAN, and dotted fields such as
  `campaign.name` or `adset.id`. Not the Google shape.
- `time_increment` gives a daily or weekly series for trend questions.

**`meta_list_objects`** is the structural view: `object_type` is
`campaign`, `adset`, `ad`, or `adcreative`, optionally narrowed by
`campaign_id` or `adset_id`. Read `effective_status` when asking why
something is not delivering: it reflects the parent's state and any review
outcome, while `status` is only the object's own setting.

## Fatigue

Rising `frequency` with falling `ctr` over two or three weeks is creative
fatigue. No budget change fixes it; a fatigued ad set with more budget
annoys the same people faster. New creative first, then a new format, then
a broader audience, then budget. Change one variable at a time.

## Changing things

**`meta_update_object`** is the only tool that can make anything spend
(status ACTIVE). `object_type` campaign, adset, or ad; fields name, status,
daily_budget, lifetime_budget, bid_amount. PAUSED stops delivery and is
reversible; ARCHIVED hides it and is how you retire something. Report the
stored values the response reads back.

## Building

The order is in `adplane-build-campaign`. Rules specific to Meta:

- `meta_check_readiness` first on any account you have not built on in
  this conversation.
- Objective is fixed at creation; `special_ad_categories` is required
  (NONE unless credit, employment, housing, social issues or politics,
  gambling, or financial products; ask, never guess).
- Prefer budgets on ad sets, not the campaign. A campaign budget turns on
  campaign budget optimisation and its ad sets must then carry none.
- `targeting` needs at least `geo_locations`. Interests, behaviours, and
  job titles come from `meta_search_targeting` only; each result's `type`
  names its key under `flexible_spec`, for example
  `{"flexible_spec": [{"interests": [{"id": "...", "name": "..."}]}]}`.
  Prefer specific mid-sized entries over the broadest match.
- OFFSITE_CONVERSIONS needs `promoted_object` with `pixel_id` and
  `custom_event_type`.
- Times are ISO 8601 with an offset, `2026-08-01T09:00:00-0700`.
- Media: `meta_upload_image` (public image URL, returns `image_hash`) and
  `meta_upload_video` (public video URL, returns `video_id`; wait while it
  processes). A video creative also needs a thumbnail image.
- Body text: the hard limit is long, but readers see about 125 characters
  before "more". Lead with the offer.
- `meta_get_preview` renders the creative or ad in a placement; the link
  expires within minutes, so use it to check, not to share.

## Deleting

`meta_delete_object` permanently deletes one campaign that has never spent,
only when the user explicitly asks. Everything else is archived with
`meta_update_object`. If the campaign has ever spent, the tool refuses and
tells you to archive instead.

## Personal data

Lead forms and customer lists are real people. Summarise, never paste them
into the conversation unprompted.
