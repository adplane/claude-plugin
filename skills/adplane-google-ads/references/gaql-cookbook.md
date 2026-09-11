# GAQL cookbook for `google_run_gaql`

Every query is a SELECT with a LIMIT, and every query that reads metrics
or change events carries an explicit date bound (change events require
both, with a LIMIT of at most 10000). Money fields ending in `_micros`
come back converted to the account currency with the suffix removed. Replace `<start>` and `<end>` with
`YYYY-MM-DD` dates. Prefer `google_run_report` unless the query needs
something below.

## Campaigns by cost, last 30 days

```
SELECT campaign.id, campaign.name, campaign.status,
       campaign_budget.amount_micros, metrics.cost_micros,
       metrics.clicks, metrics.conversions, metrics.conversions_value
FROM campaign
WHERE segments.date BETWEEN '<start>' AND '<end>'
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
LIMIT 200
```

## Search terms with spend and no conversions

```
SELECT search_term_view.search_term, segments.search_term_match_type,
       campaign.name, ad_group.name,
       metrics.cost_micros, metrics.clicks, metrics.conversions
FROM search_term_view
WHERE segments.date BETWEEN '<start>' AND '<end>'
  AND metrics.conversions = 0
  AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC
LIMIT 500
```

## Keywords with quality score

```
SELECT ad_group.name, ad_group_criterion.keyword.text,
       ad_group_criterion.keyword.match_type,
       ad_group_criterion.quality_info.quality_score,
       metrics.impressions, metrics.clicks, metrics.cost_micros,
       metrics.conversions
FROM keyword_view
WHERE segments.date BETWEEN '<start>' AND '<end>'
ORDER BY metrics.cost_micros DESC
LIMIT 500
```

## Impression share (is the campaign budget-limited?)

```
SELECT campaign.name, metrics.search_impression_share,
       metrics.search_budget_lost_impression_share,
       metrics.search_rank_lost_impression_share, metrics.cost_micros
FROM campaign
WHERE segments.date BETWEEN '<start>' AND '<end>'
  AND campaign.status = 'ENABLED'
LIMIT 200
```

If `search_budget_lost_impression_share` is near zero, more budget changes
nothing; the constraint is rank, not money.

## Responsive search ad headlines (repeated fields)

```
SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status,
       ad_group_ad.policy_summary.approval_status,
       ad_group_ad.ad.responsive_search_ad.headlines,
       ad_group_ad.ad.responsive_search_ad.descriptions
FROM ad_group_ad
WHERE ad_group_ad.status != 'REMOVED'
LIMIT 200
```

`headlines` is a list of objects each carrying `text`.

## Change history: who changed what

```
SELECT change_event.change_date_time, change_event.user_email,
       change_event.change_resource_type,
       change_event.resource_change_operation,
       change_event.changed_fields,
       change_event.old_resource, change_event.new_resource
FROM change_event
WHERE change_event.change_date_time >= '<start> 00:00:00'
  AND change_event.change_date_time <= '<end> 23:59:59'
ORDER BY change_event.change_date_time DESC
LIMIT 100
```

`changed_fields` is a list of paths; `old_resource` and `new_resource`
contain only the changed branch, for example
`{"campaign": {"status": "PAUSED"}}`. Google keeps change events for about
30 days, and the query must carry both a date bound and a LIMIT or it is
refused.

## Performance Max search categories and placements

`search_term_view` does not cover Performance Max. PMax search terms live
on `campaign_search_term_insight`, which requires a filter on ONE campaign
id on every query, reports no cost, and works in two steps. Step 1, the
categories for a campaign:

```
SELECT campaign_search_term_insight.id,
       campaign_search_term_insight.category_label,
       metrics.clicks, metrics.impressions, metrics.conversions
FROM campaign_search_term_insight
WHERE campaign_search_term_insight.campaign_id = <pmax campaign id>
  AND segments.date BETWEEN '<start>' AND '<end>'
LIMIT 500
```

Step 2, the terms inside one category (the id filter and the paired
segments are both required):

```
SELECT segments.search_term, segments.search_subcategory,
       metrics.clicks, metrics.impressions, metrics.conversions
FROM campaign_search_term_insight
WHERE campaign_search_term_insight.campaign_id = <pmax campaign id>
  AND campaign_search_term_insight.id = <category id from step 1>
  AND segments.date BETWEEN '<start>' AND '<end>'
LIMIT 500
```

Placements are account-wide, not broken out by campaign:

```
SELECT performance_max_placement_view.display_name,
       performance_max_placement_view.placement_type,
       performance_max_placement_view.target_url,
       metrics.impressions
FROM performance_max_placement_view
WHERE segments.date BETWEEN '<start>' AND '<end>'
LIMIT 500
```
