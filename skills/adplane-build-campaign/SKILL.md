---
name: adplane-build-campaign
argument-hint: <platform and brief, e.g. "google, emergency plumber, Chicago, 50/day">
description: Build a new Google Ads Search campaign or Meta (Facebook and Instagram) campaign end to end, created paused so nothing spends until the user turns it on. Use when the user wants to create, set up, launch, scaffold, or draft a campaign, ad group, ad set, ad, creative, headlines, or keywords on either platform, even when they don't say Adplane. Covers the order of calls, the Meta readiness check, image and video upload, and the ad preview. Not for reporting or optimising existing campaigns, use adplane-account-review or adplane-optimize.
---

# Building a campaign

Follow `adplane-agent` first. Load `adplane-google-ads` or
`adplane-meta-ads` for the platform's field rules. Everything below is
created **paused**; the user turns it on, not you. When invoked directly,
$ARGUMENTS is the brief: platform, what is being advertised, where, and the
daily budget.

## Before you build anything

Establish four things, or you will build the wrong campaign competently:

1. **The objective in business terms**: leads, sales, calls, installs.
2. **What a conversion is worth**, so a budget and a target make sense.
3. **The budget, daily and monthly.** Say the monthly number out loud.
4. **The landing page URL**, and whether conversion tracking exists on it.

Then check what is already there (`google_run_report` on campaigns, or
`meta_list_objects`) so you do not build a duplicate.

Publish the plan before you create anything, as an artifact if this host
has them, otherwise as a short table: structure, daily and monthly spend,
targeting, the copy, and what is still missing. It is far easier to catch
"wrong landing page" on a page than in a paragraph. Get a yes on the plan.

## Google Ads Search, in order

1. `google_create_campaign`: name, `daily_budget` in the account currency,
   `bidding_strategy` (MAXIMIZE_CLICKS by default; MAXIMIZE_CONVERSIONS with
   an optional `target_cpa`; MAXIMIZE_CONVERSION_VALUE with an optional
   `target_roas`; MANUAL_CPC), and `locations` as two-letter country codes.
   **If you omit locations, Google targets the whole world**; confirm
   targeting with the user before anything is enabled. Search only; no
   other campaign type is supported here.
2. `google_create_ad_group`: one per theme, optional `cpc_bid`.
3. `google_add_keywords`: up to 100 per call, each
   `{text, match_type, cpc_bid?}` with EXACT, PHRASE, or BROAD. Keywords are
   created paused even inside a paused ad group.
4. `google_create_ad`: a responsive search ad with 3 to 15 headlines of up
   to 30 characters, 2 to 4 descriptions of up to 90, an absolute
   `final_url`, optional `path1`/`path2`. Google mixes headlines
   independently, so each must stand alone; vary the angle (offer, speed,
   proof, price, outcome) rather than repeating one idea. The response
   includes policy approval status; name any policy topics it reports.
5. Read it back with `google_run_report` and confirm budget, status, and
   targeting match the plan.

Do not set a target CPA or ROAS on a campaign with no conversion history;
it has nothing to learn from. Start with clicks, then move to a target.

## Meta, in order

1. `meta_check_readiness` on the account. Payment method, accepted terms,
   Pages, pixel, spend cap, connection expiry. Fix `action_needed` items
   with the user before building; they otherwise fail mid-build.
2. `meta_get_schema` for objectives, optimization goals, billing events,
   bid strategies, statuses, and call-to-action types. Use only values it
   returns.
3. `meta_create_campaign`: `objective` (cannot be changed later, confirm
   it), `special_ad_categories` (NONE unless credit, employment, housing,
   social issues or politics, gambling, or financial products; ask, never
   guess). Leave budgets off the campaign so they live on the ad sets,
   which is the more predictable setup.
4. `meta_create_ad_set`: `daily_budget`, `optimization_goal`,
   `billing_event`, and `targeting` with at least `geo_locations`, for
   example `{"geo_locations": {"countries": ["US"]}, "age_min": 25}`. For
   interests or behaviours, get IDs from `meta_search_targeting` first;
   never from memory. For OFFSITE_CONVERSIONS pass `promoted_object` with
   the pixel and event. Testing three audiences means one campaign with
   three ad sets, not three campaigns.
5. Media: `meta_upload_image` from a public image URL returns an
   `image_hash`; `meta_upload_video` returns a `video_id` that may still be
   processing, so wait for its status before using it.
6. `meta_create_ad_creative`: `page_id` from the top-level `pages` list in
   `meta_list_accounts` (every Page there is usable), `message` (the body),
   `headline`, `link`, and the media. Put the point in the first 125
   characters of the body; that is what people see before "more".
7. `meta_create_ad` attaches the creative to the ad set.
8. `meta_get_preview` for the creative or ad and show the user how it
   renders. The preview link expires within minutes.
9. Read it back with `meta_list_objects`.

## After the build

Say plainly what exists, that it is **paused**, the daily and implied
monthly spend, and what remains before it should go live (tracking, a second
ad, a location check). Then ask whether to enable it. Enabling is
`google_update_object` with status ENABLED or `meta_update_object` with
status ACTIVE, and it is the user's decision, never yours.

If the build fails halfway, say exactly what exists and what does not. A
campaign with an ad group and no ad is not "created". Either finish it or,
if the user asks, remove the never-spent scaffold with
`google_remove_campaign` or `meta_delete_object`, and tell them which you
did.
