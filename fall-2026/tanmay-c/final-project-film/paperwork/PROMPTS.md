# PROMPTS.md — show-tell-veracite-pitch

**No generation prompts.** This reel uses no image, video, audio-music or
AI-video generation of any kind. There is no Higgsfield beat, no Smithsonian
fetch, no pantry still, and no paid API call anywhere in the build.

Every frame is one of exactly two things:

| Source | Beats | How it is made |
|---|---|---|
| Drawn Manim (isometric, Claude palette, `iso_kit.py`) | B00–B12, BOUT | `scenes.py` in this folder, rendered locally by `art run` / `art final` |
| Remotion house bookends | BIDEA, BDEFS, BHTF | `BrutalistHesitantWriter`, `ClaudeDefinitions`, `ClaudeComposerAsk`, rendered locally via `runtime/scripts/remotion_scenes.py` |

Narration is Kokoro `am_onyx`, local, free — no voice API.

## The one prompt that appears ON SCREEN

BHTF (`ClaudeComposerAsk`) shows a prompt for the **viewer** to paste into
Claude. It is content, not a build instruction, and nothing in this pipeline
sends it anywhere:

> Take one answer from any AI app that cites sources. For each fact in it, open
> the cited passage and check two things: does it say this, and is it about the
> same thing you asked?

## Open slots

None. There are no slates, no placeholders and no pantry requests in this reel
— every beat is renderable from this folder with no human-supplied media.
