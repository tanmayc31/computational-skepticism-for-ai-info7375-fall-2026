# PROJECT-BRIEF — Veracite

**Author:** Tanmay Chandan · **Target role:** Forward Deployed Engineer / Software Engineer (AI-adjacent) · **Stack:** Python, pytest, SQLite, an LLM judge (API), runs locally

## 1. What is it?
Veracite is a command-line tool that checks each claim in a RAG system's answer against the passage it cites, and reports whether the citation is real, whether the passage is about the right subject, and whether it actually supports the claim.
When done, it will be a GitHub repository with the CLI, a small labeled test set of car-manual answer traces, an accuracy report, and a written failure analysis.

## 2. Why would anyone care?
It saves the engineer who owns a RAG system from reading traces by hand after a user complains, by showing which claims are mis-cited or about the wrong subject.
Alternatives I looked at: **RAGAS faithfulness** checks claims against all retrieved passages pooled together, so it cannot say which citation is wrong. **ALCE** is a research benchmark on fixed datasets, built for comparing models, not for checking your own app's answers. The manual alternative is what I did on RideReady: checking answers against the real manuals by hand.
I compared them from their public documentation. My first experiment will run RAGAS on the Camry case to see whether it catches the wrong car.

## 3. Who opens it, and what do they do?
A hiring manager or engineer hiring for an FDE role. In the first sixty seconds they will read the README, run `veracite show` on the Camry trace, and see `subject = mismatch` with the passage that caused it.

## 4. What does it prove about me?
Verification (the tool never passes a claim by default), evaluation (a held-out labeled set, error counts reported with *n*), and source grounding. A reviewer could fairly conclude I can build a checker and measure how often the checker itself is wrong. Evidence: the test suite, the accuracy report, and my design document.

## 5. In, out, first
**In:** claim splitter, citation resolver, evidence checker, verdict rules, CLI, accuracy harness, all local.
**Out:** it will not run inside a live production pipeline (no cloud queue, alerts, or dashboard, which are designed but deferred), and it will never rewrite or block an answer.
**First:** the Camry trace gives `subject = mismatch`; the same trace without vehicle metadata gives `unknown`, never `match`. Someone knows it ran because a pytest test passes and they can rerun it.

## 6. What could sink it?
The judge model could be wrong in a way I cannot see, for example a false "supported" verdict. I will keep a held-out labeled set that never touches prompt tuning, report errors as counts with *n*, and label any verdict from a judge version that has not been measured. Limitation: the labeled set will be small and labeled by one person.

## 7. Why this project?
A mix. **Existing skills:** RAG pipelines, Python, AWS. Evidence: my RideReady repository and its git history. **New skills:** LLM-as-judge evaluation, claim splitting, building a held-out evaluation set, and measuring a verifier's own error.
It started with a real failure: in RideReady, a Ford F-150 question retrieved a Toyota Camry chunk (similarity 0.547, above my 0.25 floor). The app declined correctly, but by luck. I fixed retrieval (commit `5d6e68e`, Jul 28, 2026). I don't yet know whether that fix holds when the question names a different vehicle than the session; Veracite's first test will find out.

---

**Exists today**
- Veracite software design document v0.10 (Oct 3, 2026) and its step-by-step build plan
- RideReady repository with git history, including the scoped-retrieval fix commit `5d6e68e` (Jul 28, 2026)
- The recorded Camry observation: Ford question → Camry chunk at 0.547 similarity
- RideReady tester survey (n = 7): "I trusted the citations" scored lowest of six questions (3.71 / 5)

**Will exist**
- Veracite code, CLI, and tests
- Labeled test set of car-manual traces (public manual data, no private data)
- Accuracy report with counts and *n*
- RAGAS comparison run on the Camry case
- An answer to whether the scoped-retrieval fix still leaks
- Written failure analysis
