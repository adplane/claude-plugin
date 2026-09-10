---
description: Find ad spend that is not converting and propose negatives or pauses, applied only on a yes
argument-hint: "<optional: google, meta, or a campaign name>"
---
Run a wasted-spend pass on $ARGUMENTS (default: every connected account on both platforms), following the `adplane-optimize` skill.

1. Resolve accounts with `google_list_accounts` and `meta_list_accounts`. Only continue on platforms that came back connected.
2. Google: `google_run_report` on `search_term_view` for the last 30 days ordered by cost, and on `campaign` and `ad_group` for spend with zero conversions. Use the search-terms query from the GAQL cookbook in `adplane-google-ads` if the report tool is not enough.
3. Meta: `meta_run_report` at `level: "adset"` and `level: "ad"` for the last 30 days with spend, the relevant conversion `action_types`, `frequency`, and `ctr`.
4. Before proposing a cut, check volume (about three times the target CPA in spend, or around 100 clicks) and ask whether conversion tracking is known to work.
5. Present the top sources of waste with the amounts, then the proposals in order: negative keywords first (with scope), then the narrowest pause, then any budget move, each with the arithmetic and the expected effect.
6. Apply only the changes the user says yes to, one at a time: `google_add_negative_keywords`, `google_update_object`, or `meta_update_object`. Read each back and report the stored values. Never delete.
