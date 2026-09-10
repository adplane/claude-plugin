---
description: Scaffold a paused Google Ads Search or Meta campaign from a short brief
argument-hint: <platform and brief, e.g. "google, emergency plumber, Chicago, 50/day">
---
Build a paused campaign for $ARGUMENTS, following the `adplane-build-campaign` skill and the platform skill for field rules.

1. Establish the objective, what a conversion is worth, the daily budget (say the monthly number too), and the landing page URL. Ask for anything missing.
2. Resolve the account with `google_list_accounts` or `meta_list_accounts`, and check for an existing campaign that already does this.
3. Show the plan before creating anything: structure, daily and monthly spend, targeting, the copy, and what is still missing. Get a yes.
4. Google: `google_create_campaign` with explicit `locations`, then `google_create_ad_group`, `google_add_keywords`, `google_create_ad`. Meta: `meta_check_readiness`, `meta_get_schema`, then `meta_create_campaign`, `meta_create_ad_set`, media upload, `meta_create_ad_creative`, `meta_create_ad`, `meta_get_preview`.
5. Read the result back and report the stored values. Say plainly that everything is paused, what it will spend per day and per month once enabled, and what remains before it should go live.
6. Ask whether to enable it. Do not enable it yourself; enabling is `google_update_object` with status ENABLED or `meta_update_object` with status ACTIVE, and only on an explicit yes.
