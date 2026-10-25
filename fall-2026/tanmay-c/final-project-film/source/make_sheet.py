#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for show-tell-veracite-pitch.

SHOW-TELL style (skills/make/show-tell/SKILL.md): every body beat is ONE drawn
isometric illustration in the Claude palette with at most a few words of label;
the narration carries the explanation.

AUTHOR OVERRIDES (these beat the skill where they conflict — Tanmay, 2026-10-24):
  1. Narrated by the author in the first person. No "Liam", no "in for Bear",
     no Nik Bear Brown name, persona, handle or credit line anywhere — voice,
     screen, outro or metadata. Greeting is "Hello. I'm Tanmay...".
  2. Narration text is VERBATIM from ../../NARRATION-DRAFT.md.
  3. Free local pipeline only: Kokoro am_onyx, Manim, Remotion. No paid anything.
  4. Honesty labels on screen: B03 prints "RideReady survey, n=7"; the one
     mock-up (B07) prints "constructed"; nothing unbuilt is drawn as finished.
  5. BOUT is a drawn Manim card, NOT ClaudeTitleOutro — that component
     hard-codes "@NikBearBrown" (OUTRO-LOCK.md, no prop override), which rule 1
     forbids. bookend_check.py is expected to fail on the outro for this reason.

Sources: see SOURCES.md (S1 RideReady commit 5d6e68e; S2 RideReady evaluation
report; S3 RideReady tester survey n=7; S4 Veracite design doc v0.10;
S5 RAGAS + ALCE public documentation).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "show-tell-veracite-pitch"
TITLE = "Veracite"
AUTHOR = "Tanmay Chandan"
VOICE = "am_onyx"

SPARSE_REASON = (
    "show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, "
    "with the voice carrying the explanation. The negative space is the style, so only "
    "underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply."
)


def est(text):
    return round(len(text.split()) / 2.5, 1)


def beat(bid, narration, cls, image, show, sparse=True):
    b = {
        "beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
        "narration_text": narration, "estimated_duration_s": est(narration),
        "voice": VOICE, "engine": "kokoro",
        "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                 "manim": {"class": cls}, "motion_claim": image},
    }
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {
        "beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate,
        "narration_text": narration, "estimated_duration_s": est(narration),
        "voice": VOICE, "engine": "kokoro",
        "shot": {"type": "REMOTION", "source": "own", "show": show,
                 "remotion": {"pattern": pattern, "props": props}},
    }
    b.update(extra)
    return b


# ───────────────────────── bookends: open ─────────────────────────
OPEN = [
    remotion(
        "BIDEA", "the question",
        "Hello. I'm Tanmay, and this is the pitch for my final project. The question isn't "
        "whether an AI app is accurate. It's whether each citation is real.",
        "BrutalistHesitantWriter",
        {"text": "Is my AI app accurate?",
         "triggerWords": "my AI app accurate",
         "replacementWords": "each citation real",
         "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1,
         "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
        [{"at": 0.0, "event": "types 'Is my AI app accurate?'"},
         {"at": 0.62, "event": "corrects to 'Is each citation real?' on the spoken correction"}],
        lead_silence_s=0.8,
        motion_claim="The writer types the naive accuracy question and corrects it to the real one: is each citation real.",
        qc={"sparse_by_design": True,
            "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),

    remotion(
        "BDEFS", "terms",
        "Four terms. RAG: an app that answers from retrieved documents. Citation: the passage "
        "an answer points to. Claim: one fact inside an answer. LLM judge: a model that grades "
        "another model's output.",
        "ClaudeDefinitions",
        {"title": "Terms In This Film",
         "terms": [
             {"term": "RAG", "meaning": "an app that answers from retrieved documents"},
             {"term": "citation", "meaning": "the passage an answer points to"},
             {"term": "claim", "meaning": "one fact inside an answer"},
             {"term": "LLM judge", "meaning": "a model that grades another model's output"},
         ],
         # GATE T: ClaudeDefinitions' footer chip is hard-coded fontSize 32, which renders a
         # ~40 px ink run at 4K — one pixel under GATE T's 41 px floor (§8.1), and it is the
         # ONLY sub-floor text in the reel. There is no font-size prop. Rather than edit a
         # shared component in the public toolkit, the chip is emptied: it carried no
         # information this film needs, and rule 1 wants no channel handle anyway.
         "folderLabel": "",
         # SKILL.md: set durationSeconds to the MEASURED audio. ClaudeDefinitions paces its term
         # reveals over durationSeconds * fps and defaults to 14 s; BDEFS's audio is 11.97 s, so
         # the default would land "LLM judge" after the clip had already been cut to length.
         "durationSeconds": 11.97},
        [{"at": 0.10, "event": "'RAG' lands"}, {"at": 0.36, "event": "'citation' lands"},
         {"at": 0.58, "event": "'claim' lands"}, {"at": 0.76, "event": "'LLM judge' lands"}],
        gate="CARD",
        qc={"sparse_by_design": True,
            "sparse_reason": "TERMS card: four prerequisites, one line each."}),
]

# ───────────────────────── body: one drawing per beat ─────────────────────────
BODY = [
    beat("B00",
         "I built RideReady, an assistant that answers driver questions from car owner's manuals. "
         "While testing it, a question about a Ford F-150 retrieved a chunk from the Toyota Camry "
         "manual, scoring zero point five four seven, above my zero point two five cutoff.",
         "B00_WrongPage",
         "A question slip labelled 'Ford question' drops onto the stage; a manual page labelled "
         "'Camry page' slides up beside it; a score counter climbs past a 0.25 floor line to 0.547.",
         [{"at": 0.18, "event": "Ford question slip drops in"},
          {"at": 0.46, "event": "Camry page slides up beside it"},
          {"at": 0.74, "event": "counter climbs past the 0.25 floor to 0.547"}]),

    beat("B01",
         "The app still declined correctly. But that was luck, not design. Nothing in my pipeline "
         "checked that the page was about the wrong car.",
         "B01_NoCheck",
         "The Camry page rides through a gate that has no check in it and comes out the far side "
         "untouched; a question mark lands over the empty gate.",
         [{"at": 0.20, "event": "the page enters the open gate"},
          {"at": 0.52, "event": "it passes straight through, nothing fires"},
          {"at": 0.80, "event": "a question mark lands over the empty gate"}]),

    beat("B02",
         "In a later version, I added a vehicle filter to retrieval. The open question is whether "
         "that filter still holds when a question names a different car than the session. Finding "
         "out will be Veracite's first test.",
         "B02_Filter",
         "A filter grate drops onto the page stack and holds most pages back; one page still slips "
         "past it and is drawn as a dotted outline — unknown, not resolved.",
         [{"at": 0.22, "event": "the filter grate drops onto the stack"},
          {"at": 0.58, "event": "one page still slips past"},
          {"at": 0.82, "event": "that page redraws as a dotted outline — still open"}]),

    beat("B03",
         "When seven people tested RideReady, \"I trusted the citations\" scored lowest of six "
         "questions: three point seven one out of five.",
         "B03_Survey",
         "Six grey bars grow on a board; the one for 'trust in citations' stays visibly shortest; "
         "a counter beside it reads 3.71, with the printed label 'RideReady survey, n=7'.",
         [{"at": 0.22, "event": "five bars grow"},
          {"at": 0.52, "event": "the short bar grows last and stays shortest"},
          {"at": 0.78, "event": "the 3.71 counter lands beside it"}]),

    beat("B04",
         "Veracite will be a command-line tool that checks each claim in a RAG answer against the "
         "passage it cites. For every claim it will record three things: is the citation real, is "
         "the passage about the right subject, and does it actually support the claim.",
         "B04_ClaimSlips",
         "An answer page splits into three claim slips; each slip rides through a dotted gate "
         "(Veracite, not built yet) to its own cited page; three checks light one after another.",
         [{"at": 0.20, "event": "the answer page splits into three claim slips"},
          {"at": 0.48, "event": "each slip rides to its cited page"},
          {"at": 0.70, "event": "check one: citation real"},
          {"at": 0.82, "event": "check two: right subject"},
          {"at": 0.92, "event": "check three: actually supports"}]),

    beat("B05",
         "RAGAS checks each claim against all the retrieved text pooled together, and gives one "
         "faithfulness score. ALCE is a research benchmark on fixed datasets, built for comparing "
         "models, not for checking your own app. Neither tells you which citation is wrong, or "
         "whether the page is even about the right car. Veracite will. My first experiment: "
         "running RAGAS on the Camry case, to see if it catches the wrong car.",
         "B05_PooledVsPerClaim",
         "Left: every page collapses into one pooled pile feeding a single dial — one faithfulness "
         "number. Right: each claim slip gets its own arrow to its own exact page, drawn dotted.",
         [{"at": 0.14, "event": "pages collapse into the pooled pile"},
          {"at": 0.26, "event": "one dial reads a single score"},
          {"at": 0.46, "event": "the ALCE fixed-dataset block lands beside it"},
          {"at": 0.74, "event": "on the right, per-slip arrows find separate pages"}]),

    beat("B06",
         "One rule: Veracite will never pass a claim by default. Missing vehicle metadata becomes "
         "\"unknown\". A judge timeout becomes \"unverified\". Never \"supported\".",
         "B06_NeverPass",
         "A claim slip with a missing tag reaches the dotted gate; a stamp swings down and lands "
         "reading 'unknown' — not a check mark.",
         [{"at": 0.24, "event": "the slip with the missing tag reaches the gate"},
          {"at": 0.58, "event": "the stamp swings down"},
          {"at": 0.76, "event": "it lands reading 'unknown', not a check"}]),

    beat("B07",
         "The reader is a hiring manager for a forward deployed engineer role. In the first "
         "minute, they'll run one command on the Camry case and see \"subject mismatch\", with the "
         "passage that caused it.",
         "B07_OneCommand",
         "A laptop with one command line; a result slip slides out of it reading 'subject "
         "mismatch' and points back at the Camry page. The frame is labelled 'constructed' "
         "because this tool does not exist yet.",
         [{"at": 0.30, "event": "the laptop and one command line land"},
          {"at": 0.62, "event": "the command runs"},
          {"at": 0.80, "event": "the result slip slides out and points at the Camry page"}]),

    beat("B08",
         "It will prove I can build a checker, and measure how often the checker itself is wrong. "
         "Errors will be counts on a held-out test set, with the sample size, never a bare "
         "percentage.",
         "B08_CheckTheChecker",
         "A second, smaller gate turns to face the first gate and inspects it; a tally board "
         "beside them fills with counted marks, each one a number rather than a percentage.",
         [{"at": 0.22, "event": "the small gate turns to face the big one"},
          {"at": 0.54, "event": "it inspects the checker"},
          {"at": 0.78, "event": "the tally board fills with counts"}]),

    # B09 narration revised by the author after watching the master (2026-10-24, approved under
    # rule 2): "Out:" was ambiguous when spoken, so it became "Out of scope, on purpose:".
    beat("B09",
         "In scope: it runs locally, on recorded traces. Out of scope, on purpose: it will not "
         "plug into a live production system, and it will never rewrite or block an answer. "
         "First: a test where the Camry case returns mismatch, and the same case without "
         "vehicle metadata returns unknown, never match.",
         "B09_InOut",
         "A solid box marked 'local' holds the recorded traces; a cloud beside it gets crossed "
         "out; then one dotted test light turns on below them.",
         [{"at": 0.18, "event": "the local box lands with its traces"},
          {"at": 0.48, "event": "the cross lands on the cloud"},
          {"at": 0.80, "event": "one first-test light turns on"}]),

    beat("B10",
         "What could sink it: the judge being wrong in ways I can't see, like a false "
         "\"supported\". So the held-out set never touches prompt tuning, and any verdict from an "
         "unmeasured judge gets a warning. The limit: the set will be small, and labeled by me "
         "alone.",
         "B10_JudgeWrong",
         "A judge stamp lands 'supported' on a slip whose own mark shows it is wrong; a warning "
         "flag rises beside it.",
         [{"at": 0.22, "event": "the stamp lands 'supported' on the wrong slip"},
          {"at": 0.52, "event": "the slip's own mark contradicts it"},
          {"at": 0.80, "event": "a warning flag rises beside it"}]),

    beat("B11",
         "Why this project? It's a mix. I already build RAG pipelines in Python, and my RideReady "
         "repo and its git history show that. What's new is evaluation: splitting claims, LLM "
         "judges, and measuring a verifier's own error.",
         "B11_HaveNew",
         "Two stacks side by side: 'have' is solid with a git branch line drawn beside it; 'new' "
         "is an open outline that fills with one layer while you watch.",
         [{"at": 0.26, "event": "the solid 'have' stack is already standing"},
          {"at": 0.52, "event": "the git branch line draws beside it"},
          {"at": 0.80, "event": "one layer fills the outlined 'new' stack"}]),

    beat("B12",
         "What exists today: the Veracite design document, the RideReady repo with its fix commit, "
         "and that recorded failure. Everything else, the code, the test set, and the results, "
         "will exist by the end of the semester. After that, the cloud pipeline and live alerts "
         "are already designed, and come next.",
         "B12_ExistsWillExist",
         "Left: three solid objects — the design document, the repo, the recorded failure page. "
         "Right: three dotted outlines drawing themselves in — the code, the test set, the results.",
         [{"at": 0.16, "event": "the three solid objects settle on the left"},
          {"at": 0.58, "event": "the three dotted outlines draw in on the right"},
          {"at": 0.86, "event": "the last outline completes"}]),
]

# ───────────────────────── bookends: close ─────────────────────────
YT_PROMPT = ("Take one answer from any AI app that cites sources. For each fact in it, open the "
             "cited passage and check two things: does it say this, and is it about the same "
             "thing you asked?")

CLOSE = [
    remotion(
        "BHTF", "your turn",
        "Your turn. " + YT_PROMPT,
        "ClaudeComposerAsk",
        {"greeting": "Your turn.", "topic": "VERACITE · YOUR TURN",
         "segment": "Check One Citation Yourself", "command": YT_PROMPT,
         "runningText": "paste this into Claude…",
         "output": ["Check: does the cited passage actually say this?",
                    "Check: is it about the same thing you asked?"],
         "folderLabel": "Veracite", "modelLabel": "Opus 5", "effortLabel": "High"},
        [{"at": 0.0, "event": "composer opens — 'Your turn.'"},
         {"at": 0.12, "event": "the prompt types in full"},
         {"at": 0.84, "event": "the two check lines land"}]),
]

# BOUT is the one line where Kokoro breaks (author-approved change, 2026-10-24, rule 2):
# "Veracite. Tanmay Chandan." is voiced "Vericite TEN-MAY SHAN-den" — the trailing period makes
# Kokoro re-parse "Tanmay" as "ten May", and its G2P maps Ch -> /S/. Dropping the final period
# and respelling the surname "Chundan" (/tS'Vnd@n/) gives TAN-may CHUN-dun, which whisper
# transcribes back as "Chandan". This is the TTS INPUT only — the card on screen, the metadata
# and every other beat still read "Tanmay Chandan".
SPOKEN_AUTHOR = "Tanmay Chundan"

OUTRO = {
    "beat_id": "BOUT", "act": "outro", "lane": "manim", "proof_gate": "SHOW",
    "narration_text": f"{TITLE}. {SPOKEN_AUTHOR}",
    "display_text": f"{TITLE}. {AUTHOR}.",
    "estimated_duration_s": 3.0, "voice": VOICE, "engine": "kokoro",
    "shot": {"type": "GRAPHIC", "source": "own",
             "visual_intent": "Title card: 'Veracite' large in ink, a terracotta rule drawing "
                              "under it, then 'Tanmay Chandan'. No channel handle, no mascot.",
             "show": [{"at": 0.10, "event": "the title lands"},
                      {"at": 0.45, "event": "a terracotta rule draws under it"},
                      {"at": 0.70, "event": "the author name lands"}],
             "manim": {"class": "BOUT_Title"},
             "motion_claim": "The rule draws under the title and the author name lands."},
    "kind": "outro_voice", "tail_silence_s": 1.0,
    "qc": {"sparse_by_design": True,
           "sparse_reason": "Title outro: two lines of type and one rule on the cream stage."},
}

BEATS = OPEN + BODY + CLOSE + [OUTRO]

sheet = {
    "metadata": {
        "slug": SLUG, "title": TITLE, "topic": "VERACITE · FINAL PROJECT PITCH",
        "skill": "show-tell", "style_preset": "show-tell",
        "channel": "veracite", "channel_title": "Veracite",
        "persona": AUTHOR, "author": AUTHOR,
        "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
        "clock": "narration", "palette": "claude", "register": "first person, plain",
        "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
        "caption_policy": "none", "greeting_language": "English (Hello)",
        "bookend_exempt": ["cold-open", "bvdt"],
        "bookend_exempt_reason": (
            "show-tell style: opens on the hesitant writer + terms card, no verdict card; Your "
            "Turn is the Claude.ai composer. AUTHOR OVERRIDE (Tanmay, 2026-10-24): the film is "
            "narrated by the author in the first person, so there is no Liam / in-for-Bear "
            "persona and no @NikBearBrown handle anywhere — voice, screen, outro or metadata. "
            "BOUT is therefore a drawn Manim title card instead of ClaudeTitleOutro, whose "
            "handle is hard-coded by OUTRO-LOCK.md with no prop override. The outro bookend "
            "check is expected to FAIL on pattern for exactly this reason; the author's rule "
            "wins and the failure is recorded in SHOTLIST.md and ../build-log.md."),
        "audience": "a hiring manager or engineer evaluating a forward deployed engineer candidate",
        "source_doc": ("SOURCES.md — S1 RideReady commit 5d6e68e 'scoped retrieval by vehicle'; "
                       "S2 RideReady evaluation report (0.547 Camry chunk, 0.25 floor); "
                       "S3 RideReady tester survey n=7 ('I trusted the citations' 3.71/5, lowest "
                       "of six); S4 Veracite software design document v0.10; S5 RAGAS and ALCE "
                       "public documentation"),
        "playlist": "Computational Skepticism",
        "chapter_number": 0,
        "tags": ["Veracite", "RAG evaluation", "citation checking", "LLM as judge",
                 "retrieval augmented generation", "computational skepticism", "Tanmay Chandan"],
    },
    "beats": BEATS,
}

(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
words = sum(len(b["narration_text"].split()) for b in BEATS)
print(f"{len(BEATS)} beats · {words} words · est {round(sum(b['estimated_duration_s'] for b in BEATS))} s "
      f"({round(sum(b['estimated_duration_s'] for b in BEATS) / 60, 2)} min)")
