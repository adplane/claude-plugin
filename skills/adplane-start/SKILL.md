---
name: adplane-start
description: Connect Adplane and confirm which Google Ads and Meta Ads accounts are reachable, then start on the first real task. Use when Adplane is not connected yet, when the user says "connect my ad accounts", "set up adplane", "which ad accounts do you see", "my Google Ads account isn't showing", or when google_list_accounts or meta_list_accounts returns no accounts or a connection error. Relays the tool's notice as written and routes on the result. Not for reporting or building, use the other adplane skills once connected.
---

# Getting connected

Follow `adplane-agent` for everything after this. The goal here is one
thing: get from "not connected" or "no accounts" to a resolved account ID
and the first real task, with as few words as possible.

## Step 1: is Adplane connected?

Call `ping`. If it succeeds, go to step 2.

If the Adplane tools are missing or the connection fails, the user needs to
connect Adplane in this host:

- **Claude web or desktop chat, and Cowork:** the plugin bundles the
  connector. When the Adplane tools are absent, ask the user to open the
  plugin's connector in their Claude settings and sign in; the sign-in
  creates their Adplane account if they do not have one. Do not give
  terminal commands to someone in a chat app.
- **Claude Code:** run `/mcp`, find the `adplane` server, and authenticate.

Sign-in is with Google. It also connects the Google Ads accounts that login
can access. Meta is connected afterwards at https://adplane.ai/accounts by
signing in with Facebook.

## Step 2: which accounts are reachable?

Call `google_list_accounts` and `meta_list_accounts` in parallel. If no
`meta_*` tools appear in the tool list, Meta is not enabled for this
account; Google is the full surface, say so once, and never mention it
again. Route on the shape of the result:

- **Accounts on both platforms.** Name them briefly with currency and
  time zone, ask which one to work on if more than one fits the request,
  and hand off to the task they came with. Do not list capabilities, do not
  offer a menu.
- **Google accounts but no Meta accounts.** Continue with Google. Mention
  once that Meta can be connected at https://adplane.ai/accounts, then only
  if they ask about Facebook or Instagram.
- **An empty list with a `notice`.** Relay the notice as written. It names
  the login that was checked and what it found (for example a Google login
  with no Ads access, an account hidden on the accounts page, or a lapsed
  Meta connection) and says what the user can do. Do not paraphrase it into
  "you have no accounts", and do not try other IDs.
- **The account the user named is not listed.** They add or unhide it at
  https://adplane.ai/accounts. Accounts unchecked there are hidden from
  every tool on purpose.

## Step 3: hand off

Say what the first useful thing is, given what they asked for, and do it:

- "how are my ads doing" → `adplane-account-review`
- "cut wasted spend", "negatives", "pacing" → `adplane-optimize`
- "create a campaign" → `adplane-build-campaign`

## Facts to state when relevant, not as a lecture

- Everything created through Adplane starts paused; nothing spends until
  the user explicitly turns it on.
- Read tools are safe to allow always; write tools deserve per-call
  confirmation in the host's permission settings.
- Ad spend is billed by Google and Meta to the user's own accounts.
- Meta connections lapse after about 60 days and are renewed at
  https://adplane.ai/accounts; `meta_list_accounts` reports the expiry.

## Troubleshooting

- **Nothing works at all**, `ping` included: disconnect and reconnect the
  Adplane connector in the host and complete sign-in again.
- **Google works, Meta fails**: reconnect Meta at
  https://adplane.ai/accounts.
- **A tool reports the daily operation limit**: relay its message as
  written; the limit belongs to the current plan.
- Anything else: https://adplane.ai/docs, or support@adplane.ai.
