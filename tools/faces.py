#!/usr/bin/env python3
"""Face-aware photo placement for MA Beauty designs.

  python3 tools/faces.py <photo>      -> prints the faces found (x, y, w, h in pixels)

In code:  from faces import place
  css = place(photo_path, box_w, box_h, target_y=0.45)
  returns CSS (background-size + background-position) that scales the photo to cover the box
  and puts the faces' centre at target_y of the box height (0.5 = exact middle; a bit higher,
  e.g. 0.42-0.45, when a logo or headline sits below) and centred horizontally.
Needs: pip install opencv-python-headless
"""
import sys, cv2

import json, os
_cascades = None
FOCUS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand", "photos", "focus.json")

def _iou(a, b):
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    ix = max(0, min(ax + aw, bx + bw) - max(ax, bx)); iy = max(0, min(ay + ah, by + bh) - max(ay, by))
    inter = ix * iy
    return inter / float(aw * ah + bw * bh - inter)

def faces(path):
    """Faces as (x, y, w, h). A manual entry in brand/photos/focus.json (checked by eye) wins."""
    global _cascades
    img = cv2.imread(path); h, w = img.shape[:2]
    try:
        manual = json.load(open(FOCUS_FILE)).get(os.path.basename(path))
    except FileNotFoundError:
        manual = None
    if manual:
        return [tuple(f) for f in manual], (w, h)
    if _cascades is None:
        names = ["haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml", "haarcascade_profileface.xml"]
        _cascades = [cv2.CascadeClassifier(cv2.data.haarcascades + n) for n in names]
    scale = 1600 / max(w, h) if max(w, h) > 1600 else 1.0
    small = cv2.resize(img, (int(w * scale), int(h * scale))) if scale != 1 else img
    gray = cv2.equalizeHist(cv2.cvtColor(small, cv2.COLOR_BGR2GRAY))
    min_side = int(min(small.shape[:2]) * 0.05)
    hits = []
    for c in _cascades:
        for flip in (False, True):
            g = cv2.flip(gray, 1) if flip else gray
            for (x, y, fw, fh) in c.detectMultiScale(g, 1.08, 6, minSize=(min_side, min_side)):
                if flip: x = g.shape[1] - x - fw
                hits.append((x, y, fw, fh))
    # keep detections confirmed by at least 2 detector passes
    out = []
    for a in hits:
        votes = sum(1 for b in hits if _iou(a, b) > 0.3)
        if votes >= 2 and not any(_iou(a, o) > 0.3 for o in out):
            out.append(a)
    out = [tuple(int(v / scale) for v in f) for f in out]
    if out:
        biggest = max(f[2] for f in out)
        out = [f for f in out if f[2] >= 0.35 * biggest]
    return out, (w, h)

def place(path, bw, bh, target_y=0.45, target_x=0.5, face_size=None):
    """face_size: optional zoom so the face group's height is this fraction of the box height."""
    found, (iw, ih) = faces(path)
    s = max(bw / iw, bh / ih)
    if face_size and found:
        fh = max(f[1] + f[3] for f in found) - min(f[1] for f in found)
        s = max(s, face_size * bh / fh)
    if found:
        x0 = min(f[0] for f in found); x1 = max(f[0] + f[2] for f in found)
        y0 = min(f[1] for f in found); y1 = max(f[1] + f[3] for f in found)
        fx, fy = (x0 + x1) / 2, (y0 + y1) / 2
    else:
        fx, fy = iw / 2, ih / 2
    ox = min(0, max(bw - iw * s, target_x * bw - fx * s))
    oy = min(0, max(bh - ih * s, target_y * bh - fy * s))
    return f"background-size:{iw*s:.0f}px {ih*s:.0f}px;background-position:{ox:.0f}px {oy:.0f}px;"

if __name__ == "__main__":
    for p in sys.argv[1:]:
        f, size = faces(p); print(p, size, f)

def place_xy(path, bw, bh, target_y=0.45, target_x=0.5, face_size=None):
    """Numbers version of place(): (scaled_w, scaled_h, crop_x, crop_y, face_fx, face_fy) where
    crop_x/y is the top-left of the bw x bh crop in the scaled image and face_fx/fy is the
    face-group centre as a fraction of the crop (useful for zooming towards the face)."""
    found, (iw, ih) = faces(path)
    s = max(bw / iw, bh / ih)
    if face_size and found:
        fh = max(f[1] + f[3] for f in found) - min(f[1] for f in found)
        s = max(s, face_size * bh / fh)
    if found:
        x0 = min(f[0] for f in found); x1 = max(f[0] + f[2] for f in found)
        y0 = min(f[1] for f in found); y1 = max(f[1] + f[3] for f in found)
        fx, fy = (x0 + x1) / 2, (y0 + y1) / 2
    else:
        fx, fy = iw / 2, ih / 2
    ox = min(0, max(bw - iw * s, target_x * bw - fx * s))
    oy = min(0, max(bh - ih * s, target_y * bh - fy * s))
    return (round(iw * s), round(ih * s), round(-ox), round(-oy),
            (fx * s + ox) / bw, (fy * s + oy) / bh)
