"""Analyze SEJA harness usage profiles from briefs-index.md tables (both repos)."""
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})(?:\s+(\d{2}:\d{2}))?\s*(?:UTC)?\s*\|\s*([a-z-]+)\s*\|\s*(.*?)\s*\|\s*(STARTED|DONE)\s*\|")


def parse(path):
    entries = []
    for line in open(path, encoding="utf-8"):
        m = ROW.match(line)
        if m:
            date, time, skill, brief, status = m.groups()
            dt = datetime.strptime(f"{date} {time or '12:00'}", "%Y-%m-%d %H:%M")
            entries.append({"dt": dt, "skill": skill, "brief": brief, "status": status})
    entries.sort(key=lambda e: e["dt"])
    return entries


def analyze(name, entries, session_gap_hours=3):
    print(f"\n{'='*70}\n PROFILE: {name}  ({len(entries)} entries, "
          f"{entries[0]['dt'].date()} -> {entries[-1]['dt'].date()})\n{'='*70}")
    span_days = (entries[-1]["dt"] - entries[0]["dt"]).days + 1
    active_days = len({e["dt"].date() for e in entries})
    print(f"span: {span_days} days | active days: {active_days} | "
          f"entries/active-day: {len(entries)/active_days:.1f}")

    counts = Counter(e["skill"] for e in entries)
    print("\n-- skill counts --")
    for s, c in counts.most_common():
        print(f"  {s:<12} {c:>3}  ({100*c/len(entries):.0f}%)")

    started = sum(1 for e in entries if e["status"] == "STARTED")
    print(f"\norphaned STARTED (abandoned/crashed): {started} ({100*started/len(entries):.0f}%)")

    # sessions: group entries separated by < gap
    sessions = []
    cur = [entries[0]]
    for e in entries[1:]:
        if (e["dt"] - cur[-1]["dt"]) <= timedelta(hours=session_gap_hours):
            cur.append(e)
        else:
            sessions.append(cur)
            cur = [e]
    sessions.append(cur)
    print(f"\nsessions (gap>{session_gap_hours}h): {len(sessions)} | "
          f"avg invocations/session: {len(entries)/len(sessions):.1f}")

    # transition matrix (within sessions)
    trans = Counter()
    for s in sessions:
        for a, b in zip(s, s[1:]):
            trans[(a["skill"], b["skill"])] += 1
    print("\n-- top transitions (within-session) --")
    for (a, b), c in trans.most_common(14):
        print(f"  {a:>10} -> {b:<10} {c}")

    # row-normalized conditional probabilities P(next|current), with row n
    # (added in plan-000088 step 1 to verify the probabilities cited in
    # research-000087; raw counts above truncate at top-14 and hide row totals)
    row_totals = Counter()
    for (a, _b), c in trans.items():
        row_totals[a] += c
    print("\n-- P(next|current), row-normalized --")
    for a, n in row_totals.most_common():
        row = sorted(((b, c) for (x, b), c in trans.items() if x == a),
                     key=lambda t: -t[1])
        parts = ", ".join(f"{b} {100*c/n:.0f}% ({c})" for b, c in row)
        print(f"  {a:<12} (n={n}): {parts}")

    # session signatures (collapse consecutive repeats)
    sigs = Counter()
    for s in sessions:
        seq = []
        for e in s:
            if not seq or seq[-1] != e["skill"]:
                seq.append(e["skill"])
        sigs[" > ".join(seq)] += 1
    print("\n-- session signatures (collapsed, top 15) --")
    for sig, c in sigs.most_common(15):
        print(f"  [{c}x] {sig}")

    # entry-point skill per session
    starts = Counter(s[0]["skill"] for s in sessions)
    print("\n-- session entry-point skill --")
    for s_, c in starts.most_common():
        print(f"  {s_:<12} {c}")

    # briefs referencing prior artifacts (source:/plan/research/roadmap NNN refs)
    ref = sum(1 for e in entries if re.search(
        r"source:|research[- ]?0*\d{2,6}|plan[- ]?0*\d{2,6}|roadmap[- ]?0*\d{2,6}|reflection[- ]?0*\d{2,6}|advisory", e["brief"], re.I))
    print(f"\nbriefs explicitly chaining a prior artifact: {ref} ({100*ref/len(entries):.0f}%)")
    return counts, trans, sigs


e1 = parse(sys.argv[1])
e2 = parse(sys.argv[2])

# Phase cuts inside the parent repo:
#  P1 exploracao: <= 2026-06-10 12:00 (advise/atlas, tttc-poc, gavealab-poc)
#  P2 transicao:  2026-06-10 12:00 .. 2026-06-18 (fala-gavea prototypes in parent)
#  P4 relato:     >= 2026-06-19 (reporting/communication tail in parent)
c1 = datetime(2026, 6, 10, 12, 0)
c2 = datetime(2026, 6, 18, 0, 0)
p1 = [e for e in e1 if e["dt"] <= c1]
p2 = [e for e in e1 if c1 < e["dt"] < c2]
p4 = [e for e in e1 if e["dt"] >= c2]

analyze("FASE 1 - exploracao (parent ate 10/jun)", p1)
analyze("FASE 2 - transicao (parent 10-17/jun, prototipos fala-gavea)", p2)
analyze("FASE 3 - execucao focada (fala-gavea repo)", e2)
analyze("FASE 4 - relato/consolidacao (parent 19-30/jun)", p4)
