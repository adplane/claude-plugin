# Adplane plugin for Claude

Google Ads and Meta Ads (Facebook, Instagram) in one plugin. Pull reports,
find wasted spend, add negative keywords, and build paused campaigns from
chat, on your own ad accounts.

The plugin bundles the Adplane remote MCP connector (`https://mcp.adplane.ai`)
with seven skills that teach Claude how a performance marketer works the
accounts. Claude loads them on its own when the conversation calls for
them, and the three workflow skills can also be run directly from the "/"
menu with an argument. It runs in Claude web and desktop chat, Claude
Cowork, and Claude Code.

## Install

- **Claude web, desktop, or Cowork:** Customize > Plugins > Browse plugins,
  search "Adplane", click Add, then sign in when the connector opens.
- **Claude Code:**

  ```
  /plugin marketplace add adplane/claude-plugin
  /plugin install adplane@adplane
  ```

  then `/mcp`, pick `adplane`, and authenticate.

Sign-in is with Google and creates your Adplane account if you do not have
one. Google then asks separately for Google Ads access; if you skip that
step, connect Google Ads later at
[adplane.ai/accounts](https://adplane.ai/accounts), which is also where
Meta is connected.

## What it does

| Skill | Use it for |
|---|---|
| `adplane-account-review` | How the ads are doing: spend, conversions, cost per result, ROAS, versus the previous period |
| `adplane-agent` | The ground rules: created paused, money needs a yes, read back after every write, never invent a number |
| `adplane-build-campaign` | A Google Search or Meta campaign end to end, created paused |
| `adplane-google-ads` | Reports, raw GAQL, search terms, negatives, bids, campaign settings |
| `adplane-meta-ads` | Ad sets, targeting search, creatives, previews, insights, readiness |
| `adplane-optimize` | Wasted spend, negatives, pacing, moving budget to what works |
| `adplane-start` | Connecting, and what to do when an account is not showing |

Run directly: `/adplane-account-review [period]`,
`/adplane-optimize [platform or campaign]`, `/adplane-build-campaign <brief>`.
In Claude Code these carry the plugin prefix, for example
`/adplane:adplane-account-review last 7 days`.

## Example prompts

- "How did my Google Ads do last week compared to the week before?"
- "Find search terms that spent money and never converted, and propose
  negatives."
- "Why is my Facebook cost per lead climbing?"
- "Set up a paused Search campaign for emergency plumbing in Chicago at 50
  a day."

## Safety

- Everything the write tools create starts **paused**. Nothing spends until
  you explicitly turn it on, and only `google_update_object` and
  `meta_update_object` can do that.
- Every write returns the platform's own stored view, and Claude reports
  that rather than what it asked for.
- Deletes are limited to campaigns that have never spent, and only when you
  ask. Everything else is paused or archived.
- Where your Claude client lets you allow tools individually, read tools
  are safe to allow always; keep write tools on per-call confirmation.

## Data and privacy

- **No hooks, no telemetry.** The plugin is skills and one connector
  reference. The only network destination is Adplane's own server,
  reached through the MCP connection you authorise.
- Ad spend is billed by Google and Meta to your own accounts.
- Privacy policy: https://adplane.ai/privacy. Terms: https://adplane.ai/terms.
- Support: support@adplane.ai.

## Development

```
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
claude plugin validate skills --strict
python3 scripts/lint.py
```

(`claude plugin validate .` stops at the marketplace manifest, so run the
three targets separately.)

`scripts/lint.py` checks frontmatter, skill size, the URL allowlist, that
no skill text carries em-dashes, prices, plan names, or upsell wording, and
that every `google_*` / `meta_*` name mentioned in a skill or
reference exists in `scripts/tool-names.txt`. `tests/prompt-catalog.md`
lists natural prompts with the skill expected to fire for each; check it by
hand in Claude before a release.

Documentation: https://adplane.ai/docs
