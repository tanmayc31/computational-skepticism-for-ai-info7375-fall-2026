# COMMANDS.md — every command run to build this reel

Source material for `BUILD-PROMPT.md`. Paths are written relative to the two roots:

```bash
TOOLKIT="$HOME/Desktop/ST-Computational-Skepticism/Final Project Film/brutalist.art"
REEL="$HOME/Desktop/ST-Computational-Skepticism/Final Project Film/youtube/show-tell-veracite-pitch"
```

The reel lives OUTSIDE the toolkit, per CLAUDE.md rule 3 ("videos travel with their book,
never into the toolkit folder").

---

## 0. Readiness

```bash
cd "$TOOLKIT"
./setup                       # readiness table; everything READY except Manim equation beats
                              # (no LaTeX/dvisvgm) — not needed, this film has no MathTex
./art remotion-version        # reports BEHIND 4.0.535 vs 4.0.538 — advisory, deliberately not upgraded
```

## 0b. REQUIRED build-environment patch (one line, local clone only)

GATE T §8.1 blocks the master without this. `ClaudeDefinitions` renders its meaning column
at 48 design px, which produces a 40 px x-height run at 4K/scale=2 against a 41 px floor —
the cluster "swe" in the word "answers". Apply to the local clone; **do not commit or push.**

```bash
cd "$TOOLKIT"
python3 - <<'PY'
p = "runtime/remotion/src/scenes/ClaudeDefinitions.tsx"
s = open(p).read()
old = "  const meanSize = 48;   // \u2265 48: a lowercase run's x-height must clear GATE T's 41px floor at 4K"
new = ("  // GATE T \u00a78.1 (2026-10-24): at 48 a PURE x-height run \u2014 'swe' in \"answers\" \u2014 measures\n"
       "  // exactly 40px at 4K/scale=2, one pixel under the 41px floor, so any definitions card\n"
       "  // whose meaning text has three consecutive x-height letters fails the gate. 52 gives ~43px.\n"
       "  const meanSize = 52;")
assert old in s
open(p, "w").write(s.replace(old, new, 1))
PY
git -C "$TOOLKIT" diff --stat          # expect: 1 file changed, 4 insertions(+), 1 deletion(-)
git -C "$TOOLKIT" log --oneline -1     # expect: a99b5323 — unchanged, nothing committed
```

Revert when finished (optional):

```bash
git -C "$TOOLKIT" checkout -- runtime/remotion/src/scenes/ClaudeDefinitions.tsx
```

Verify the fix on the rendered clip BEFORE paying for a full recompile:

```bash
cd "$TOOLKIT" && python3 runtime/scripts/remotion_scenes.py "$REEL" --only BDEFS --force
cd "$TOOLKIT/runtime/scripts" && python3 - <<'PY'
import sys; sys.path.insert(0, ".")
import type_check as tc, numpy as np
from pathlib import Path
img = tc.extract_frame(Path("<REEL>")/"media"/"BDEFS.mp4")
arr = np.array(img); mask = tc.visible_text_mask(arr, "light"); lab, n = tc.labeled_blobs(mask)
runs = tc.text_run_bboxes(tc.blob_bboxes(lab, n), img.height)
print("floor", int(img.height*tc.MIN_SIZE_PCT/100), "smallest run", min(r[3]-r[1] for r in runs))
PY
```

## 1. Scaffold + paperwork (Gate F refuses to render without the paperwork set)

```bash
mkdir -p "$REEL"
# written by hand into $REEL:
#   SOURCES.md     S1-S5, every claim's origin
#   FACTCHECK.md   38 rows: # | Beat | Claim | Verdict | Source | Fix
#   SHOTLIST.md    the cast, per-beat drawing + motion + labels, deviations from SKILL.md
#   PROMPTS.md     "no generation prompts" — nothing paid, nothing generated
#   make_sheet.py  the beat sheet generator
```

## 2. Beat sheet

```bash
cd "$REEL" && python3 make_sheet.py
# -> 17 beats · 611 words · beat_sheet.json
```

## 3. Audio = the master clock

```bash
cd "$TOOLKIT"
# pronunciation pre-check BEFORE spending 2.5 min on a full voice run:
python3 runtime/scripts/generate_audio_kokoro.py --phonemize "Ford F-150"
python3 runtime/scripts/generate_audio_kokoro.py --phonemize "RAGAS"      # etc.

python3 runtime/scripts/generate_audio_kokoro.py "$REEL"                  # 17 beats, 2m20s, $0.00
python3 runtime/scripts/generate_audio_kokoro.py "$REEL" --only BOUT      # after the name respell
```

Whisper verification of every beat (catches what `--phonemize` cannot):

```python
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe("mp3/beat-BOUT.mp3", beam_size=5)
print(" ".join(x.text for x in segs))
```

Pad the declared silences BY HAND — nothing in `runtime/` reads `lead_silence_s` /
`tail_silence_s` (verified: `grep -rn "tail_silence" runtime/` returns nothing):

```bash
cd "$REEL"
ffmpeg -y -f lavfi -t 0.8 -i anullsrc=r=24000:cl=mono -i mp3/beat-BIDEA.mp3 \
       -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" -b:a 128k mp3/_pad.mp3 && mv mp3/_pad.mp3 mp3/beat-BIDEA.mp3
ffmpeg -y -i mp3/beat-BOUT.mp3 -f lavfi -t 1.0 -i anullsrc=r=24000:cl=mono \
       -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" -b:a 128k mp3/_pad.mp3 && mv mp3/_pad.mp3 mp3/beat-BOUT.mp3
# then ffprobe each mp3 and write actual_duration_s + audio_file back into beat_sheet.json
```

**AUDIO LOCK: 203.12 s = 3:23.** Never re-run `make_sheet.py` after this — it wipes the
measured durations.

## 4. Draw

```bash
cd "$REEL"
cp "$TOOLKIT/skills/make/show-tell/templates/iso_kit.py" _kit.py
cat _kit.py _body.py > scenes.py && rm _kit.py _body.py   # PASTE the kit, never import it
```

## 5. Pre-flight (free, seconds — run this before every render)

Gate A must run from a scratch folder holding **only** `scenes.py`, because that is exactly
what `art run` copies into its sandbox:

```bash
SCR=$(mktemp -d); cp "$REEL/scenes.py" "$SCR/"
for C in B00_WrongPage B01_NoCheck ... BOUT_Title; do
  (cd "$SCR" && python3 "$TOOLKIT/runtime/qc/static_scene_check.py" scenes.py --class "$C")
done

cd "$REEL"
for C in ...; do python3 "$TOOLKIT/runtime/qc/manim_layout_audit.py" scenes.py --class "$C" --curve-strict; done
```

## 6. LOOK at frames before rendering (this caught 6 faults no gate did)

```bash
cd "$REEL"
for C in ...; do manim -ql -s --media_dir /tmp/stills/m -o "$C" scenes.py "$C"; done
# then tile the PNGs into one contact sheet with PIL and actually look at it
```

## 7. Render

```bash
cd "$TOOLKIT"
./art run "$REEL"            # Gates F/L/A/W, Manim 4K, remotion_scenes.py, compile, Gate V
```

Note: `--height 1080` does nothing useful. `run.sh` only parses the flag when it is the FIRST
argument, and line 205 renders Manim at a hard-coded `-qk -r 3840,2160` regardless.

Check every clip against its audio (a clip longer than its audio is silently centre-cut):

```bash
cd "$REEL" && for f in manim/*.mp4; do ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"; done
```

After editing a scene, move the old clip AND the stale cache aside or it will not re-render:

```bash
mkdir -p _superseded && mv manim/B03.mp4 manim/B07.mp4 _superseded/
mv media/videos _superseded/videos-$(date +%H%M%S)
```

## 8. Master

```bash
cd "$TOOLKIT"
./art final "$REEL" --height 2160 --out "$REEL/exports/landscape"
```

## 9. Checks run outside `art run`

```bash
python3 "$TOOLKIT/runtime/qc/factcheck_check.py" "$REEL"
python3 "$TOOLKIT/runtime/scripts/bookend_check.py" "$REEL"   # expected FAIL — see GATE-BOOKEND.md
```

## Never run

`./art post` — staging/publishing. Not used, not needed, explicitly out of scope.
