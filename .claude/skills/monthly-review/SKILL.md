---
name: monthly-review
description: Analyse MA Beauty's marketing results (Meta/TikTok ads, Instagram insights, Fresha bookings) and recommend what to change next month.
argument-hint: "[paste numbers or attach screenshots]"
---

Review MA Beauty's marketing performance. Data provided: $ARGUMENTS

1. If no data was provided, tell the owner exactly what to export and where to click:
   - Meta Ads Manager → Campaigns → set the date range to last month → columns: Amount spent,
     Reach, Impressions, Link clicks, CTR (link), CPC (link), Results, Cost per result → screenshot.
   - Instagram app → Profile → Professional dashboard → Insights → last 30 days → screenshot
     Accounts reached, Accounts engaged, Followers, and Top content.
   - Fresha → Reports → bookings and new clients for the month (and how clients heard about you,
     if recorded).
   Then stop and wait for the data.
2. With data, use the **ads-manager** agent (paid) and **social-media-manager** agent (organic) to
   analyse it. Explain in plain English: what worked, what didn't, and cost per booking.
3. Use the **marketing-strategist** agent to give the top 3 actions for next month.
4. Save to `marketing/reports/YYYY-MM.md` and add a row to the results log in
   `business/marketing-plan.md`.
