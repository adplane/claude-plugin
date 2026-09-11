---
name: adplane-optimize
argument-hint: "<optional: google, meta, or a campaign name>"
description: Find and cut wasted ad spend on Google Ads and Meta Ads, with search terms that never convert, negative keywords, budget pacing, pausing what does not work, and moving budget to what does. Use when the user asks about wasted spend, negatives, "which campaigns should I pause", "am I over budget", pacing, or reallocating budget, even when they don't say Adplane. Proposes each change with the numbers and applies it only after the user agrees to that specific change. Not for building new campaigns, use adplane-build-campaign.
---

# Cutting waste and pacing budget

Follow `adplane-agent` first, and the platform skill for field rules. This
skill proposes changes and applies them only after the user agrees to that
specific change. When invoked directly, $ARGUMENTS narrows the pass to a
platform or a campaign (default: every connected account on both platforms).

## Find the waste

**Google.** `google_run_report` on `search_term_view` ordered by cost, and
on `campaign` and `ad_group` for spend with zero conversions. The GAQL
cookbook in `adplane-google-ads` has a ready query for search terms with
spend and no conversions.

**Meta.** `meta_run_report` at `level: "adset"` and `level: "ad"` with the
conversion `action_types` the user cares about, plus `frequency` and `ctr`
for fatigue.

Waste has a few shapes and they need different fixes:

- **Spend with zero conversions.** Check volume first: an ad group with 40
  spent and no conversions may not have had a chance at a 60 CPA.
- **Spend converting far above target.** Worse than zero, because it looks
  like it is working.
- **Search terms you never meant to buy.** Broad match reaching "free",
  "jobs", "diy", competitor names, wrong locations, adjacent products.
- **Ad sets and ads nobody clicks any more.** Rising frequency, falling
  CTR.

## Before you cut anything

- **Check the tracking.** A campaign that looks like it converts nothing
  very often converts fine and reports nothing. Ask whether conversions are
  known to be tracked before pausing on that evidence alone.
- **Check the volume.** Ten clicks and no conversions is not evidence. As a
  rule of thumb, wait for about three times the target CPA in spend, or
  around 100 clicks, before calling something a loser.
- **Check the assist.** The campaign with no last-click conversions may be
  the one introducing people to the brand.

## Fix it, in this order

1. **Negatives before pauses.** `google_add_negative_keywords` is precise
   and reversible and keeps the campaign learning. Pausing an ad group to
   stop one bad search term is a blunt instrument. Choose the scope
   deliberately: campaign for a term that is wrong everywhere in that
   campaign, ad_group for a term that is only wrong there, an existing
   shared_list for a term that is wrong account-wide.
2. **Pause the narrowest thing** that solves the problem:
   `google_update_object` or `meta_update_object` with status PAUSED on
   the keyword, ad, ad set, ad group, or campaign. Never delete when
   pausing will do; deletes lose history and the delete tools only accept
   never-spent campaigns anyway.
3. **Reallocate** what you freed with `daily_budget` changes. Move money
   toward proven cost per conversion, not toward volume, and move in steps
   of 20 to 30 percent; a budget that doubles overnight re-enters learning
   and gets worse before it gets better.

Every proposal carries the arithmetic: "Move 30 a day from A (CPA 140,
target 50) to B (CPA 38). Same total. If B holds, about 17 more leads a
month: 900 moved buys 24 at B's CPA and gave up 6 at A's." Then wait for
the yes, apply one change, read it back, and report the stored values.

## Pacing

Compare spend so far against elapsed days in the period.

- **Underpacing** usually means the budget is capped, bids are too low,
  the target is set below what the account can do, or the audience is too
  narrow. On Google, check impression share lost to budget before raising
  the budget (query in the GAQL cookbook); if it is near zero, more money
  changes nothing.
- **Overpacing** means the month runs out early. Cut the daily budget or
  fix what is expensive; do not let it stop mid-month.
- Google may spend up to twice the daily budget on a given day and settles
  over the month. A single-day overspend is not a bug; say so before anyone
  panics.

## Then verify, and do not promise to watch

After every change, read the object back and tell the user what to expect:
a learning period, a dip, a delay before the data means anything.

Pacing drifts and CPAs creep. "I'll keep an eye on it" is a promise the
conversation cannot keep. If this host can schedule work, offer a
mid-month and month-end pacing check, or weekly for accounts where a day of
overspend is real money. Each run uses the account's daily operation
budget, so say so.
