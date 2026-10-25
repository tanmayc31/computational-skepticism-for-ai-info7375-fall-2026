# SOURCES.md — show-tell-veracite-pitch

Every factual claim in this film traces to one of the five sources below.
There is no web research in this reel and no generated media: all sources are
the author's own primary records, plus two pieces of public vendor documentation
used only to describe what those tools do.

| # | Source | Kind | Held where | Used by |
|---|---|---|---|---|
| S1 | RideReady repository, commit `5d6e68e` — "scoped retrieval by vehicle" (Jul 28, 2026) | Primary — author's own git history | Author's RideReady repo | B02, B11, B12 |
| S2 | RideReady evaluation report — Ford F-150 question retrieved a Toyota Camry manual chunk at similarity 0.547, against a 0.25 relevance floor; the app declined to answer | Primary — author's own recorded evaluation run | Author's RideReady evaluation report | B00, B01, B05, B07, B09 |
| S3 | RideReady tester survey, n = 7 — "I trusted the citations" scored 3.71 / 5, the lowest of six questions | Primary — author's own survey results | Author's RideReady evaluation report | B03 |
| S4 | Veracite software design document v0.10 (Oct 3, 2026) and its step-by-step build plan | Primary — author's own design document | Author's project files | B04, B06, B07, B08, B09, B10, B11, B12 |
| S5 | RAGAS and ALCE public documentation | Secondary — public vendor / project documentation | Public docs, read for this film | B05 |

## Notes on S5

The film describes RAGAS and ALCE only as their own public documentation
describes them — RAGAS faithfulness scoring claims against the pooled retrieved
context and returning one score; ALCE as a fixed-dataset research benchmark for
comparing systems. The film does not claim to have benchmarked either tool. The
RAGAS run on the Camry case is stated in the future tense, as a planned first
experiment, because it has not been run.

## What is NOT a source

Nothing in this film comes from a model's recollection, a social post, or a
screenshot of someone else's product. No figure is estimated. Every number
spoken aloud (0.547, 0.25, 3.71, 5, 6, 7) is read from S2 or S3.

---

## Build-environment modification (affects reproduction, not the claims)

To reproduce this film byte-for-byte you need **one uncommitted one-line change** to the
toolkit clone. It is recorded here because it changes the rendered output, so anyone
re-rendering from a clean checkout would get a different (gate-failing) BDEFS.

File: `brutalist.art/runtime/remotion/src/scenes/ClaudeDefinitions.tsx`

```diff
@@ -79,7 +79,10 @@ export const ClaudeDefinitions: React.FC<ClaudeDefinitionsProps> = ({
   const bottom = SAFE.y + SAFE.h - 70;
   const rowH = Math.floor((bottom - top) / n);
   const termSize = n <= 3 ? 54 : 50;
-  const meanSize = 48;   // ≥ 48: a lowercase run's x-height must clear GATE T's 41px floor at 4K
+  // GATE T §8.1 (2026-10-24): at 48 a PURE x-height run — 'swe' in "answers" — measures
+  // exactly 40px at 4K/scale=2, one pixel under the 41px floor, so any definitions card
+  // whose meaning text has three consecutive x-height letters fails the gate. 52 gives ~43px.
+  const meanSize = 52;
 
   // Which row landed most recently → carries the terracotta.
   let active = -1;
```

**Status: local working tree only. Not committed, not pushed.** The toolkit's HEAD is
unchanged at `a99b5323`. Revert with:

```bash
git -C brutalist.art checkout -- runtime/remotion/src/scenes/ClaudeDefinitions.tsx
```

**Why it was needed.** GATE T §8.1 enforces a minimum text-run height of 1.9% of frame
height (41 px at 2160). `ClaudeDefinitions` renders its meaning column at 48 design px,
which at 4K/scale=2 produces a 40 px run for any cluster of three consecutive x-height
letters — the cluster "swe" in the word "answers". Three of this film's four definitions
contain "answer", so the text could not be reworded around it. 52 design px yields ~43 px.

**This affects no factual claim in the film.** It changes the meaning column's type size by
4 design px; every term, every definition and every number is identical.
