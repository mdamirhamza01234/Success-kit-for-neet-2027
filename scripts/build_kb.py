"""Build www/files/kb.json: every question of every mock test (text, correct answer, short solution, chapter tags).

The AI chatbot (Gemini and Gemma) reads this file together with the student's saved test records, so it can answer
"how many marks in test 3", "which questions did I get wrong", "show all animal kingdom questions in the 5 tests" etc.
Runs on every GitHub build (called from build_manifest.py). It never stops the build: on any problem it only warns.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_chapters import CHAPTERS  # noqa: E402

SUBJECTS = ["Physics", "Chemistry", "Botany", "Zoology"]
Q_MAX, S_MAX = 650, 420


def norm(s):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s


def words(s):
    """lower-case text with every non letter/digit turned into one space (so keywords match whole words)."""
    return " " + re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip() + " "


def squash(s):
    return re.sub(r"[^a-z0-9]+", "", str(s).lower())


def compile_keywords():
    out = []
    for idx, (cid, name, subj, alias, kws) in enumerate(CHAPTERS):
        pats = []
        seen = set()
        for kw in [k.strip().lower() for k in kws.split(",") if k.strip()]:
            w = re.sub(r"[^a-z0-9]+", " ", kw).strip()
            if not w or w in seen:
                continue
            seen.add(w)
            body = r"\s+".join(re.escape(p) for p in w.split())
            # 6+ letter keywords match as a word prefix (glomerul -> glomerulus), shorter ones as a whole word
            pat = r"(?<![a-z0-9])" + body + ("" if len(w.replace(" ", "")) >= 6 else r"(?![a-z0-9])")
            long_sq = squash(w) if len(squash(w)) >= 9 else None   # also matched in text with broken spacing
            pats.append((re.compile(pat), long_sq, len(squash(w)) >= 6))
        out.append(pats)
    return out


def tag(question, solution, compiled):
    """Chapter(s) of a question. A keyword found in the question counts 2, in the solution 1.
    A chapter is accepted with 3+ points, or with 2 points when the keyword is specific (6+ letters)."""
    qw, sw = words(question), words(solution)
    qs, ss = squash(question), squash(solution)
    scores = []
    for ci, pats in enumerate(compiled):
        hit, strong = 0, False
        for rx, lsq, long_kw in pats:
            q_hit = rx.search(qw) is not None or (lsq and lsq in qs)
            s_hit = rx.search(sw) is not None or (lsq and lsq in ss)
            if q_hit:
                hit += 2
                strong = strong or long_kw
            elif s_hit:
                hit += 1
        if hit >= 3 or (hit == 2 and strong):
            scores.append((hit, ci))
    if not scores:
        return []
    scores.sort(key=lambda x: (-x[0], x[1]))
    top = scores[0][0]
    keep = [ci for sc, ci in scores if sc == top][:2]
    if len(keep) < 2 and len(scores) > 1 and scores[1][0] >= max(3, top - 1) and scores[1][1] not in keep:
        keep.append(scores[1][1])
    return keep


def read_mock(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r'<script[^>]*id="app-data-holder"[^>]*>(.*?)</script>', t, re.S)
    if not m:
        return None
    return json.loads(m.group(1))


def build(src_dir, out_dir, classify):
    compiled = compile_keywords()
    tests, stats = {}, {}
    for name in sorted(os.listdir(src_dir)):
        res = classify(name)
        if not res or res[1] != "mock":
            continue
        n = res[0]
        try:
            d = read_mock(os.path.join(src_dir, name))
        except Exception as e:  # noqa: BLE001
            print("kb: could not read %s (%s)" % (name, e))
            continue
        if not d or "qtx" not in d:
            print("kb: %s has no question data - skipped" % name)
            continue
        rows = []
        for i, q in enumerate(d["qtx"]):
            sol = norm(d["stx"][i]) if i < len(d.get("stx", [])) else ""
            ans = d["answers"][i] if i < len(d.get("answers", [])) else 0
            subj = d["subjects"][i] if i < len(d.get("subjects", [])) else ""
            sidx = SUBJECTS.index(subj) if subj in SUBJECTS else -1
            chs = tag(q, sol, compiled)
            for c in chs:
                stats[c] = stats.get(c, 0) + 1
            has_fig = 1 if (i < len(d.get("qfg", [])) and d["qfg"][i]) else 0
            rows.append([i + 1, sidx, ans, chs, norm(q)[:Q_MAX], sol[:S_MAX], has_fig])
        tests[str(n)] = rows
    chapters = []
    for cid, nm, subj, alias, kws in CHAPTERS:
        al = [a.strip() for a in alias.split(",") if a.strip()]
        if nm.lower() not in al:
            al.insert(0, nm.lower())
        chapters.append({"id": cid, "name": nm, "subj": subj, "alias": al})
    kb = {"subjects": SUBJECTS, "chapters": chapters, "tests": tests}
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "kb.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, separators=(",", ":"))
    total = sum(len(v) for v in tests.values())
    tagged = sum(1 for v in tests.values() for r in v if r[3])
    print("kb: %d questions from %d tests, %d tagged with a chapter -> kb.json (%d KB)" % (total, len(tests), tagged, os.path.getsize(path) // 1024))
    return kb, stats


if __name__ == "__main__":
    # quick local run:  python scripts/build_kb.py
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(root, "scripts"))
    import build_manifest  # noqa: E402
    build(os.path.join(root, "files"), os.path.join(root, "www", "files"), build_manifest.classify)
