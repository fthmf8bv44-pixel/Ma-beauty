#!/usr/bin/env python3
"""MA Beauty video toolkit (wraps ffmpeg).

  python3 tools/video.py info <video>...
      Duration, resolution, fps, rotation, audio for each file.
  python3 tools/video.py sheet <video> [out.jpg] [--every SECONDS]
      Contact sheet of frames (with timestamps) so Claude can SEE the footage.
  python3 tools/video.py frame <video> <seconds> <out.jpg>
      Grab one still (for covers, thumbnails, graphics).
  python3 tools/video.py edit <plan.json>
      Build a finished video from an edit plan (see tools/edit-plan.example.json).
"""
import json, os, subprocess, sys, tempfile, shutil

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{' '.join(cmd)}\n{r.stderr[-3000:]}")
    return r.stdout

def probe(path):
    out = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path])
    return json.loads(out)

def info(paths):
    for p in paths:
        d = probe(p)
        v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
        a = any(s["codec_type"] == "audio" for s in d["streams"])
        rot = 0
        if v:
            rot = int(v.get("tags", {}).get("rotate", 0) or 0)
            for sd in v.get("side_data_list", []) or []:
                if "rotation" in sd: rot = int(sd["rotation"])
        dur = float(d["format"].get("duration", 0))
        w, h = (v["width"], v["height"]) if v else (0, 0)
        if abs(rot) in (90, 270): w, h = h, w
        fps = v.get("avg_frame_rate", "0/1") if v else "-"
        try: n, dn = fps.split("/"); fps = round(int(n) / int(dn), 2)
        except Exception: pass
        print(f"{p}: {dur:.1f}s  {w}x{h} ({'vertical' if h > w else 'horizontal' if w > h else 'square'})  fps={fps}  audio={'yes' if a else 'no'}")

def sheet(path, out=None, every=None):
    dur = float(probe(path)["format"]["duration"])
    every = every or max(0.5, round(dur / 16, 2))
    out = out or os.path.splitext(path)[0] + "-sheet.jpg"
    vf = (f"fps=1/{every},scale=360:-2,"
          f"drawtext=text='%{{pts\\:hms}}':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6,"
          f"tile=4x4:padding=6:color=white")
    run(["ffmpeg", "-y", "-v", "error", "-i", path, "-vf", vf, "-frames:v", "1", "-q:v", "3", out])
    print(f"{out}  (one frame every {every}s, first 16 shown; use --every to change)")

def frame(path, t, out):
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", "-q:v", "2", out])
    print(out)

def atempo_chain(speed):
    parts, s = [], speed
    while s > 2.0: parts.append("atempo=2.0"); s /= 2.0
    while s < 0.5: parts.append("atempo=0.5"); s /= 0.5
    parts.append(f"atempo={s}")
    return ",".join(parts)

def edit(plan_path):
    plan = json.load(open(plan_path))
    base = os.path.dirname(os.path.abspath(plan_path))
    rp = lambda p: p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))
    W, H = plan.get("size", [1080, 1920])
    fps = plan.get("fps", 30)
    look = plan.get("look", "natural")  # natural | warm | none
    grade = {"natural": "eq=contrast=1.04:saturation=1.05",
             "warm": "eq=contrast=1.04:saturation=1.06,colorbalance=rs=0.03:bs=-0.03",
             "none": "null"}[look]
    tmp = tempfile.mkdtemp()

    # 1. Cut, reframe, grade and speed-adjust each clip to an identical format.
    parts = []
    for i, c in enumerate(plan["clips"]):
        src = rp(c["src"]); speed = float(c.get("speed", 1.0))
        has_audio = any(s["codec_type"] == "audio" for s in probe(src)["streams"])
        if c.get("fit", "fill") == "fill":  # crop to fill the frame
            fx = float(c.get("focus_x", 0.5)); fy = float(c.get("focus_y", 0.5))
            v = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                 f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})*{fy}")
        else:  # "fit": whole shot visible over a blurred copy of itself
            v = (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:2[bg];"
                 f"[b]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
        v += f",setsar=1,fps={fps},{grade},setpts=(PTS-STARTPTS)/{speed}"
        cmd = ["ffmpeg", "-y", "-v", "error", "-ss", str(c.get("start", 0))]
        if "end" in c: cmd += ["-to", str(c["end"])]
        cmd += ["-i", src]
        if not has_audio or c.get("mute"):
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                    "-filter_complex", f"[0:v]{v}[v]", "-map", "[v]", "-map", "1:a", "-shortest"]
        else:
            cmd += ["-filter_complex", f"[0:v]{v}[v];[0:a]aresample=48000,{atempo_chain(speed)}[a]",
                    "-map", "[v]", "-map", "[a]"]
        out = os.path.join(tmp, f"p{i:03d}.mp4")
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-ar", "48000", "-ac", "2", out]
        run(cmd); parts.append(out)

    # 2. Join the clips.
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(tmp, "joined.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])
    total = float(probe(joined)["format"]["duration"])

    # 3. Text/graphic overlays (transparent PNGs), music, loudness for social (-14 LUFS).
    out = rp(plan["output"]); os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", joined]
    vf, last_v, n = [], "[0:v]", 1
    for j, o in enumerate(plan.get("overlays", [])):
        cmd += ["-loop", "1", "-t", str(total), "-i", rp(o["image"])]
        st, en = float(o.get("start", 0)), float(o.get("end", total))
        vf.append(f"[{n}:v]format=rgba,fade=t=in:st={st}:d=0.2:alpha=1,"
                  f"fade=t=out:st={max(st, en - 0.2)}:d=0.2:alpha=1[o{j}]")
        vf.append(f"{last_v}[o{j}]overlay=0:0:enable='between(t,{st},{en})'[v{j}]")
        last_v = f"[v{j}]"; n += 1
    vf.append(f"{last_v}null[vout]")
    ov = float(plan.get("original_audio_volume", 1.0))
    music = plan.get("music")
    if music:
        cmd += ["-stream_loop", "-1", "-i", rp(music["src"])]
        mv = float(music.get("volume", 0.25))
        af = (f"[0:a]volume={ov}[oa];[{n}:a]volume={mv},atrim=0:{total},"
              f"afade=t=out:st={max(0, total - 1.5)}:d=1.5[ma];"
              f"[oa][ma]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[aout]")
    else:
        af = f"[0:a]volume={ov},loudnorm=I=-14:TP=-1.5[aout]"
    cmd += ["-filter_complex", ";".join(vf + [af]), "-map", "[vout]", "-map", "[aout]",
            "-t", str(total), "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
            "-r", str(fps), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out]
    run(cmd)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{out}  {total:.1f}s  {W}x{H}  {os.path.getsize(out) / 1e6:.1f} MB")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "info": info(a[1:])
    elif a[0] == "sheet":
        every = None
        if "--every" in a: i = a.index("--every"); every = float(a[i + 1]); a = a[:i] + a[i + 2:]
        sheet(a[1], a[2] if len(a) > 2 else None, every)
    elif a[0] == "frame": frame(a[1], a[2], a[3])
    elif a[0] == "edit": edit(a[1])
    else: sys.exit(__doc__)
