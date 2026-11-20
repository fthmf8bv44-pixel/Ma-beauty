#!/usr/bin/env python3
"""On-brand text overlays for MA Beauty videos (transparent 1080x1920 PNGs).

  python3 tools/overlay.py <out.png> <style> "<text>" ["<small text>"]

Styles (all kept inside the Reels safe zone, y 300-1450):
  hook   big serif (Branch) headline, upper third, for the first 1-2 seconds
  line   medium sans line, lower-middle, for supporting points
  linetop same as line but in the upper third (use when a face is in the lower half)
  linemid same as line but mid-frame (use when faces are top AND bottom)
  end    full oxblood end card: logo, serif headline, small label (opaque)
Use <br> in text for line breaks.
"""
import os, sys, subprocess, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def make(out, style, text, small=""):
    out = os.path.abspath(out)
    d = os.path.dirname(out); os.makedirs(d, exist_ok=True)
    rel = lambda p: os.path.relpath(os.path.join(ROOT, p), d)
    shadow = "text-shadow:0 2px 18px rgba(0,0,0,.55),0 1px 3px rgba(0,0,0,.5)"
    if style == "hook":
        css = ".t{position:absolute;left:70px;top:320px;max-width:860px;display:inline-block;background:rgba(55,12,14,.9);color:#fff;font-family:Branch,Georgia,serif;font-size:92px;line-height:1.06;padding:34px 44px 40px;border-radius:6px}.s{margin-top:18px;font-family:Montserrat,sans-serif;font-size:24px;letter-spacing:.3em;text-transform:uppercase}"
    elif style == "line":
        css = ".t{position:absolute;left:70px;top:1150px;max-width:860px;display:inline-block;background:rgba(55,12,14,.9);color:#fff;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:400;font-size:54px;line-height:1.2;padding:26px 36px 30px;border-radius:6px}.s{margin-top:12px;font-family:Montserrat,sans-serif;font-size:22px;letter-spacing:.3em;text-transform:uppercase}"
    elif style == "linetop":
        css = ".t{position:absolute;left:70px;top:320px;max-width:860px;display:inline-block;background:rgba(55,12,14,.9);color:#fff;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:400;font-size:54px;line-height:1.2;padding:26px 36px 30px;border-radius:6px}.s{margin-top:12px;font-family:Montserrat,sans-serif;font-size:22px;letter-spacing:.3em;text-transform:uppercase}"
    elif style == "linemid":
        css = ".t{position:absolute;left:70px;top:820px;max-width:860px;display:inline-block;background:rgba(55,12,14,.9);color:#fff;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:400;font-size:54px;line-height:1.2;padding:26px 36px 30px;border-radius:6px}"
    elif style == "end":
        css = f"body{{background:var(--ox)!important}}.wrap{{position:absolute;inset:0 0 260px 0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#fff;padding:0 100px}}.logo{{width:240px;margin-bottom:70px}}.t{{font-family:Branch,Georgia,serif;font-size:130px;line-height:1.02}}.s{{margin-top:46px;font-family:Montserrat,sans-serif;font-size:28px;letter-spacing:.3em;text-transform:uppercase;opacity:.9}}"
    else:
        sys.exit("style must be hook, line, linetop, linemid or end")
    small_html = f'<div class="s">{small}</div>' if small else ""
    if style == "end":
        body = f'<div class="wrap"><img class="logo" src="{rel("brand/logo-white.png")}"><div class="t">{text}</div>{small_html}</div>'
    else:
        body = f'<div class="t">{text}{small_html}</div>'
    page = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{rel("brand/templates/ma.css")}"><style>html,body{{background:transparent}}{css}</style></head><body>{body}</body></html>'
    h = out[:-4] + ".html"; open(h, "w").write(page)
    args = ["node", os.path.join(ROOT, "tools/render.js"), h, "1080", "1920", out]
    if style != "end": args.append("--transparent")
    subprocess.run(args, check=True, capture_output=True)
    return out

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 3: sys.exit(__doc__)
    print(make(a[0], a[1], a[2], a[3] if len(a) > 3 else ""))
