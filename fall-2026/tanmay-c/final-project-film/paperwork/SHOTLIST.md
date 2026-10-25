# SHOTLIST.md — show-tell-veracite-pitch

17 beats. Style: **show-tell** — one drawn isometric image per beat, labels of
1–3 words, the voice carries the explanation.

**Cast (law 4 — same objects, whole film).** Five objects, reused end to end:

| object | what it is | first seen |
|---|---|---|
| **manual page** | a kraft/white page — one chunk of a car owner's manual | B00 (the Camry page) |
| **question slip** | a small slip — a user's question | B00 (the Ford question) |
| **answer page** | a page that splits into **claim slips** | B04 |
| **check gate** | an arch the slips ride through; **dotted = Veracite, not built yet** | B01 (open, no check) |
| **counter / tally** | a number that climbs, and the bar board | B00 (0.547), B03, B08 |

**Cards used: zero.** Every body beat is a drawing. B03 (the survey chart) was
the only beat that could have taken a `ShowTellCard` (`chart`): it passes card
test 1 (real numbers) and 2 (bars growing, one shortest, IS the claim), but
fails test 3 — the beat needs the printed honesty label "RideReady survey, n=7"
and the "lowest of six" emphasis held on screen, which a drawn chart controls
and the card kind does not. SKILL.md: a film with zero cards is a normal,
complete show-tell film.

| beat | lane | class / pattern | the drawing | motion that carries the claim | labels on screen |
|---|---|---|---|---|---|
| BIDEA | bookend | `BrutalistHesitantWriter` | the typed question corrects itself | "Is my AI app accurate?" → "Is each citation real?" | — |
| BDEFS | bookend | `ClaudeDefinitions` | terms card | four terms land one by one | RAG · citation · claim · LLM judge |
| B00 | manim | `B00_WrongPage` | a Ford question slip drops in; a Camry manual page slides up beside it; a score counter climbs | the counter climbing **past** the floor line is the claim | Ford question · Camry page · `0.547` · floor `0.25` |
| B01 | manim | `B01_NoCheck` | the wrong page rides through an **open** gate — nothing stops it | the page passing clean through, then a question mark landing | no check |
| B02 | manim | `B02_Filter` | a filter grate drops onto the page stack; one page still slips past it; its outline is **dotted** (unknown) | the grate landing, then the one page escaping | fix · still open? |
| B03 | manim | `B03_Survey` | six grey bars grow on a board; the "trusted the citations" bar stays shortest; a counter reads 3.71 | the six bars growing to different heights, the short one last | trust in citations · `3.71` · **RideReady survey, n=7** |
| B04 | manim | `B04_ClaimSlips` | an answer page splits into three claim slips; each rides to its cited page through a **dotted** gate; three checks light one by one | the split, then the three checks lighting | claim · real? · subject? · supports? |
| B05 | manim | `B05_PooledVsPerClaim` | left: all pages pooled into one pile feeding one dial (RAGAS). right: each slip arrowed to its own exact page (Veracite, dotted) | the pile collapsing to one number vs. arrows finding separate pages | RAGAS · ALCE · Veracite |
| B06 | manim | `B06_NeverPass` | a slip with a missing tag reaches the gate; a stamp lands reading "unknown" — not a check | the stamp landing on the **wrong-looking** word | never pass by default |
| B07 | manim | `B07_OneCommand` | a laptop with one command line; a result slip slides out and points to the Camry page. **Mock-up — labelled "constructed"** | the command running, the result slip emerging and pointing | one command · mismatch · **constructed** |
| B08 | manim | `B08_CheckTheChecker` | a second, smaller gate inspects the first gate; a tally board fills with marks | the small gate turning to face the big one, then the tally filling | held-out set · counts + n |
| B09 | manim | `B09_InOut` | a box marked local; a cloud beside it gets crossed out; one test light turns on | the cross landing on the cloud, then the single light | local · not live · first test |
| B10 | manim | `B10_JudgeWrong` | a judge stamp lands "supported" on a slip that is visibly wrong; a warning flag rises beside it | the wrong stamp landing, then the flag rising | risk · warning |
| B11 | manim | `B11_HaveNew` | two stacks: "have" solid with a git branch line, "new" an outline that fills slowly | the solid stack already there; the outlined stack filling one layer | have · new |
| B12 | manim | `B12_ExistsWillExist` | left: three solid objects (doc, repo, page). right: three dotted outlines | the solid three settling, the dotted three drawing in | exists · will exist |
| BHTF | bookend | `ClaudeComposerAsk` | the Claude.ai composer; the prompt types in full | the prompt typing, then two check lines landing | YOUR TURN |
| BOUT | manim | `BOUT_Title` | title card: **Veracite**, then **Tanmay Chandan**, one terracotta rule | the rule drawing under the title, the name landing | Veracite · Tanmay Chandan |

## Honesty on screen

- **B03** prints **"RideReady survey, n=7"**. The n is never dropped.
- **B07** prints **"constructed"** — it is a mock-up of a tool that does not exist.
- Everything that does not exist yet is drawn **dotted or open**, never solid:
  B02's unresolved leak, B04's and B06's gate, B09's first-test light, B12's
  right-hand column. Solid = exists today.

## Deviations from `skills/make/show-tell/SKILL.md`

Recorded, not worked around (author's rules override the skill here):

1. **No Liam, no "in for Bear", no @NikBearBrown** — anywhere: voice, screen,
   outro or metadata. BIDEA's greeting is "Hello. I'm Tanmay…". `folderLabel`
   on BDEFS and BHTF is "Veracite", not the channel handle.
2. **BOUT is a drawn Manim card, not `ClaudeTitleOutro`.** The Remotion
   component hard-codes "@NikBearBrown" in its source (no prop, no override,
   locked by `OUTRO-LOCK.md`), so it cannot satisfy rule 1. `bookend_check.py`
   is expected to FAIL on the outro pattern for exactly this reason.
3. Voice is Kokoro `am_onyx` as the skill specifies, but the persona is the
   author in first person, not a character.
