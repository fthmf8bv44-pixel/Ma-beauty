#!/usr/bin/env python3
"""Builds the HTML for the Christmas Thuzzle campaign graphics, then renders PNGs.
Run from the repo root:  python3 marketing/graphics/2026-11-christmas-thuzzle/build.py
Edit text here, re-run, and every size updates."""
import os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../tools"))
from faces import place
PHOTOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../brand/photos/website")
def bg(photo, bw, bh, ty=0.45, face_size=None):
    """CSS that fills a bw x bh box with the photo, faces centred (ty = height fraction)."""
    return f"background-image:url({P}/{photo});background-repeat:no-repeat;" + place(os.path.join(PHOTOS, photo), bw, bh, ty, face_size=face_size)

HERE = os.path.dirname(os.path.abspath(__file__))
B = "../../../brand"           # brand folder, relative to this folder
P = f"{B}/photos/website"
HEAD = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{B}/templates/ma.css"><style>{{css}}</style></head><body>{{body}}</body></html>'

def page(name, w, h, css, body):
    path = os.path.join(HERE, f"{name}.html")
    open(path, "w").write(HEAD.replace("{css}", css).replace("{body}", body))
    return path, w, h

designs = []
FEED, STORY = (1080, 1350), (1080, 1920)

# ---------- AD 1: "Few Melbourne clinics have Thuzzle. We do." ----------
THUZZLE_PHOTO = None   # set to a file in brand/photos/ once there's a real Thuzzle photo
def ad_thuzzle(split):
    def f(w, h):
        tall = h > 1500
        ph = int(h * (0.54 if tall else 0.55))          # photo area height
        pad_b = 330 if tall else 40
        if split:
            half = w // 2
            right = (bg(THUZZLE_PHOTO, half, ph) if THUZZLE_PHOTO else "background:#cfc9c9")
            photos = f"""<div class="ph" style="left:0;width:{half}px;{bg('mira-portrait-logo.jpg', half, ph, 0.45, 0.26)}"></div>
            <div class="ph" style="left:{half}px;width:{w-half}px;{right}">{'' if THUZZLE_PHOTO else '<div class="ph-note">Thuzzle treatment photo<br>goes here</div>'}</div>"""
        else:
            photos = f"""<div class="ph" style="left:0;width:{w}px;{bg('mira-portrait-logo.jpg', w, ph, 0.45)}"></div>"""
        css = f"""
        .ph{{position:absolute;top:0;height:{ph}px}}
        .ph-note{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;font:500 26px Montserrat,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:#6b6262}}
        .bot{{position:absolute;left:0;bottom:0;width:100%;height:{h-ph}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 80px {pad_b}px}}
        h1{{font-size:{84 if tall else 78}px;line-height:1.04;margin:20px 0 24px}}
        .sub{{font-size:{30 if tall else 28}px;line-height:1.5;opacity:.93;max-width:880px}}
        .from{{margin-top:26px;font-size:21px}}
        """
        body = f"""{photos}
        <div class="bot ox">
          <div class="label">Thuzzle · Caulfield South</div>
          <h1 class="serif">Few Melbourne clinics<br>have Thuzzle. We do.</h1>
          <div class="sub">Italian-engineered radiofrequency.<br>Targets stubborn fat. Tightens skin.<br>No needles. No downtime.</div>
          <div class="label from">From $159 · Hawthorn Rd</div>
        </div>"""
        return css, body
    return f

# ---------- AD 2: Thuzzle price menu on oxblood ----------
def ad_menu(w, h):
    tall = h > 1500
    css = f"""
    body{{background:var(--ox);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:{'center' if tall else 'flex-start'};text-align:center;padding:{0 if tall else 110}px 110px {120 if tall else 0}px}}
    .logo{{width:{150 if tall else 128}px;opacity:.95}}
    .label{{margin-top:{60 if tall else 44}px}}
    h1{{font-size:{100 if tall else 92}px;line-height:1.02;margin:20px 0 {56 if tall else 40}px}}
    .row{{display:flex;justify-content:space-between;width:100%;max-width:740px;font-size:{36 if tall else 33}px;padding:{22 if tall else 17}px 0;border-bottom:1px solid rgba(255,255,255,.28)}}
    .row b{{font-weight:400}}
    .group{{font-family:Montserrat,sans-serif;font-size:19px;letter-spacing:.3em;text-transform:uppercase;opacity:.7;width:100%;max-width:740px;text-align:left;margin-top:{40 if tall else 30}px}}
    .note{{margin-top:{48 if tall else 36}px;font-size:26px;line-height:1.5;opacity:.88}}
    """
    rows = lambda items: "".join(f'<div class="row"><span>{a}</span><b>{b}</b></div>' for a, b in items)
    body = f"""<img class="logo" src="{B}/logo-white.png">
    <div class="label">Before Christmas</div>
    <h1 class="serif">Thuzzle body<br>contouring</h1>
    <div class="group">Body · 15–30 min per area</div>
    {rows([("Tummy tightening","$279"),("Love handles","$299"),("Double chin","$159")])}
    <div class="group">Face</div>
    {rows([("Full face lift &amp; tighten","$249")])}
    <div class="note">Targets stubborn fat. Tightens skin.<br>No needles. No downtime.<br>Body consult $22, taken off your treatment.</div>"""
    return css, body

# ---------- AD 3 / posts: review card on soft grey ----------
def review(quote, who, src, treatment="", size=64):
    def f(w, h):
        tall = h > 1500
        css = f"""
        body{{background:var(--grey);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 110px}}
        .logo{{width:132px;position:absolute;top:{290 if tall else 90}px;left:50%;transform:translateX(-50%)}}
        .mark{{font-family:Branch,Georgia,serif;font-size:200px;line-height:.6;color:var(--ox);height:90px}}
        blockquote{{font-family:Branch,Georgia,serif;font-size:{size + (6 if tall else 0)}px;line-height:1.2;color:var(--ox);margin-top:10px}}
        .who{{margin-top:48px;font-family:Montserrat,sans-serif;font-size:21px;letter-spacing:.3em;text-transform:uppercase;color:var(--ox)}}
        .t{{margin-top:12px;font-size:24px;color:var(--text)}}
        .foot{{position:absolute;bottom:{430 if tall else 90}px;left:0;right:0;text-align:center;font-size:24px;color:var(--text)}}
        .stars{{color:var(--ox);letter-spacing:.2em;font-size:26px;margin-right:12px}}
        """
        body = f"""<img class="logo" src="{B}/logo-black.png">
        <div class="mark">“</div>
        <blockquote>{quote}</blockquote>
        <div class="who">{who} · {src}</div>
        {f'<div class="t">{treatment}</div>' if treatment else ''}
        <div class="foot"><span class="stars">★★★★★</span>5.0 from 529 reviews on Fresha</div>"""
        return css, body
    return f

# ---------- AD 4: Christmas gift cards ----------
def ad_gift(w, h):
    tall = h > 1500
    split = 0.55 if not tall else 0.54
    css = f"""
    .top{{position:absolute;left:0;top:0;width:100%;height:{int(h*split)}px;{bg('gold-mask-headband.jpg', w, int(h*split), 0.5)}}}
    .bot{{position:absolute;left:0;bottom:0;width:100%;height:{h-int(h*split)}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 100px {330 if tall else 0}px}}
    h1{{font-size:{92 if tall else 84}px;line-height:1.06;margin:24px 0 28px}}
    .sub{{font-size:30px;line-height:1.5;opacity:.92}}
    .outline{{margin-top:40px}}
    """
    body = f"""<div class="top photo"></div>
    <div class="bot ox">
      <div class="label">Christmas gift cards</div>
      <h1 class="serif">Give them an hour<br>with Mira</h1>
      <div class="sub">Thuzzle, facials, brows and more.<br>Buy online in a minute.</div>
      <div class="outline">Link in bio</div>
    </div>"""
    return css, body

# ---------- CAROUSEL: What is Thuzzle? ----------
def car1(w, h):
    css = f"""
    .top{{position:absolute;left:0;top:0;width:{w}px;height:{int(h*0.66)}px;{bg('mira-portrait-logo.jpg', w, int(h*0.66), 0.45)}}}
    .bot{{position:absolute;left:0;right:0;bottom:0;height:34%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
    h1{{font-size:112px;line-height:1;margin-top:18px}}
    .swipe{{margin-top:26px;font-size:24px;opacity:.8}}"""
    body = """<div class="top photo"></div><div class="bot ox"><div class="label">Our most asked question</div>
    <h1 class="serif">What is Thuzzle?</h1><div class="swipe">Mira explains →</div></div>"""
    return css, body

def text_slide(label, title, html_body, n, bg="ox"):
    def f(w, h):
        css = f"""
        body{{display:flex;flex-direction:column;justify-content:center;padding:0 110px}}
        h2{{font-size:80px;line-height:1.06;margin:22px 0 40px}}
        .b{{font-size:34px;line-height:1.55}}
        .b li{{list-style:none;padding:16px 0;border-bottom:1px solid {'rgba(255,255,255,.25)' if bg=='ox' else 'rgba(55,12,14,.18)'}}}
        .n{{position:absolute;bottom:70px;right:90px;font-family:Montserrat,sans-serif;font-size:20px;letter-spacing:.3em;opacity:.6}}
        .logo{{position:absolute;bottom:58px;left:100px;width:84px;opacity:.9}}
        """
        logo = f"{B}/logo-white.png" if bg == "ox" else f"{B}/logo-black.png"
        body = f"""<div class="label">{label}</div><h2 class="serif">{title}</h2><div class="b">{html_body}</div>
        <img class="logo" src="{logo}"><div class="n">{n} / 5</div>"""
        return css.replace("body{", f"body{{background:{'var(--ox);color:#fff' if bg=='ox' else 'var(--grey);color:var(--ox)'};"), body
    return f

# ---------- STORY: December bookings ----------
def story_dec(w, h):
    css = f"""
    .top{{position:absolute;inset:0 0 52% 0;background-image:url({P}/clinic-reception.jpg);background-position:50% 50%}}
    .bot{{position:absolute;left:0;right:0;bottom:0;height:52%;display:flex;flex-direction:column;align-items:center;text-align:center;padding:110px 100px 0}}
    h1{{font-size:96px;line-height:1.04;margin:22px 0 34px}}
    .hrs{{font-size:30px;line-height:1.7;opacity:.92}}
    .outline{{margin-top:44px}}"""
    body = """<div class="top photo"></div><div class="bot ox"><div class="label">December at MA Beauty</div>
    <h1 class="serif">Christmas bookings<br>are open</h1>
    <div class="hrs">Tuesday to Saturday from 10am<br>Thursday until 6:30pm</div>
    <div class="outline">Book via link in bio</div></div>"""
    return css, body

designs = [
    ("ad1-thuzzle-mira-feed", *FEED, ad_thuzzle(False)), ("ad1-thuzzle-mira-story", *STORY, ad_thuzzle(False)),
    ("ad1b-thuzzle-split-PREVIEW-feed", *FEED, ad_thuzzle(True)), ("ad1b-thuzzle-split-PREVIEW-story", *STORY, ad_thuzzle(True)),
    ("ad2-thuzzle-menu-feed", *FEED, ad_menu), ("ad2-thuzzle-menu-story", *STORY, ad_menu),
    ("ad3-review-rachael-feed", *FEED, review("I place a lot of trust in Mira’s expertise and advice, and am getting great results.", "Rachael K.", "Fresha", "", 66)),
    ("ad3-review-rachael-story", *STORY, review("I place a lot of trust in Mira’s expertise and advice, and am getting great results.", "Rachael K.", "Fresha", "", 66)),
    ("ad4-gift-cards-feed", *FEED, ad_gift), ("ad4-gift-cards-story", *STORY, ad_gift),
    ("post-carousel-thuzzle-01", *FEED, car1),
    ("post-carousel-thuzzle-02", *FEED, text_slide("How it works", "Radiofrequency, at more than one depth",
        "Thuzzle warms the targeted fat layer and tightens the skin above it, in the same treatment. It also supports lymphatic drainage.", 2)),
    ("post-carousel-thuzzle-03", *FEED, text_slide("Where we use it", "Body and face",
        "<ul><li>Tummy, love handles, back</li><li>Thighs, knees, buttocks, arms</li><li>Double chin</li><li>Face, neck and décolletage</li></ul>", 3, "grey")),
    ("post-carousel-thuzzle-04", *FEED, text_slide("What to expect", "In and out in your lunch break",
        "<ul><li>15–30 minutes per body area</li><li>No downtime, so straight back to your day</li><li>A course of treatments gives the best results</li><li>Results vary from person to person</li></ul>", 4)),
    ("post-carousel-thuzzle-05", *FEED, text_slide("Start here", "Book a body consult with Mira",
        "Mira will look at your goals and tell you honestly if Thuzzle is right for you.<br><br>$22 for 30 minutes, taken off your treatment.<br>Tummy $279 · Love handles $299 · Double chin $159", 5, "grey")),
    ("post-review-eveline", *FEED, review("Mira is amazing, very passionate and professional. Great personalised skin treatment!", "Eveline T.", "Fresha", "Thuzzle Full Face Lift &amp; Tighten", 70)),
    ("post-review-tara", *FEED, review("Mira is a wonderful practitioner. She has state of the art equipment and treats every client with the best care…", "Tara S.", "Google", "", 60)),
    ("post-review-natalie", *FEED, review("Mira has been looking after my skin for years. I get compliments how fresh and young my skin looks.", "Natalie M.", "Fresha", "", 62)),
    ("story-december-bookings", *STORY, story_dec),
]

if __name__ == "__main__":
    import sys
    only = sys.argv[1:]
    for name, w, h, fn in designs:
        if only and not any(o in name for o in only): continue
        css, body = fn(w, h)
        path, _, _ = page(name, w, h, css, body)
        out = os.path.join(HERE, "png", f"{name}.png"); os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run(["node", os.path.join(HERE, "../../../tools/render.js"), path, str(w), str(h), out], check=True, capture_output=True)
        print(out)
