# BUILD-PROMPT — how this film was built

The film was built by Claude Code running inside the Brutalist toolkit (commit `a99b5323`), following its `show-tell` skill, from my script (`NARRATION-DRAFT.md`) and brief (`PROJECT-BRIEF.md`). Below are the prompts I gave it, in order, then the command spine. The full command list with context is in `paperwork/COMMANDS.md`.

## Prompt 1 — the build

~~~
I need to build a 2-4 minute pitch film tonight with this toolkit, using the show-tell skill. Deadline is 11:59pm, so work efficiently.

FIRST read: CLAUDE.md, HOW-TO.md, skills/make/show-tell/SKILL.md, and the worked show-tell example it names. Then read my two files: ../NARRATION-DRAFT.md (the script, one row per beat) and ../PROJECT-BRIEF.md (context).

HARD RULES (these override the skill where they conflict):
1. Narrate as me, Tanmay, first person. NO "Liam", NO "in for Bear", NO Nik Bear Brown name, persona, handle or credit line anywhere (voice, screen, outro, metadata). BIDEA greeting is "Hello. I'm Tanmay..." exactly as in my script. BOUT says only "Veracite. Tanmay Chandan."
2. Use my narration text VERBATIM. Do not add, remove or change any claim. If a line must change for Kokoro pronunciation or timing, tell me the exact change and why before applying it.
3. Free local pipeline only: Kokoro voice (am_onyx is fine), Manim, Remotion. No Higgsfield, no API keys, no paid generation. Never publish, never run art post.
4. Honesty labels on screen: B03 must show "RideReady survey, n=7". Anything that does not exist yet must not be drawn as finished; if a beat shows a mock-up, label it "constructed" on screen.
5. If a toolkit gate or bookend check fails because of rule 1 (persona/outro change), do not undo my rule. Record it and continue.

DELIVERABLES: create the reel, write SOURCES.md, FACTCHECK.md, SHOTLIST.md, PROMPTS.md as the skill requires. Sources for facts: my RideReady git commit 5d6e68e ("scoped retrieval by vehicle"), my RideReady evaluation report (0.547 Camry chunk, 0.25 floor; "trusted the citations" 3.71/5, lowest of six, n=7), and my Veracite design document. RAGAS/ALCE descriptions are from their public documentation.

SPEED PLAN: audio first, then low-res stills contact sheet for me to look at, then render. Do a review render at 1080p first if the gates allow it; only go to 4K if time allows. Tell me rough render times before starting a long render.

LOG: keep a running file ../build-log.md with a timestamp and one line for every problem you hit and how you fixed it (I will use it for my FRICTIONAL.md).

At the end, copy into ../final-project-film/: the final .mp4, beat_sheet.json, all gate reports, and the paperwork files. Then give me the exact commands you ran, so I can write BUILD-PROMPT.md.

Start by telling me your plan in 5 lines and the reel folder path you will use. Then begin.
~~~

## Decisions I gave during the build (answers to its check-ins)

- **Name pronunciation (BOUT):** approved a TTS-only respelling of my surname ("Chundan") so the voice says it correctly; on-screen text stays "Tanmay Chandan".
- **"Veracite" / "ALCE":** kept as Kokoro says them.
- **GATE T failure in a shared component:** approved a one-line edit in my local clone only, with: *"Do not commit or push to the upstream repo. Record the exact one-line diff in build-log.md and SOURCES.md, and include it in the rebuild commands."*

## Prompt 2 — fix the log timestamps

~~~
Problem: build-log.md has timestamps that are in the future. The real clock is 19:16 EDT and the file was last saved at 19:11, but the log has entries at 19:13 through 20:57. Do not guess times. Rebuild every timestamp from real evidence: run `date` for now, and use `ls -lT` / `stat` on the actual files each step produced (clips, gate reports, audio, logs) to date each entry. Where no file proves a time, mark it "~approx" or "time unknown". Add a top note: "Timestamps corrected on <date> from file modification times; earlier version contained estimated times, some in the future." From now on, run `date` before writing any log line.
~~~

## Prompt 3 — fixes after I watched the first master

~~~
I watched the master. Please fix these, then re-run all gates, re-render the master, and re-run deliver.sh.

1. B09 narration change (approved by me, rule 2): replace B09's narration with exactly:
"In scope: it runs locally, on recorded traces. Out of scope, on purpose: it will not plug into a live production system, and it will never rewrite or block an answer. First: a test where the Camry case returns mismatch, and the same case without vehicle metadata returns unknown, never match."
Re-voice only B09 (--only B09), whisper-check it, update actual_duration_s, re-pace the B09 scene. Also update ../NARRATION-DRAFT.md to match.

2. B09 layout: the "local" label sits on top of the box. Move it beside the box with the 0.3-unit gap.

3. B12 (exists / will exist, ~2:55): boxes overlap the folder icon. Space them so nothing overlaps.

4. Sweep every beat: pull the midpoint and last frame of every clip and check for ANY label sitting on top of an icon or object (I saw text over folder icons in some frames). Fix every overlap you find and list which beats you changed.

5. Reminder: fix the future timestamps in build-log.md from real file modification times, as I asked earlier, and add the correction note at the top.

Tell me the render-time estimate before starting.

6. B11 (Have / New, ~2:49): the narration names three NEW skills: "splitting claims", "LLM judges", "measuring a verifier's own error". Only one box appears on the New side. Make it three boxes, each one appearing (fully opaque, landing before the clip midpoint where possible) as its phrase is spoken, using until() on each phrase. Same for the Have side: one box for "RAG pipelines in Python" and the git branch line for "my RideReady repo and its git history". Keep labels 1-3 words, beside the boxes, not on them. Re-check Gate A, layout audit, Gate V and GATE T for B11 after the change.
~~~

## Prompt 4 — remaining log cleanup

~~~
build-log.md still has leftovers from the clock drift: the "19:34" remotion --stills entry is out of order (it sits between 18:34 and 18:41), and cross-references still use old times ("corrected 19:48", "predicted at 17:52", "see 18:48"). Fix them from file mtimes, mark any you can't prove "~approx", then re-run deliver.sh. Do not change anything else.
~~~

## Command spine

Run from the toolkit folder; REEL is the reel folder (youtube/show-tell-veracite-pitch, next to brutalist.art). See paperwork/COMMANDS.md for every flag and the exact local patch.

~~~
./setup --install
# step 0b: one-line local patch to ClaudeDefinitions.tsx (meanSize 48 -> 52), see COMMANDS.md
python3 make_sheet.py
python3 runtime/scripts/generate_audio_kokoro.py --phonemize "<text>"
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"
python3 runtime/scripts/generate_audio_kokoro.py "$REEL" --only BOUT
python3 runtime/scripts/generate_audio_kokoro.py "$REEL" --only B09
# ffmpeg: pad BIDEA +0.8 s lead and BOUT +1.0 s tail, then ffprobe durations back into the sheet
python3 runtime/qc/static_scene_check.py scenes.py --class <C>
python3 runtime/qc/manim_layout_audit.py scenes.py --class <C> --curve-strict
manim -ql -s scenes.py <C>
./art run "$REEL"
./art final "$REEL" --height 2160 --out "$REEL/exports/landscape"
bash deliver.sh
~~~
