# Veracite — Final Project Pitch Film

**Author:** Tanmay Chandan
**Course:** INFO 7375 · Final Project Pitch Film
**Working title:** Veracite — a claim-level citation checker for RAG answers
**Target role:** Forward Deployed Engineer / Software Engineer (AI-adjacent)
**Runtime:** 3:24 (3840×2160, 24 fps, h264)
**Made with:** Brutalist toolkit (`show-tell` skill), free local pipeline only: Kokoro TTS, Manim, Remotion. $0.00, no API keys, nothing published.

## What's in this folder

| File | What it is |
|---|---|
| `show-tell-veracite-pitch.mp4` | The film |
| `PROJECT-BRIEF.md` | The seven answers in text, ending with *exists today* / *will exist* |
| `beat_sheet.json` | Narration and visual plan, one entry per beat (17 beats) |
| `BUILD-PROMPT.md` | The prompts and commands that rebuild the film |
| `SOURCES.md` | What I used, what I made, what Claude contributed, third-party assets |
| `FRICTIONAL.md` | My dated log of decisions and problems |
| `build-log.md` | Claude Code's detailed build log (problems hit and fixes) |
| `gate-reports/` | The toolkit's quality-gate reports |
| `paperwork/` | Fact-check, shot list, prompts and command list the toolkit requires |
| `source/` | `make_sheet.py` and `scenes.py` (the film's source) |

## Gate results (final master)

GATE T (type) PASS · Gate V (visual) PASS · Gate A / Gate W / layout audit PASS · fact-check PASS.
**GATE BOOKEND fails by design:** the toolkit's outro component hard-codes the instructor's handle, and the assignment requires narrating as myself with no instructor name, persona or credit line. Explained in `gate-reports/GATE-BOOKEND.md`.

## How to rebuild

1. Clone the toolkit and check out the commit this film was built on:
   `git clone https://github.com/nikbearbrown/brutalist.art && cd brutalist.art && git checkout a99b5323`
2. Install: `./setup --install` (Python 3.11, Node, ffmpeg; downloads the free Kokoro voice model).
3. Apply the one-line local patch described in `paperwork/COMMANDS.md` step 0b (a font size in `ClaudeDefinitions.tsx` that renders 1 px under the toolkit's own GATE T floor). It is local only and was never pushed.
4. Put the `source/` files in the reel folder and follow `BUILD-PROMPT.md` / `paperwork/COMMANDS.md`: build the sheet, voice it, check pronunciation, render with `./art run`, then `./art final --height 2160`.

No private data is included: the film uses my own RideReady project facts and public documentation only.
