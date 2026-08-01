"""
Lay the narration onto a video.

Lines are spoken end to end with a fixed breath between them, which is how a person actually
reads. Nothing is time-stretched and no line is trimmed to fit a picture. The render scripts
are pinned to THIS schedule, not the other way round, so if a line changes, reprint the
schedule and move the visuals.

Audio is reused from measured/ when present, so re-muxing costs no API credits.
"""
import json, os, subprocess, sys
from lines import SETS
from tts import synth

OUT = os.path.dirname(os.path.abspath(__file__))
AU = os.path.join(OUT, "measured")
GAP = 0.42          # breath between lines
LEAD = 0.30         # silence before the first word

TARGETS = {
    "v1": "quantica-01-percent",
    "v2": "quantica-02-pizza",
    "v3": "quantica-03-regions",
    "v4": "quantica-04-avgspeed",
    "v5": "quantica-05-repeating",
    "v6": "quantica-06-pemdas",
    "v7": "quantica-07-cube",
    "v8": "quantica-08-squares",
    "v9": "quantica-09-down20up20",
    "v10": "quantica-10-paycut",
}


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())


def schedule(key):
    """(start, wav, duration) per line, generating any audio that is missing."""
    os.makedirs(AU, exist_ok=True)
    out, t = [], LEAD
    for i, txt in enumerate(SETS[key]):
        w = os.path.join(AU, f"{key}_{i:02d}.wav")
        if not os.path.exists(w):
            synth(txt, w)
        d = dur(w)
        out.append((t, w, d))
        t += d+GAP
    return out


def build(key, show=True):
    stem = TARGETS[key]
    src = os.path.join(OUT, stem+".mp4")
    dst = os.path.join(OUT, stem+"-voiced.mp4")
    sch = schedule(key)
    vlen = dur(src)
    if show:
        print(f"  {stem}   video {vlen:.1f}s")
        for i, (st, _, d) in enumerate(sch):
            print(f"    L{i:<2} {st:5.2f} -> {st+d:5.2f}   {SETS[key][i][:56]}")
        end = sch[-1][0]+sch[-1][2]
        pad = vlen-end
        verdict = "ok" if pad >= 0.5 else ("TIGHT" if pad >= 0 else "NARRATION OVERRUNS THE VIDEO")
        print(f"    narration ends {end:.2f}s, video is {vlen:.1f}s, tail {pad:+.2f}s  [{verdict}]")

    ins, filt = [], []
    for i, (st, w, _) in enumerate(sch):
        ins += ["-i", w]
        filt.append(f"[{i+1}:a]adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(sch)))
    filt.append(f"{mix}amix=inputs={len(sch)}:normalize=0:dropout_transition=0[m]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, *ins,
                    "-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[m]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", dst], check=True)
    print(f"    wrote {os.path.basename(dst)}")

    with open(os.path.join(OUT, stem+"-voiceover.txt"), "w") as f:
        f.write(f"{stem}\nnarration, in order, with the second each line starts\n\n")
        for i, (st, _, _) in enumerate(sch):
            f.write(f"{st:6.2f}   {SETS[key][i]}\n")


if __name__ == "__main__":
    for k in (sys.argv[1:] or list(TARGETS)):
        build(k)
