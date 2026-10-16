# Reproduction check

Checked on 17 October 2026 against the article as published at
https://ismybrandinai.com/do-ai-engines-cite-the-same-sources (round one
published 19 June 2026, round two 9 August 2026, last updated 10 October 2026).
Only the sections on rounds one and two were checked; round three is archived
elsewhere.

## Result

**Every figure checked matches.** `notes/verify.py` runs 88 checks, the figures
published for rounds one and two plus consistency checks on the files, and all
88 pass. No figure was changed.

## What was checked

1. **The files are the published files, with seven notes translated.** The site
   publishes these four files (SHA-256):

    72dad27d051261219ce201b8ca75c430e98f2ec7865b9a849c4913f5590a9be8  cross-engine-brands-sources-2026-06.csv
    5caa399abd4d51c3c5e9efad2414014f4b9504cd4cfcf24375a050c9c06e35e6  cross-engine-brands-sources-2026-06.json
    6f16365e7a33a9d4f4a2cf0de7bcf3070b240e25369976c24cf15439c008c99b  cross-engine-brands-sources-2026-08.csv
    e22b6db558bb8cfeca40c62376e531503586e0988addbccaad589cdbce0b45fe  cross-engine-brands-sources-2026-08.json

   The August files in this archive are byte-identical to them. In the June CSV
   and JSON, seven short notes written in Turkish during collection were
   translated into English, the same seven in both files. Nothing else was
   changed, including the defects described in the README. The translated fields:

   | Question | Engine | Field | Value in this archive |
   |---|---|---|---|
   | 1 | Perplexity | `collection_note` | `+ zendesk regional duplicates; "more" hidden` |
   | 2 | Perplexity | `collection_note` | `+ more hidden` |
   | 3 | Perplexity | `collection_note` | `+ more hidden` |
   | 4 | Perplexity | `collection_note` | `+ more hidden` |
   | 5 | Gemini | `collection_note` | `2 sources` |
   | 6 | Perplexity | `collection_note` | `**youtube.com ×3**, one in Japanese; no Reddit` |
   | 9 | Google AI Overview | `sources` | `SurveyMonkey +2" (+ probably SuperOffice)` |

   The "Before" column quotes the published text so the change can be checked;
   it is the only place the original wording appears. No figure uses
   `collection_note`, and the question 9 value counts as one source before and
   after. SHA-256 of the archive copy:

    4e28d8353105d8a0f296079e6ccca76aefff1a408edb681b940d1aec5ff35180  data/cross-engine-brands-sources-2026-06.csv
    e4c06c400df764342972c6a56a4ca74881e826b0a8b3fa66205955110733d7d4  data/cross-engine-brands-sources-2026-06.json
    6f16365e7a33a9d4f4a2cf0de7bcf3070b240e25369976c24cf15439c008c99b  data/cross-engine-brands-sources-2026-08.csv
    e22b6db558bb8cfeca40c62376e531503586e0988addbccaad589cdbce0b45fe  data/cross-engine-brands-sources-2026-08.json

2. **The CSV and the JSON agree** for each round, once the one June note split by
   an unquoted comma is rejoined (see the README, "Known defects").

3. **Every figure for rounds one and two recounts from the rows.** Output of
   `python3 notes/verify.py`:

```
NOTE  June CSV Q12 Perplexity: collection_note split by an unquoted comma; the remainder [' listicles and vendors'] falls into an extra column. The JSON has the full note.
[OK ] June CSV rows equal June JSON rows (after rejoining that note): published True, computed True
[OK ] August CSV rows equal August JSON rows: published True, computed True

== Round two, 6 to 7 August 2026 ==
[OK ] runs: published 48, computed 48
[OK ] questions x engines: published (12, 4), computed (12, 4)
[OK ] citations logged: published 322, computed 322
[OK ] source_count column sums to the citations: published 322, computed 322
[OK ] distinct sources: published 193, computed 193
[OK ] cited by one engine only: published (151, 78.2), computed (151, 78.2)
[OK ] cited by all four engines (pooled): published (4, 2.1), computed (4, 2.1)
       pooled four-engine sources: ['monday.com', 'project-management.com', 'reddit.com', 'zapier.com']
[OK ] runs with no source: published 7, computed 7
[OK ] Perplexity: citations, distinct, average per answer: published (138, 106, 11.5), computed (138, 106, 11.5)
[OK ] Google AI Overview: citations, distinct, average per answer: published (104, 77, 8.7), computed (104, 77, 8.7)
[OK ] ChatGPT: citations, distinct, average per answer: published (43, 35, 3.6), computed (43, 35, 3.6)
[OK ] Gemini: citations, distinct, average per answer: published (37, 35, 3.1), computed (37, 35, 3.1)
[OK ] type vendor's own site: published (156, 48.4), computed (156, 48.4)
[OK ] type listicle or blog: published (85, 26.4), computed (85, 26.4)
[OK ] type review media: published (50, 15.5), computed (50, 15.5)
[OK ] type YouTube: published (16, 5.0), computed (16, 5.0)
[OK ] type Reddit: published (14, 4.3), computed (14, 4.3)
[OK ] type forum: published (1, 0.3), computed (1, 0.3)
[OK ] Reddit + YouTube in AI Overview citations: published (18, 104, 17.3), computed (18, 104, 17.3)
[OK ] ChatGPT Reddit + YouTube share, % (next highest): published 7, computed 7
       ChatGPT: Reddit + YouTube 7.0%
       Perplexity: Reddit + YouTube 5.8%
       Gemini: Reddit + YouTube 2.7%
       Google AI Overview: Reddit + YouTube 17.3%
       share of citations to non-vendor sites: {'ChatGPT': 33, 'Perplexity': 54, 'Gemini': 57, 'Google AI Overview': 54}
[OK ] Perplexity, Gemini and AI Overview non-vendor share within 54% to 57%: published True, computed True
[OK ] coverage: ChatGPT alone, %: published 14, computed 14
[OK ] coverage: Perplexity + AI Overview, %: published 82, computed 82
[OK ] coverage: those two plus ChatGPT, %: published 91, computed 91
[OK ] Gemini's unique contribution, points: published 9, computed 9
[OK ] Q1 best CRM for startups: brands all four named: published {'pipedrive', 'hubspot'}, computed {'pipedrive', 'hubspot'}
[OK ] Q1: brand overlap %, source overlap %: published (22, 0), computed (22, 0)
[OK ] Q2 best project management software for small teams: brands all four named: published {'trello', 'asana', 'clickup'}, computed {'trello', 'asana', 'clickup'}
[OK ] Q2: brand overlap %, source overlap %: published (38, 6), computed (38, 6)
[OK ] Q2 sources all four cited: published {'project-management.com', 'zapier.com'}, computed {'project-management.com', 'zapier.com'}
[OK ] Q3 best email marketing platform: brands all four named: published {'activecampaign', 'kit'}, computed {'activecampaign', 'kit'}
[OK ] Q3: brand overlap %, source overlap %: published (25, 0), computed (25, 0)
[OK ] Q4 best AI writing tools: brands all four named: published {'claude', 'chatgpt'}, computed {'claude', 'chatgpt'}
[OK ] Q4: brand overlap %, source overlap %: published (25, 0), computed (25, 0)
[OK ] Q10 Salesforce alternatives: brands all four named: published {'ms dynamics', 'pipedrive', 'zoho', 'hubspot'}, computed {'ms dynamics', 'pipedrive', 'zoho', 'hubspot'}
[OK ] Q10: brand overlap %, source overlap %: published (36, 0), computed (36, 0)
[OK ] Q11 cheaper alternatives to HubSpot: brands all four named: published {'pipedrive', 'zoho', 'engagebay'}, computed {'pipedrive', 'zoho', 'engagebay'}
[OK ] Q11: brand overlap %, source overlap %: published (30, 0), computed (30, 0)
[OK ] Q12 best free project management tools: brands all four named: published {'trello', 'asana', 'clickup'}, computed {'trello', 'asana', 'clickup'}
[OK ] Q12: brand overlap %, source overlap %: published (50, 0), computed (50, 0)
[OK ] average brand overlap, %: published 32, computed 32
[OK ] average source overlap, %: published 1, computed 1
[OK ] questions with no shared source: published 6, computed 6
[OK ] all four named HubSpot / Zoho / Salesforce / Pipedrive (times): published (2, 2, 0, 3), computed (2, 2, 0, 3)
[OK ] most frequent four-engine brand: published 'pipedrive', computed 'pipedrive'
[OK ] excluded questions (three comparisons, two how-to): published [5, 6, 7, 8, 9], computed [5, 6, 7, 8, 9]
[OK ] Q11: engines citing Searchlab: published {'Gemini', 'ChatGPT', 'Perplexity'}, computed {'Gemini', 'ChatGPT', 'Perplexity'}
[OK ] Q11: engines citing AI Topia: published 2, computed 2
[OK ] Q1: engines citing hubspot.com: published 3, computed 3
[OK ] Q5 source counts ChatGPT/Perplexity/Gemini/AIO: published (0, 13, 6, 8), computed (0, 13, 6, 8)
[OK ] Q6 source counts ChatGPT/Perplexity/Gemini/AIO: published (0, 10, 4, 11), computed (0, 10, 4, 11)
[OK ] Q7 source counts ChatGPT/Perplexity/Gemini/AIO: published (0, 10, 0, 9), computed (0, 10, 0, 9)
[OK ] Q8 source counts ChatGPT/Perplexity/Gemini/AIO: published (0, 9, 0, 7), computed (0, 9, 0, 7)
[OK ] Q9 source counts ChatGPT/Perplexity/Gemini/AIO: published (0, 10, 1, 6), computed (0, 10, 1, 6)
[OK ] Perplexity sources per answer, round two range: published (8, 19), computed (8, 19)
[OK ] highest single count on a comparison question (Perplexity, HubSpot vs Salesforce): published 13, computed 13
[OK ] comparison questions, other three engines' range: published (4, 13), computed (4, 13)
[OK ] ChatGPT sources per answer, round two (spectrum table): published (0, 9, 2.5), computed (0, 9, 2.5)
       Gemini sources per answer, round two: 0 to 6
[OK ] Gemini on 'how to choose a CRM': nine brands, no source: published (9, 0), computed (9, 0)

== Round one, 19 June 2026 ==
[OK ] June rows: published 27, computed 27
[OK ] coverage: Perplexity / ChatGPT / Gemini / AIO questions: published (12, 6, 6, 3), computed (12, 6, 6, 3)
[OK ] Q1 Perplexity list: published 'crm.org, tech.co, zendesk.com, techradar.com, hubspot.com, digitalocean.com, salesflare.com, blog.hubspot.com', computed 'crm.org, tech.co, zendesk.com, techradar.com, hubspot.com, digitalocean.com, salesflare.com, blog.hubspot.com'
[OK ] Q1: sites in more than one list: published {'techradar.com', 'reddit.com'}, computed {'techradar.com', 'reddit.com'}
[OK ] Q1: Gemini overlaps with the others: published 0, computed 0
[OK ] Q1: sources cited by all four: published 0, computed 0
[OK ] six head-to-head questions: published [1, 2, 5, 7, 9, 11], computed [1, 2, 5, 7, 9, 11]
[OK ] Q1 Perplexity and ChatGPT shared: published {'techradar.com'}, computed {'techradar.com'}
[OK ] Q2 Perplexity and ChatGPT shared: published set(), computed set()
[OK ] Q5 Perplexity and ChatGPT shared: published {'forbes.com', 'reddit.com'}, computed {'forbes.com', 'reddit.com'}
[OK ] Q7 Perplexity and ChatGPT shared: published {'technologyadvice.com'}, computed {'technologyadvice.com'}
[OK ] Q9 Perplexity and ChatGPT shared: published set(), computed set()
[OK ] Q11 Perplexity and ChatGPT shared: published {'reddit.com'}, computed {'reddit.com'}
[OK ] domains cited by all three (ChatGPT, Perplexity, Gemini) on any of the six: published 0, computed 0
[OK ] Perplexity 8 to 10 and ChatGPT 4 to 7 on the six: published ((8, 10), (4, 7)), computed ((8, 10), (4, 7))
[OK ] mean shared per question under one: published True, computed True
[OK ] Gemini sources on 'how to reduce customer churn': published 0, computed 0
[OK ] Gemini sources per answer, round one (spectrum table): published (0, 4), computed (0, 4)
[OK ] Perplexity sources per answer, round one (spectrum table): published (8, 10), computed (8, 10)
       ChatGPT sources per answer, round one: 4 to 7, median 7.0

== Seven-week churn, Perplexity, June to August ==
[OK ] distinct Perplexity sources in June (pooled): published 80, computed 80
[OK ] still cited in August (pooled): published 42, computed 42
[OK ] gone, %: published 48, computed 48
[OK ] pooled Jaccard: published 0.29, computed 0.29
[OK ] question by question, share of June source slots gone, %: published 58, computed 58
[OK ] every question kept at least one source: published True, computed True
[OK ] most volatile question (Q4 best AI writing tools), %: published (4, 90), computed (4, 90)
[OK ] most stable question (Q5 HubSpot vs Salesforce), %: published (5, 25), computed (5, 25)
       survivors include: ['project-management.com', 'techradar.com', 'thedigitalprojectmanager.com', 'youtube.com', 'zapier.com']

88 of 88 checks match.
```

## Notes on the counts

- **Where each figure comes from.** The engine summary table in the article
  ("sources per answer") mixes the rounds: Perplexity's 8 to 10 and Gemini's 0 to
  4 are round one; ChatGPT's 0 to 9 with a median of 2.5 is round two (in round
  one ChatGPT cited 4 to 7, median 7). Each figure matches its round.
- **Pooled against per-question.** "Cited by all four engines" is 4 sources
  pooled across the twelve questions (monday.com, project-management.com,
  reddit.com, zapier.com); on a single question it is the two on the project
  management question.
- **Churn.** Sources are compared as recorded strings, without subdomain
  collapsing, as the article states. The per-question figure of 58% is the share
  of June source slots, summed across the twelve questions, that were gone in
  August.
- **Brand normalization.** `BRAND_ALIASES` in `notes/verify.py` is the mapping
  used when the brand figures were first counted. "Monday CRM" (Perplexity,
  question 11) is not merged with monday.com; merging it changes no published
  figure because no other engine named monday.com on that question.
