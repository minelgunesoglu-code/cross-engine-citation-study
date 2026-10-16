# Cross-Engine Citation Study

**Rounds one and two: which sources ChatGPT, Perplexity, Gemini and Google's AI Overview cite, and which brands they recommend, for the same twelve B2B SaaS buyer questions**

| | |
|---|---|
| **Article** | https://ismybrandinai.com/do-ai-engines-cite-the-same-sources |
| **Repository** | https://github.com/minelgunesoglu-code/cross-engine-citation-study |
| **Archive** | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23427370.svg)](https://doi.org/10.5281/zenodo.23427370) concept DOI, resolves to the latest version |
| **Collected** | Round one 19 June 2026 (sources only); round two 6 to 7 August 2026 (sources and brands). By hand, one run per engine-question pair |
| **Published** | Round one 19 June 2026; round two 9 August 2026 |
| **Engines** | ChatGPT (free tier, web search on; temporary chat in round two), Perplexity (default web search), Gemini (Flash model in round one), Google AI Overview as shown in standard search results |
| **Sample** | Twelve B2B SaaS buyer questions in four intents. Round one: 27 runs (Perplexity 12, ChatGPT 6, Gemini 6, AI Overview 3). Round two: 48 runs, every question on every engine |
| **Headline** | On the seven open recommendation and alternatives questions of round two, the four engines agreed on **32%** of the brands they recommended and **1%** of the sources they cited. |
| **Licence** | CC BY 4.0 (`LICENSE`); see `LICENCE-NOTES.md` for what it does and does not cover |

The same buyer questions ("best CRM for startups", "HubSpot vs Salesforce", "how to
reduce customer churn", "cheaper alternatives to HubSpot") were put to four AI
engines, and every source each engine displayed was written down in order. Round
two also recorded the brands each answer recommended, in order, and gave every
source a type.

**What is measured:** which sources each engine displayed for each question, how
far the engines share them, which brands they named, and how much of Perplexity's
source list changed in seven weeks.
**What is NOT measured:** whether a cited page is accurate, why an engine chose a
source, and how stable any single answer is between runs: every figure comes from
one run per engine-question pair.

**Round three** (October 2026, five engines, 50 different questions) is not in
this repository. It is archived with The AI Answer Evidence Index,
[doi:10.5281/zenodo.23238429](https://doi.org/10.5281/zenodo.23238429), and is
not pooled with these two rounds.

---

## 1. Findings

All figures below are the ones published in the article. Each is recounted from
the rows by `notes/verify.py`; see `notes/reproduction-check.md`.

### The engines recommend the same brands but cite different sources (round two)

| Question | Brands all four named | Brand overlap | Sources all four cited | Source overlap |
| --- | --- | ---: | --- | ---: |
| best CRM for startups | HubSpot, Pipedrive | 22% | none | 0% |
| best project management software | Asana, ClickUp, Trello | 38% | zapier.com, project-management.com | 6% |
| best email marketing platform | ActiveCampaign, Kit | 25% | none | 0% |
| best AI writing tools | ChatGPT, Claude | 25% | none | 0% |
| Salesforce alternatives | HubSpot, Pipedrive, Zoho, MS Dynamics | 36% | none | 0% |
| cheaper alternatives to HubSpot | Zoho, Pipedrive, EngageBay | 30% | none | 0% |
| best free project management tools | Trello, ClickUp, Asana | 50% | none | 0% |
| **Average** | | **32%** | | **1%** |

Overlap is Jaccard similarity: items named by all four engines divided by the
distinct items named by any of them. The three "X vs Y" questions are left out
because the question names the brands, "how to reduce customer churn" because no
engine named a brand, and "how to choose a CRM" because Perplexity named none.

### Round two in numbers

| | |
|---|---|
| Citations logged | 322 |
| Distinct sources | 193 |
| Cited by one engine only | 151 (78.2%) |
| Cited by all four engines, pooled | 4 (2.1%) |
| Runs that showed no source | 7 of 48 |

| Engine | Citations | Distinct sources | Average per answer |
|---|---:|---:|---:|
| Perplexity | 138 | 106 | 11.5 |
| Google AI Overview | 104 | 77 | 8.7 |
| ChatGPT | 43 | 35 | 3.6 |
| Gemini | 37 | 35 | 3.1 |

By source type: vendor's own site 156 (48.4%), independent listicle or blog 85
(26.4%), review media 50 (15.5%), YouTube 16 (5.0%), Reddit 14 (4.3%), forum 1
(0.3%). Averaged across the twelve questions, watching ChatGPT alone shows 14% of
a question's cited set, Perplexity and the AI Overview together 82%, and those
two plus ChatGPT 91%.

### Round one: almost no shared sources

On the six questions put to ChatGPT, Perplexity and Gemini, no domain was cited by
all three. Perplexity and ChatGPT shared between none and two domains per
question.

### A source list turns over in seven weeks (Perplexity, June to August)

Perplexity cited 80 distinct sources across the twelve questions in June; 42 of
them were still cited in August, so 48% were gone (pooled Jaccard 0.29). Question
by question, 58% of June's source slots turned over. Every question kept at least
one source.

---

## 2. What is in this repository

```
data/cross-engine-brands-sources-2026-06.csv    round one: 27 rows, one per engine-question pair
data/cross-engine-brands-sources-2026-06.json   the same rows plus that round's metadata and limits
data/cross-engine-brands-sources-2026-08.csv    round two: 48 rows, one per engine-question pair
data/cross-engine-brands-sources-2026-08.json   the same rows plus the run conditions, the type key and the limits
notes/
  verify.py                 recounts the published figures from the rows
  reproduction-check.md     the result of that recount
  zenodo-release-steps.md   how this repository is archived on Zenodo
```

This is a data package with method notes. The August files are byte-identical to
the ones published on the site. In the June files, seven short collection notes
written in Turkish were translated into English for this archive; nothing else
was changed, and the before and after of each is listed in
`notes/reproduction-check.md`. The data were collected by hand and no analysis
code is included; `notes/verify.py` was written afterwards, to check every
published figure against the rows.

### Columns

Round one: `question_id`, `question`, `intent`, `engine`, `run_date`, `sources`
(as displayed, separated by ` | `), `source_count`, `collection_note`.

Round two: `question_id`, `question`, `intent`, `engine`, `run_date`,
`brands_in_order` (separated by ` | `), `brand_count`, `sources_with_type` (each
source followed by its type code in brackets), `source_count`.

Type codes: `V` vendor's own site, `RM` review or authority media, `L` independent
listicle or niche blog, `R` Reddit, `F` other forum, `YT` YouTube, `WK` reference
work.

### Rules worth knowing before recounting

- Sources are counted as distinct strings exactly as the files record them, with
  no subdomain collapsing: blog.hubspot.com and hubspot.com count separately.
- Some sources in round one are product or publication names the engine showed
  without a URL ("Best CRM Reviews", "UpliftGTM"); they are kept as written.
- Brand names get light normalization: "HubSpot CRM" counts as HubSpot, and the
  Salesforce editions count as Salesforce. The full mapping is `BRAND_ALIASES` in
  `notes/verify.py`.
- ChatGPT and the AI Overview hide some sources behind a "+N" badge, and several
  of Perplexity's June panels were truncated, so source counts are what was
  visible: a floor, not a total.

### Known defects in the round one files

These are recorded, not corrected. None affects a published figure.

- The last row of the June CSV (question 12, Perplexity) has an unquoted comma in
  `collection_note`, so a CSV reader splits the note into an extra column. The
  JSON holds the full note.
- Four `sources` values in round one carry a stray double quote left from
  transcription (question 2 Gemini, question 5 AI Overview, question 9 AI
  Overview, question 11 Gemini).

---

## 3. Recounting the figures

```bash
python3 notes/verify.py
```

Python 3.8 or later, standard library only. Run it from the repository root. It
prints each published figure next to the recounted one and ends with the number
of checks that match.

---

## 4. Limits

- One run per engine-question pair; a single run cannot separate a stable
  pattern from a lucky draw. The 32% against 1% gap is large; the per-question
  percentages are not precise.
- One market (US English), one sector (B2B SaaS), two moments in time.
- Round one is smaller and uneven: Perplexity answered all twelve questions,
  ChatGPT and Gemini six, the AI Overview three. Do not quote it as twelve
  questions on four engines.
- The churn figures are Perplexity only, the one engine with all twelve
  questions in both rounds, and measure churn among visible sources.
- Which rows can be re-opened: in round two, all twelve Gemini conversations,
  two of twelve Perplexity answers, no ChatGPT answers (temporary chats leave no
  transcript) and no AI Overviews.

---

## 5. Citing this

> Gunesoglu, M. (2026). *Cross-Engine Citation Study, rounds one and two* [Data set].
> Is My Brand in AI. https://ismybrandinai.com/do-ai-engines-cite-the-same-sources

If a count here does not match what you get from the files, open an issue and a
correction will be published saying what changed.
