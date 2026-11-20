# Start here: your MA Beauty marketing agent

You have a small marketing team that lives in this project:

| Team member | What they do |
|---|---|
| Graphic designer | Makes Instagram, Facebook, TikTok and ad graphics as ready-to-post PNG images |
| Ads manager | Plans Meta (Facebook + Instagram) and TikTok ads: who to target, budget, ad text, step-by-step setup |
| Social media manager | Weekly post plans, captions, hashtags, reel and TikTok scripts, replies to reviews |
| Video editor | Turns your footage into Reels, TikToks, Stories and video ads, and tells you where to post each |
| Marketing strategist | Tells you the few things most worth doing to get more local clients |

You don't need to call them by name. Just say what you want and Claude picks the right one.

## How to use it (every time)
1. Go to **claude.ai/code** (or the Claude app → Code).
2. Start a new session and pick the **Ma-beauty** repository.
3. Type a shortcut or just ask in plain English.

### Shortcuts
| Type this | You get |
|---|---|
| `/weekly-content` | Next week's posts, captions, hashtags, reel shot lists and graphics |
| `/weekly-content push HiFu` | Same, focused on one service |
| `/new-ad-campaign Glass Skin facial $15/day Meta` | A full ad plan with click-by-click setup steps and ad images |
| `/make-graphic story: Saturday appointments available` | One graphic |
| `/edit-video` (with videos attached) | Finished vertical videos, plus where to post, caption, hashtags and ad copy |
| `/monthly-review` | Tells you what to screenshot, then explains your results and what to change |
| `/marketing-advice how do I fill quiet Tuesdays?` | Practical advice |

Plain requests work too: *"How do partnership ads work?"*, *"Reply to this Google review: …"*, *"Write a TikTok script about HiFu aftercare"*.

### Sending videos
1. Tap the **paperclip / +** in the message box and choose your clips. A few at a time is best.
2. Add a line about them, e.g. *"/edit-video body treatment session, want a reel and an ad"*.
3. Claude watches the footage frame by frame, suggests edit ideas, edits, and sends the finished
   videos back for you to save to your phone. It can't hear audio, so if you talk to camera,
   tell it roughly what you say.
4. Add a trending sound inside Instagram/TikTok when you post. That helps reach.

Videos aren't kept between sessions (they're too big to save in the project), so save finished
videos to your phone straight away.

### Getting your finished work
Claude saves everything in the project (graphics are in `marketing/graphics/`). At the end of a
session, ask **"save and push my work"** so it's kept for next time. To download an image to your
phone, ask Claude to **send you the file**.

## Safety: what Claude will and won't do
- It **never** posts, publishes or spends money for you. You stay in control. You copy the text and images into
  Instagram, Meta Ads Manager or TikTok yourself.
- It follows Meta/TikTok rules for cosmetic treatments: 18+ targeting, no before/after photos in ads,
  no guaranteed results.

## One-time setup checklist
- [ ] **1. Check your business facts.** Open `business/profile.md`. Anything marked [CONFIRM] came
      from Fresha and may be out of date. Tell Claude the corrections (e.g. *"HiFu Jaw Line is now
      $320, and we're open Wed–Fri 10–6"*) and it will update the file.
- [ ] **2. Brand.** Send Claude your logo and tell it your brand colours (or approve the starter
      look in `brand/brand-guide.md`).
- [ ] **3. Photos.** Upload 10–20 real photos (clinic, you at work, treatment close-ups) so graphics
      look like *your* clinic.
- [ ] **4. Meta ads payment and pixel.** In Meta Business Suite → Settings, make sure your ad account
      has a payment method. Claude will walk you through the first campaign step by step.
- [ ] **5. TikTok (optional, later).** Create a TikTok Business account and start reposting your reels.
- [ ] **6. Google Business Profile.** Ask `/marketing-advice optimise my Google Business Profile`.
      This is often the biggest free win for local clinics.
