# Peer Review — _Artificial Intelligence and Nutritionist-Guided Dietary Personalization: A Systematic Review of Clinical and Technological Integration_

**Review date:** 2026-08-10
**Source reviewed:** `Tech Enabled Dietary Personalization.docx` (extracted to `extractions/tech_enabled_dietary_personalization_review.md`)
**Review method:** Full-text extraction (pandoc) → structured audit (academic-researcher framework) → verification of every citation-content pairing against the published record via web search.
**Overall verdict:** **Major revisions required before this manuscript can be considered a defensible systematic review.** The manuscript contains several verified citation–content mismatches (including one entirely off-topic study), a critical PRISMA citation error, an internally contradictory search window, and extensive AI-generated prose artifacts. The underlying synthesis idea — that AI and nutritionist-guided approaches are complementary — is reasonable, but as currently written the paper does not meet PRISMA reporting standards and some passages misattribute evidence to the wrong sources.

---

## 1. Critical Issues (must fix — data integrity / factual errors)

### 1.1 An off-topic archaeology paper is included as a reviewed study (Section 3.2.5, Table-7)

> "Accurate population proxies do not exist between 11.7 and 15 ka in North America" (Pelton SR, Mackie ME, Kelly R, Surovell TA. _Nat Commun_. 2022)

- **Verified:** This is a peer-reviewed **archaeology/palaeoecology** paper (PubMed subject terms: _Archaeology, Palaeontology, Palaeoecology_) about radiocarbon-dated event-count modeling of human/megafaunal populations in late Quaternary North America. It has **zero** connection to AI-driven personalized nutrition or the gut microbiome.
- It is placed inside "**3.2.5 Critical Review of AI-Driven Personalized Nutrition in Gut Microbiome**", classified as "Nutritionist-guided" in Table-7, and the synthesis paragraph even acknowledges the problem by describing the corpus as "spanning both prehistoric demographic modeling and modern personalized nutrition interventions."
- **Action:** Remove this study (text, table row, reference #10). This is almost certainly a reference-manager mix-up from an unrelated project.

### 1.2 PRISMA is cited to a hospitality-management paper (Methodology)

> "(Elkhwesky Z, Salem IE, Ramkissoon H, Castañeda-García JA)" — Ref. #25

- **Verified:** Elkhwesky et al. (2022, _Int J Contemp Hosp Manag_) is "A systematic and critical review of leadership styles in contemporary hospitality." It is **not** the PRISMA statement.
- **Action:** Replace with the canonical citation: Page MJ, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. _BMJ_. 2021;372:n71.

### 1.3 Kassem et al. is mis-attributed to two different studies

- **In §3.2.6** the paper attributes "Effects of Intermittent Fasting on Health Markers in Humans" to "Kassem H, Beevi A, Basheer S, Lutfi G, Ismail LC, Papandreou D".
- **In Table-8** the same author group is credited with the IBD RCT "Artificial intelligence–enabled microbiome-based precision nutrition in patients with inflammatory bowel disease."
- **Verified:** The real Kassem et al. (2025, _Nutrients_ 17(1):190) paper is "Investigation and Assessment of AI's Role in Nutrition—An Updated Narrative Review of the Evidence." The IBD RCT is by **Heithoff DM et al. (_Cell Rep Med_. 2023;4(5):101023)** and is already (correctly) reviewed in §3.2.5. The intermittent-fasting review is a different paper entirely.
- **Action:** Re-attribute both passages; remove the duplicated IBD row from Table-8 (it belongs in §3.2.5 only) or cross-reference it.

### 1.4 Agrawal et al. is mis-attributed (§3.2.6 text)

- The manuscript attributes "Nutritional Strategies for Managing Inflammation in Chronic Disease" to "Agrawal K, Goktas P, Holtkemper M, Beecks C, Kumar N".
- **Verified:** Agrawal et al. (2025, _Front Nutr_ 12:1553942) is "AI-driven transformation in food manufacturing: a pathway to sustainable efficiency and quality assurance" — about food-manufacturing AI, not anti-inflammatory diets.
- **Action:** Re-attribute; find the actual inflammation-review source or remove.

### 1.5 Kim DW et al. is mis-attributed (§3.2.6 text)

- The manuscript attributes "The Role of Dietary Patterns in Mental Health: Emerging Evidence" to "Kim DW, Park JS, Sharma K, Velazquez A, Li L, Ostrominski JW, et al."
- **Verified:** Kim DW et al. (2024, _Front Nutr_ 11) is "Qualitative evaluation of artificial intelligence-generated weight management diet plans." Meanwhile, Table-8 lists this same author group against a "Dietary Polyphenols and Cardiometabolic Health" row that does not appear anywhere in the text.
- **Action:** Re-attribute both; ensure every Table-8 row corresponds to a study actually discussed in §3.2.6.

### 1.6 Corrupted hypothesis text (Section 4.8)

> "**Ηψποτηεισι−1:** ... **Ηψποτηεισι−2:** ..."

- The word "Hypothesis" is rendered in Greek letters (Ηψποτηεισι). This is an encoding/copy artifact.
- **Action:** Restore "Hypothesis-1 / Hypothesis-2." Also reconsider framing: a systematic review does not test hypotheses; these read better as "Review Questions" or "Analytical Frames."

---

## 2. Methodology / PRISMA-Compliance Problems

| #   | Issue                                              | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| --- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M1  | **Search window contradicted by included studies** | Search stated as **January 2016 – June 2024** (Abstract, §2.1). At least **10 of the 30 included studies were published in 2025** and could not have been retrieved by a June-2024 search: Pradhan (Biomedicines 2025), Sajid (PLoS One 2025), Rouskas (Nutrients 2025), Kassem (Nutrients 2025), Agrawal (Front Nutr 2025), Danneel (Biomedicines 2025), Cabała (Metabolites 2025), Donovan (Crit Rev Food Sci Nutr 2025), Kenger (Iran J Public Health 2025), Tang (BMC Med Inform Decis Mak 2025). Either extend and re-run the search with a documented new date, or exclude post-cutoff studies. |
| M2  | **No protocol registration**                       | PRISMA-2020 item 24a: a systematic review should be registered (e.g., PROSPERO) and the registration cited. None is mentioned.                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| M3  | **No formal risk-of-bias / quality tool**          | §2.4 lists generic bias-mitigation statements but names no instrument (RoB 2, ROBINS-I, MMAT, Newcastle-Ottawa, etc.). Not reproducible.                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| M4  | **PRISMA flow numbers don't reconcile**            | 112 identified → 45 full-text → 30 included. No duplicate count, no exclusion counts with reasons at each stage (PRISMA-2020 item 16 requires these).                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| M5  | **Search strings not reproducible**                | Table-1: IEEE Xplore row has no full string; the Google Scholar string (`"AI-based personalized diet" + "systematic review"`) searches for reviews, not primary studies. No search execution dates, no per-database hit counts, no grey-literature sources despite the claim of grey literature in §2.5.                                                                                                                                                                                                                                                                                              |
| M6  | **No data-extraction table for all 30 studies**    | PRISMA item 19 expects a characteristics-of-studies table. The paper gives selective per-disease tables only.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| M7  | **"Systematic review" label not defensible**       | With the above gaps plus heavy reliance on narrative summaries of _other_ systematic/narrative reviews (e.g., Pérez-Beltrán, Rivera-Íñiguez, Pradhan, Cabała, Kassem, Kelly, Shinn, Donovan), the design is closer to an umbrella/narrative review. Either strengthen the protocol or relabel.                                                                                                                                                                                                                                                                                                        |
| M8  | **Synthesis of heterogeneous designs**             | Quantitative results are only summarized narratively with no stated synthesis method (no vote counting, no effect metrics, no meta-analysis decision rationale beyond "heterogeneity").                                                                                                                                                                                                                                                                                                                                                                                                               |
| M9  | **Thematic map (Figure 4) methodology missing**    | No tool (VOSviewer/biblioshiny), no parameters (period, threshold), no citation counts — the quadrant analysis is unverifiable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

---

## 3. Internal Inconsistencies

- **Dates:** Abstract and §2.1 say "2016–2024"; §2.2 Table-2 exclusion column says "Prior to 2017"; §4.2 says "2017 through 2024"; 10 included studies are 2025. Pick one window and make every element agree.
- **Geography (§2.6):** China "6 studies (10%)" — 6/30 = 20%. Italy 5 (8%) → 16.7%; USA 4 (7%) → 13.3%; India/Spain 3 (5%) → 10%. The percentages appear to be computed against ~60 _country participations_ while the text says "studies." The "remaining 79%" cannot be reconciled with the enumerated shares. Rewrite with one consistent denominator.
- **Metrics (Table-5 vs text):** ASCVD model reported as "AUC 0.8143" in text vs "88.4% accuracy" in Table-5 — different metrics presented as if equivalent.
- **AI-vs-nutritionist coding:** The binary label is applied inconsistently — e.g., Rein et al.'s ML-predicted diet is labeled "Nutritionist-Guided" (Table-3); the off-topic archaeology paper is "Nutritionist-guided" (Table-7); the PROTEIN app study (AI + nutritionist support) is "AI-Driven." §4.7's "16 AI-driven / 14 nutritionist-guided" split is not reproducible from the tables.
- **Qarajeh (§3.2.4):** "ChatGPT 4 had the highest accuracy (81%)… Bard AI and Bing Chat followed closely with 79% and 81%" — Bing Chat ties ChatGPT-4 at 81%; "highest" claim is muddled.
- **Section 3.2.5 synthesis:** "In contrast, the next three studies focus on AI-driven personalized nutrition" — only **two** nutrition studies follow (Heithoff, Rouskas).

---

## 4. Table Issues

| Table    | Problem                                                                                                                                                                                                                                                                         |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Table-1  | Non-reproducible strings (see M5); Google Scholar string targets "systematic review" papers.                                                                                                                                                                                    |
| Table-2  | Publication-period inclusion (2016–2024) vs exclusion (prior to 2017) contradiction.                                                                                                                                                                                            |
| Table-3  | Rein et al. mislabeled "Nutritionist-Guided" (it is an ML-based diet).                                                                                                                                                                                                          |
| Table-4  | "Key Genes Focused" column lists LDLR/APOB/PCSK9/etc. for the Gutiérrez-Esparza ML cohort study, but the text describes that study as using anthropometric/biochemical/dietary/psychological variables — no gene panel. Column appears fabricated or pasted from another paper. |
| Table-5  | Metric mismatch (accuracy vs AUC); "88.4% accuracy" unsupported by text.                                                                                                                                                                                                        |
| Table-7  | Includes the off-topic archaeology study; header "Table-7: Comparative Summary Table" is orphaned after the table body.                                                                                                                                                         |
| Table-8  | Row 1 credits the IBD RCT to Kassem et al. (should be Heithoff et al.); Row 5 "Dietary Polyphenols…" (Kim DW et al.) corresponds to no study in the text; the mental-health paper discussed in text is missing from the table.                                                  |
| Table-11 | Redundant with §3.3/Table-10; bullets after it (16 vs 14 split) are unsupported by consistent coding.                                                                                                                                                                           |

---

## 5. Writing Quality & AI-Generation Artifacts

The prose shows pervasive signs of AI-generated drafting (per the _humanizer_ checklist):

- **Em-dash overuse** and rule-of-three constructions ("scalability, data integration, and precision").
- **Inflated/vague evaluation language:** "AI technologies showed excellent capabilities," "promising but still fragmented," "exceptional accuracy," "synergistic possibilities," "client contentment" (→ patient satisfaction), "expansion potential" (→ scalability), "situational appropriateness."
- **Repetitive template structure:** every disease section is the same pattern (3–4 study summaries → synthesis paragraph → comparison table), giving a stitched-together feel rather than an integrated analysis.
- **Broken/awkward headings:** "3.2.3 Critical Analysis for Personalized Dietary in Heart Objectives" (→ …in Cardiovascular Disease); "2.7Thematic Map" (missing space); Methodology main heading is unnumbered while its subsections are 2.1–2.8.
- **Citation style chaos:** in-text parenthetical author lists "(Pradhan N, et al.; Han K, et al.; King A, et al.)" with a numbered reference list that is never referenced by number; references #1 is empty; list runs #2–#31 for "30 studies"; Vancouver-style entries mixed with parenthetical fragments; no DOIs.
- **Encoding corruption:** the Greek-letter "Ηψποτηεισι" (§4.8) and a stray `\[.` in §3.2.2.
- **Duplication:** §2.7 and §2.7.1 restate the same quadrant descriptions; Figure-1 caption appears twice.

---

## 6. What Works (preserve these)

- The **core thesis** — AI and human nutrition expertise are complementary; hybrid "cooperative intelligence" models are the promising direction — is timely, reasonable, and supported by the _overall_ tenor of the corpus.
- The **disease-domain organization** (diabetes → lipids/CVD → CKD → microbiome → COVID) is a sensible structure for a clinical review.
- Several study summaries are accurate and well-condensed (e.g., Shamanna digital-twin, Bermingham RCT, Heithoff IBD RCT, Rouskas PROTEIN app, García-Ordás COVID clustering).
- The limitations section (§4) already anticipates most of the valid criticisms; it needs only to be reconciled with the actual data (dates, counts).

---

## 7. Prioritized Action Plan

**Blocking (do before any resubmission):**

1. Delete the Pelton archaeology study from §3.2.5, Table-7, and references.
2. Fix the PRISMA citation → Page MJ et al. (2021), _BMJ_ 372:n71.
3. Correct all mis-attributions: Kassem (§3.2.6 + Table-8), Agrawal (§3.2.6), Kim DW (§3.2.6 + Table-8); remove the duplicate IBD row from Table-8.
4. Fix the hypothesis text corruption; reframe hypotheses as review questions.
5. Resolve the search-window contradiction: extend the documented search to cover the 2025 studies or exclude them; make Abstract, §2.1, §2.2, §4.2, and the reference list agree on one window.

**High:** 6. Rebuild the PRISMA flow with duplicate counts and exclusion reasons; add search execution dates and complete per-database strings. 7. Add a formal risk-of-bias instrument and a characteristics-of-studies table. 8. State the thematic-map methodology (tool and parameters); state a synthesis method. 9. Fix the geography percentages to a consistent denominator. 10. Align Table-5 metrics with text (AUC vs accuracy); correct Table-4 gene column; re-derive the AI/nutritionist coding and the 16/14 split.

**Medium:** 11. Normalize citation style (numbered in-text, Vancouver reference list, DOIs, no empty entry #1). 12. De-AI the prose (remove em-dash tics, inflated adjectives, template repetition); run through the _humanize-academic-writing_ pass. 13. Fix headings, numbering, duplicated captions, stray bullets/`\[.`, and orphaned Table-7 header.

---

## 8. Verdict Summary

| Dimension                         | Rating              | Notes                                                                    |
| --------------------------------- | ------------------- | ------------------------------------------------------------------------ |
| Novelty/relevance of question     | Good                | Hybrid AI–human nutrition is an active, publishable question             |
| Methodological rigor (as written) | **Poor**            | Does not currently meet PRISMA-2020; window contradicts included studies |
| Evidence integrity                | **Poor**            | 5+ verified citation–content mismatches; 1 off-topic study               |
| Analysis depth                    | Fair                | Per-study summaries OK; synthesis is repetitive and uncritical in places |
| Writing                           | Needs work          | Heavy AI artifacts; inconsistent terminology                             |
| **Overall**                       | **Major revisions** | All §7 Blocking + High items before resubmission                         |
