# FACTCHECK.md — show-tell-veracite-pitch

Status: checked and signed off by Tanmay Chandan (author), 2026-10-24. Every row was read
back against the named source after the beat sheet was written, not only while drafting it.

Verdicts: **PASS** (claim is supported by the named source as stated) ·
**CORRECTED** (claim was changed before shipping) · **EXEMPT** (not a factual
claim — a plan, an intention, a definition, or the author's own judgement,
and spoken in the future or first-person conditional so the viewer can tell).

Sources S1–S5 are defined in `SOURCES.md`.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | "The question isn't whether an AI app is accurate. It's whether each citation is real." | EXEMPT | S4 §1–2 | Author's framing/thesis, not a factual assertion. Derivation: S4 states the tool's purpose as per-citation checking rather than overall accuracy scoring. |
| 2 | BDEFS | RAG: "an app that answers from retrieved documents" | PASS | S5 | Standard definition, consistent with RAGAS docs. |
| 3 | BDEFS | Citation: "the passage an answer points to" | PASS | S4 | Definition as used throughout the Veracite design doc. |
| 4 | BDEFS | Claim: "one fact inside an answer" | PASS | S4 | Definition as used by the claim splitter in S4. |
| 5 | BDEFS | LLM judge: "a model that grades another model's output" | PASS | S4, S5 | Standard definition. |
| 6 | B00 | "I built RideReady, an assistant that answers driver questions from car owner's manuals." | PASS | S1, S2 | Repo exists with git history. |
| 7 | B00 | A Ford F-150 question retrieved a chunk from the Toyota Camry manual | PASS | S2 | Recorded in the evaluation report. |
| 8 | B00 | That chunk scored **0.547** | PASS | S2 | Exact figure from S2. Spoken as "zero point five four seven". |
| 9 | B00 | 0.547 was "above my zero point two five cutoff" | PASS | S2 | Relevance floor of 0.25 recorded in S2; 0.547 > 0.25. |
| 10 | B01 | "The app still declined correctly." | PASS | S2 | S2 records the decline. |
| 11 | B01 | "that was luck, not design. Nothing in my pipeline checked that the page was about the wrong car." | PASS | S1, S2 | No subject check existed before commit `5d6e68e` (S1); S2 records no subject check firing. |
| 12 | B02 | "In a later version, I added a vehicle filter to retrieval." | PASS | S1 | Commit `5d6e68e`, "scoped retrieval by vehicle", Jul 28 2026. |
| 13 | B02 | Whether that filter holds when the question names a different car than the session is **open** | EXEMPT | S1 | Stated as an open question, not a result. Drawn as a dotted (unknown) outline on screen. |
| 14 | B03 | "When seven people tested RideReady" | PASS | S3 | n = 7. On screen as "RideReady survey, n=7". |
| 15 | B03 | "I trusted the citations" scored **lowest of six questions** | PASS | S3 | Six-question survey; this item ranked last. |
| 16 | B03 | The score was **3.71 out of 5** | PASS | S3 | Exact figure from S3. Spoken as "three point seven one out of five". |
| 17 | B04 | Veracite **will be** a CLI that checks each claim against the passage it cites, recording citation-real / right-subject / actually-supports | EXEMPT | S4 | Design intent, spoken in future tense. Drawn with a dotted gate — not drawn as finished. |
| 18 | B05 | RAGAS checks claims against all retrieved text **pooled together** and gives one faithfulness score | PASS | S5 | As described in RAGAS public documentation. |
| 19 | B05 | ALCE is a research benchmark on **fixed datasets**, built for comparing models | PASS | S5 | As described in ALCE public documentation. |
| 20 | B05 | "Neither tells you which citation is wrong, or whether the page is even about the right car." | PASS | S5 | Follows from the two descriptions above: a pooled score has no per-citation verdict, and neither tool models document subject. Scope: as documented; not an empirical benchmark result. |
| 21 | B05 | "Veracite will." | EXEMPT | S4 | Design intent, future tense. |
| 22 | B05 | "My first experiment: running RAGAS on the Camry case" | EXEMPT | S4 | Plan, not a result. The film never claims the run happened. |
| 23 | B06 | Veracite will never pass a claim by default; missing metadata → "unknown", judge timeout → "unverified" | EXEMPT | S4 | Verdict rules from the design document, future tense. |
| 24 | B07 | The intended reader is a hiring manager for a forward deployed engineer role | EXEMPT | S4 | Author's stated audience. |
| 25 | B07 | They'll run one command on the Camry case and see "subject mismatch" with the passage | EXEMPT | S4 | Planned first-run behaviour. The terminal on screen is a mock-up and is **labelled "constructed"**. |
| 26 | B08 | Errors will be reported as counts on a held-out test set, with the sample size, never a bare percentage | EXEMPT | S4 | Measurement commitment from S4, future tense. |
| 27 | B09 | In scope: runs locally on recorded traces. Out: no live production system; never rewrites or blocks an answer | EXEMPT | S4 | Scope statement from S4. |
| 28 | B09 | First test: Camry case → "mismatch"; same case without vehicle metadata → "unknown", never "match" | EXEMPT | S4 | Planned acceptance test. |
| 29 | B10 | Risk: the judge wrong in ways the author can't see, e.g. a false "supported" | EXEMPT | S4 | Stated risk. |
| 30 | B10 | Mitigation: held-out set never touches prompt tuning; unmeasured judge verdicts get a warning | EXEMPT | S4 | Stated mitigation, future tense. |
| 31 | B10 | Limit: the set will be small, and labeled by the author alone | PASS | S4 | Stated limitation; the film says it out loud rather than hiding it. |
| 32 | B11 | "I already build RAG pipelines in Python, and my RideReady repo and its git history show that." | PASS | S1 | Repo + git history are the evidence. |
| 33 | B11 | What's new: LLM judges, claim splitting, measuring a verifier's own error | EXEMPT | S4 | Author's self-assessment. |
| 34 | B12 | What exists today: the Veracite design document, the RideReady repo with its fix commit, and the recorded failure | PASS | S1, S2, S4 | All three are held artifacts. |
| 35 | B12 | Code, test set and results "will exist by the end of the semester" | EXEMPT | S4 | Commitment, future tense. Drawn as dotted outlines — not drawn as finished. |
| 36 | B12 | The cloud pipeline and live alerts "are already designed, and come next" | PASS | S4 | S4 contains the deferred cloud design. |
| 37 | BHTF | The viewer exercise | EXEMPT | S4 §1 | An instruction, not a claim. Derivation: it is the manual version of the two checks S4 defines for Veracite — "does the passage support it" and "is it the right subject". |
| 38 | BOUT | "Veracite. Tanmay Chandan." | PASS | S4 title page | Project name and author, as printed on the Veracite design document v0.10. Spoken as "Chundan" for Kokoro; see the pronunciation note below. |

## Honesty rules applied on screen

- **B03** carries the printed label **"RideReady survey, n=7"** beside the chart.
  A thin-n figure is never shown without its n.
- **B07** is a mock-up of a tool that does not exist yet. It carries the printed
  label **"constructed"**.
- Everything Veracite "will" do is drawn as a **dotted / open outline**
  (B02 unknown, B04 gate, B06 gate, B09 first-test light, B12 right-hand stack),
  never as a solid finished object. Solid objects on screen mean the thing
  exists today.
- No percentage appears anywhere in the film without its denominator.

## Double-check

The two numbers that carry the most weight (0.547 against the 0.25 floor, and
3.71 as lowest of six at n=7) were each read back against S2 and S3 after the
beat sheet was written, not only when it was drafted. Both match. The
comparison claim in B05 (#20) is the one claim whose strength depends on
reading two vendor documents correctly; it is therefore scoped in writing to
"as their public documentation describes them", and the film says the RAGAS
comparison run has **not** happened yet.

## Pronunciation note (does not change any claim)

BOUT's TTS input is spelled `Veracite. Tanmay Chundan` because Kokoro voices the written form
"Veracite. Tanmay Chandan." as *"Vericite ten-May Shan-den"* — the trailing period makes it
re-parse "Tanmay" as "ten May", and its grapheme-to-phoneme map sends `Ch` to /ʃ/. The respelling
is TTS input only, verified by whisper transcript ("Varasite Tanmay Chandan."). The card on
screen, `display_text` in the beat sheet, and every other beat all read "Tanmay Chandan".
No claim is affected.
