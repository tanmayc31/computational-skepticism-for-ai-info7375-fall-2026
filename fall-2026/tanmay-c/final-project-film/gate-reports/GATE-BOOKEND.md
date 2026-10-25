# GATE BOOKEND — recorded FAILURE, accepted by the author

`runtime/scripts/bookend_check.py` output, run 2026-10-24 against this reel:

```
[bookend] BLOCKED — 2 failure(s) in show-tell-veracite-pitch:
  ✗ OUTRO handle is empty — must be 'Veracite'
  ✗ OUTRO title is missing or is the sentinel placeholder — set title='Veracite' in the outro beat props
```

## Why this fails, and why it is not being fixed

The gate asserts that the outro beat is a `ClaudeTitleOutro` Remotion composition and reads its
`handle` and `title` props. This reel's BOUT is a **drawn Manim title card** (`BOUT_Title`), so
there are no such props and the gate reports both as missing.

That substitution is deliberate. The author's rule 1 for this film is: no "Liam", no "in for
Bear", and no Nik Bear Brown name, persona, handle or credit line anywhere — voice, screen,
outro or metadata. `ClaudeTitleOutro.tsx` **hard-codes** the handle:

> `handle  → '@NikBearBrown', HARDCODED — no prop, no lookup, no override.`
> (`runtime/remotion/src/scenes/ClaudeTitleOutro.tsx`, locked by `OUTRO-LOCK.md`)

There is no prop, flag or metadata key that suppresses it, and `OUTRO-LOCK.md` forbids editing
it. Using the component as the skill requires would put the handle on screen, which rule 1
forbids. Using it with an empty handle is not possible.

So the outro was rebuilt as a Manim card in the same Claude palette, showing the film's title
and the author's name and nothing else. Per the author's rule 5 — *"if a toolkit gate or bookend
check fails because of rule 1, do not undo my rule; record it and continue"* — this failure is
recorded here and the build continues.

## What the gate would have caught, checked by hand instead

| assertion | status |
|---|---|
| an outro beat exists, last in the sheet | ✅ `BOUT`, beat 17 of 17 |
| the outro restates the film's title | ✅ "Veracite" is the first word spoken and the large type on the card |
| no baked tagline / subline | ✅ the card carries the title, a terracotta rule, and the author's name — nothing else |
| the outro is voiced, with a silent tail | ✅ Kokoro `am_onyx`, 2.28 s of speech + a 1.0 s silent tail = 3.28 s |
| the handle matches the channel | ⛔ **intentionally absent** — this film has no channel handle |

## The other three bookends all pass unchanged

`BIDEA` is `BrutalistHesitantWriter`, `BDEFS` is `ClaudeDefinitions`, `BHTF` is
`ClaudeComposerAsk` with "YOUR TURN" in its topic — the three the skill requires. The cold-open
composer and the verdict card are dropped under the skill's own
`bookend_exempt: ["cold-open", "bvdt"]`, as show-tell prescribes.
