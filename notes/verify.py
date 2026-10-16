"""Recount the figures published for rounds one and two of the Cross-Engine Citation Study.

This script was written after publication, to check the article's figures
against the published rows. The data were collected by hand. Standard library only. Run from the repository root:

    python3 notes/verify.py

Counting rules, as the article states them:
- Sources are distinct strings exactly as the files record them, with no
  subdomain collapsing (blog.hubspot.com and hubspot.com count separately).
- Overlap is Jaccard similarity: items named by all four engines, divided by
  the distinct items named by any of them.
- Brand names get light normalization ("HubSpot CRM" counts as HubSpot, the
  Salesforce editions count as Salesforce). The table BRAND_ALIASES below is
  the mapping used when the brand figures were first counted.
"""
import csv
import json
import re
import statistics
from collections import Counter
from pathlib import Path

DATA = Path("data")
JUNE_CSV = DATA / "cross-engine-brands-sources-2026-06.csv"
JUNE_JSON = DATA / "cross-engine-brands-sources-2026-06.json"
AUG_CSV = DATA / "cross-engine-brands-sources-2026-08.csv"
AUG_JSON = DATA / "cross-engine-brands-sources-2026-08.json"

ENGINES = ["ChatGPT", "Perplexity", "Gemini", "Google AI Overview"]

BRAND_ALIASES = {
    "hubspot crm": "hubspot",
    "zoho crm": "zoho", "zoho crm / zoho one": "zoho",
    "salesforce starter": "salesforce", "salesforce essentials": "salesforce",
    "salesforce sales cloud": "salesforce",
    "monday sales crm": "monday.com", "monday": "monday.com",
    "microsoft dynamics 365": "ms dynamics", "microsoft": "ms dynamics", "dynamics 365": "ms dynamics",
    "kit (convertkit)": "kit", "kit (formerly convertkit)": "kit",
    "kit (convertkit) & beehiiv": "kit", "kit / beehiiv": "kit",
    "google gemini": "gemini", "jasper / surfer seo": "jasper", "close crm": "close",
    "attio / twenty": "attio", "grammarly ai": "grammarly",
}

checks = []


def check(label, published, computed):
    ok = published == computed
    checks.append(ok)
    print(f"[{'OK ' if ok else 'DIFF'}] {label}: published {published!r}, computed {computed!r}")


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def same_rows(csv_rows, json_rows):
    norm = [{k: ("" if v is None else str(v)) for k, v in r.items()} for r in json_rows]
    return norm == csv_rows


def split(field):
    return [x.strip() for x in field.split(" | ") if x.strip()]


def brand(name):
    n = name.strip().lower()
    return BRAND_ALIASES.get(n, n)


def jaccard_all(sets):
    union = set().union(*sets)
    return (len(set.intersection(*sets)) / len(union)) if union else 0.0


june = read_csv(JUNE_CSV)
aug = read_csv(AUG_CSV)
# Known defect in the June CSV: the last row's collection_note contains an
# unquoted comma, so a CSV reader splits it and puts the remainder in an extra
# column. The JSON holds the full note. No figure uses collection_note.
for r in june:
    extra = r.pop(None, None)
    if extra:
        print(f"NOTE  June CSV Q{r['question_id']} {r['engine']}: collection_note split by an unquoted comma; "
              f"the remainder {extra!r} falls into an extra column. The JSON has the full note.")
        r["collection_note"] = r["collection_note"] + "," + ",".join(extra)
check("June CSV rows equal June JSON rows (after rejoining that note)", True,
      same_rows(june, json.loads(JUNE_JSON.read_text())["rows"]))
check("August CSV rows equal August JSON rows", True, same_rows(aug, json.loads(AUG_JSON.read_text())["rows"]))

# ---------------------------------------------------------------- round two
print("\n== Round two, 6 to 7 August 2026 ==")
cites = {}   # (qid, engine) -> list of (source, type)
for r in aug:
    items = []
    for x in split(r["sources_with_type"]):
        m = re.match(r"^(.*?)\s*\(([A-Z]+)\)$", x)
        items.append((m.group(1), m.group(2)) if m else (x, ""))
    check_count = len(items) == int(r["source_count"])
    if not check_count:
        print(f"       source_count differs from the list on Q{r['question_id']} {r['engine']}")
    cites[(int(r["question_id"]), r["engine"])] = items
    r["_brands"] = {brand(b) for b in split(r["brands_in_order"])}

QIDS = sorted({q for q, _ in cites})
check("runs", 48, len(aug))
check("questions x engines", (12, 4), (len(QIDS), len({e for _, e in cites})))
all_cites = [c for v in cites.values() for c in v]
check("citations logged", 322, len(all_cites))
check("source_count column sums to the citations", 322, sum(int(r["source_count"]) for r in aug))
engines_by_source = {}
for (q, e), items in cites.items():
    for s, _ in items:
        engines_by_source.setdefault(s, set()).add(e)
check("distinct sources", 193, len(engines_by_source))
one = sum(len(v) == 1 for v in engines_by_source.values())
four = sum(len(v) == 4 for v in engines_by_source.values())
check("cited by one engine only", (151, 78.2), (one, round(100 * one / len(engines_by_source), 1)))
check("cited by all four engines (pooled)", (4, 2.1), (four, round(100 * four / len(engines_by_source), 1)))
print("       pooled four-engine sources:", sorted(s for s, v in engines_by_source.items() if len(v) == 4))
check("runs with no source", 7, sum(not v for v in cites.values()))

published_engine = {"Perplexity": (138, 106, 11.5), "Google AI Overview": (104, 77, 8.7),
                    "ChatGPT": (43, 35, 3.6), "Gemini": (37, 35, 3.1)}
for e, pub in published_engine.items():
    items = [c for (q, en), v in cites.items() if en == e for c in v]
    check(f"{e}: citations, distinct, average per answer", pub,
          (len(items), len({s for s, _ in items}), round(len(items) / 12, 1)))

types = Counter(t for _, t in all_cites)
for code, label, n, share in [("V", "vendor's own site", 156, 48.4), ("L", "listicle or blog", 85, 26.4),
                              ("RM", "review media", 50, 15.5), ("YT", "YouTube", 16, 5.0),
                              ("R", "Reddit", 14, 4.3), ("F", "forum", 1, 0.3)]:
    check(f"type {label}", (n, share), (types[code], round(100 * types[code] / len(all_cites), 1)))


def engine_items(e):
    return [c for (q, en), v in cites.items() if en == e for c in v]


aio = engine_items("Google AI Overview")
ry = sum(t in ("R", "YT") for _, t in aio)
check("Reddit + YouTube in AI Overview citations", (18, 104, 17.3), (ry, len(aio), round(100 * ry / len(aio), 1)))
cg = engine_items("ChatGPT")
check("ChatGPT Reddit + YouTube share, % (next highest)", 7,
      round(100 * sum(t in ("R", "YT") for _, t in cg) / len(cg)))
for e in ENGINES:
    items = engine_items(e)
    print(f"       {e}: Reddit + YouTube {100 * sum(t in ('R', 'YT') for _, t in items) / len(items):.1f}%")

nonvendor = {e: round(100 * sum(t != "V" for _, t in engine_items(e)) / len(engine_items(e))) for e in ENGINES}
print(f"       share of citations to non-vendor sites: {nonvendor}")
check("Perplexity, Gemini and AI Overview non-vendor share within 54% to 57%", True,
      all(54 <= nonvendor[e] <= 57 for e in ["Perplexity", "Gemini", "Google AI Overview"]))


def qsets(q):
    return {e: {s for s, _ in cites[(q, e)]} for e in ENGINES}


def coverage(watch):
    shares = []
    for q in QIDS:
        s = qsets(q)
        union = set().union(*s.values())
        if union:
            shares.append(len(set().union(*(s[e] for e in watch))) / len(union))
    return round(100 * statistics.mean(shares))


check("coverage: ChatGPT alone, %", 14, coverage(["ChatGPT"]))
check("coverage: Perplexity + AI Overview, %", 82, coverage(["Perplexity", "Google AI Overview"]))
check("coverage: those two plus ChatGPT, %", 91, coverage(["Perplexity", "Google AI Overview", "ChatGPT"]))
check("Gemini's unique contribution, points", 9, 100 - coverage(["Perplexity", "Google AI Overview", "ChatGPT"]))

# Brand and source overlap on the seven recommendation and alternatives questions.
SEVEN = [1, 2, 3, 4, 10, 11, 12]
published_overlap = {1: (22, 0), 2: (38, 6), 3: (25, 0), 4: (25, 0), 10: (36, 0), 11: (30, 0), 12: (50, 0)}
published_common = {1: {"hubspot", "pipedrive"}, 2: {"asana", "clickup", "trello"}, 3: {"activecampaign", "kit"},
                    4: {"chatgpt", "claude"}, 10: {"hubspot", "pipedrive", "zoho", "ms dynamics"},
                    11: {"zoho", "pipedrive", "engagebay"}, 12: {"trello", "clickup", "asana"}}
b_j, s_j, common_counter = [], [], Counter()
for q in SEVEN:
    bsets = [next(r["_brands"] for r in aug if int(r["question_id"]) == q and r["engine"] == e) for e in ENGINES]
    ssets = list(qsets(q).values())
    bj, sj = jaccard_all(bsets), jaccard_all(ssets)
    b_j.append(bj)
    s_j.append(sj)
    common = set.intersection(*bsets)
    common_counter.update(common)
    question = next(r["question"] for r in aug if int(r["question_id"]) == q)
    check(f"Q{q} {question}: brands all four named", published_common[q], common)
    check(f"Q{q}: brand overlap %, source overlap %", published_overlap[q], (round(100 * bj), round(100 * sj)))
    if q == 2:
        check("Q2 sources all four cited", {"zapier.com", "project-management.com"}, set.intersection(*ssets))
check("average brand overlap, %", 32, round(100 * statistics.mean(b_j)))
check("average source overlap, %", 1, round(100 * statistics.mean(s_j)))
check("questions with no shared source", 6, sum(j == 0 for j in s_j))
check("all four named HubSpot / Zoho / Salesforce / Pipedrive (times)", (2, 2, 0, 3),
      (common_counter["hubspot"], common_counter["zoho"], common_counter["salesforce"], common_counter["pipedrive"]))
check("most frequent four-engine brand", "pipedrive", common_counter.most_common(1)[0][0])
excluded = [q for q in QIDS if q not in SEVEN]
check("excluded questions (three comparisons, two how-to)", [5, 6, 7, 8, 9], excluded)

s11 = qsets(11)
check("Q11: engines citing Searchlab", {"ChatGPT", "Perplexity", "Gemini"},
      {e for e, v in s11.items() if any("searchlab" in x.lower() for x in v)})
check("Q11: engines citing AI Topia", 2,
      len({e for e, v in s11.items() if any("aitopia" in x.lower().replace(" ", "") for x in v)}))
check("Q1: engines citing hubspot.com", 3, sum("hubspot.com" in v for v in qsets(1).values()))

counts_table = {5: (0, 13, 6, 8), 6: (0, 10, 4, 11), 7: (0, 10, 0, 9), 8: (0, 9, 0, 7), 9: (0, 10, 1, 6)}
for q, pub in counts_table.items():
    check(f"Q{q} source counts ChatGPT/Perplexity/Gemini/AIO", pub,
          tuple(len(cites[(q, e)]) for e in ENGINES))
ppx = [len(cites[(q, "Perplexity")]) for q in QIDS]
check("Perplexity sources per answer, round two range", (8, 19), (min(ppx), max(ppx)))
check("highest single count on a comparison question (Perplexity, HubSpot vs Salesforce)", 13,
      max(len(cites[(q, e)]) for q in (5, 6, 7) for e in ENGINES))
check("comparison questions, other three engines' range", (4, 13),
      (min(len(cites[(q, e)]) for q in (5, 6, 7) for e in ENGINES[1:] if cites[(q, e)]),
       max(len(cites[(q, e)]) for q in (5, 6, 7) for e in ENGINES[1:])))
cgc = [len(cites[(q, "ChatGPT")]) for q in QIDS]
check("ChatGPT sources per answer, round two (spectrum table)", (0, 9, 2.5),
      (min(cgc), max(cgc), statistics.median(cgc)))
gmc = [len(cites[(q, "Gemini")]) for q in QIDS]
print(f"       Gemini sources per answer, round two: {min(gmc)} to {max(gmc)}")
check("Gemini on 'how to choose a CRM': nine brands, no source", (9, 0),
      next((int(r["brand_count"]), int(r["source_count"])) for r in aug
           if r["question_id"] == "8" and r["engine"] == "Gemini"))

# ---------------------------------------------------------------- round one
print("\n== Round one, 19 June 2026 ==")
jrows = {(int(r["question_id"]), r["engine"]): split(r["sources"]) for r in june}
check("June rows", 27, len(june))
cov = Counter(e for _, e in jrows)
check("coverage: Perplexity / ChatGPT / Gemini / AIO questions", (12, 6, 6, 3),
      (cov["Perplexity"], cov["ChatGPT"], cov["Gemini"], cov["Google AI Overview"]))
check("Q1 Perplexity list", "crm.org, tech.co, zendesk.com, techradar.com, hubspot.com, digitalocean.com, salesflare.com, blog.hubspot.com",
      ", ".join(jrows[(1, "Perplexity")]))
q1 = {e: set(jrows[(1, e)]) for e in ENGINES}
multi = {s for s in set().union(*q1.values()) if sum(s in v for v in q1.values()) > 1}
check("Q1: sites in more than one list", {"techradar.com", "reddit.com"}, multi)
check("Q1: Gemini overlaps with the others", 0,
      len(q1["Gemini"] & (q1["ChatGPT"] | q1["Perplexity"] | q1["Google AI Overview"])))
check("Q1: sources cited by all four", 0, len(set.intersection(*q1.values())))

SIX = sorted(q for q, e in jrows if e == "ChatGPT")
check("six head-to-head questions", [1, 2, 5, 7, 9, 11], SIX)
shared_pub = {1: {"techradar.com"}, 2: set(), 5: {"forbes.com", "reddit.com"}, 7: {"technologyadvice.com"},
              9: set(), 11: {"reddit.com"}}
for q in SIX:
    check(f"Q{q} Perplexity and ChatGPT shared", shared_pub[q],
          set(jrows[(q, "Perplexity")]) & set(jrows[(q, "ChatGPT")]))
check("domains cited by all three (ChatGPT, Perplexity, Gemini) on any of the six", 0,
      sum(len(set(jrows[(q, "Perplexity")]) & set(jrows[(q, "ChatGPT")]) & set(jrows[(q, "Gemini")])) for q in SIX))
p6 = [len(jrows[(q, "Perplexity")]) for q in SIX]
c6 = [len(jrows[(q, "ChatGPT")]) for q in SIX]
check("Perplexity 8 to 10 and ChatGPT 4 to 7 on the six", ((8, 10), (4, 7)), ((min(p6), max(p6)), (min(c6), max(c6))))
check("mean shared per question under one", True, statistics.mean(len(v) for v in shared_pub.values()) < 1)
check("Gemini sources on 'how to reduce customer churn'", 0, len(jrows[(9, "Gemini")]))
g6 = [len(jrows[(q, "Gemini")]) for q in SIX]
check("Gemini sources per answer, round one (spectrum table)", (0, 4), (min(g6), max(g6)))
pall = [len(jrows[(q, "Perplexity")]) for q in range(1, 13)]
check("Perplexity sources per answer, round one (spectrum table)", (8, 10), (min(pall), max(pall)))
print(f"       ChatGPT sources per answer, round one: {min(c6)} to {max(c6)}, median {statistics.median(c6)}")

# ---------------------------------------------------------------- churn
print("\n== Seven-week churn, Perplexity, June to August ==")
jp = {q: set(jrows[(q, "Perplexity")]) for q in range(1, 13)}
ap = {q: {s for s, _ in cites[(q, "Perplexity")]} for q in range(1, 13)}
jpool, apool = set().union(*jp.values()), set().union(*ap.values())
kept = jpool & apool
check("distinct Perplexity sources in June (pooled)", 80, len(jpool))
check("still cited in August (pooled)", 42, len(kept))
check("gone, %", 48, round(100 * (1 - len(kept) / len(jpool))))
check("pooled Jaccard", 0.29, round(len(kept) / len(jpool | apool), 2))
slots = sum(len(v) for v in jp.values())
lost = sum(len(jp[q] - ap[q]) for q in jp)
check("question by question, share of June source slots gone, %", 58, round(100 * lost / slots))
check("every question kept at least one source", True, all(jp[q] & ap[q] for q in jp))
per_q = {q: round(100 * len(jp[q] - ap[q]) / len(jp[q])) for q in jp}
check("most volatile question (Q4 best AI writing tools), %", (4, 90), max(per_q.items(), key=lambda x: x[1]))
check("most stable question (Q5 HubSpot vs Salesforce), %", (5, 25), min(per_q.items(), key=lambda x: x[1]))
print("       survivors include:", sorted(kept & {"zapier.com", "thedigitalprojectmanager.com",
                                                   "project-management.com", "techradar.com", "youtube.com"}))

print()
print(f"{sum(checks)} of {len(checks)} checks match.")
