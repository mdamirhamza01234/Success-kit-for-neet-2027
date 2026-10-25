"""Collect the files in files/ and prepare them for the app (runs on every GitHub build).

File name rules (number first, then S for a solution):
  01_NEET Success Kit.html   -> mock test of test 1
  01_NEET Success Kit.pdf    -> question paper of test 1
  01S_NEET Success Kit.pdf   -> solutions of test 1   (S right after the number)
Fallback: a .pdf with key / ans / solution in the name is also treated as solutions.

Files are copied to www/files/ as p01.pdf (paper), k01.pdf (solutions), m01.html (mock)
and www/files/manifest.json is written for the app.
"""
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "files")
OUT = os.path.join(ROOT, "www", "files")
PREFIX = {"paper": "p", "key": "k", "mock": "m"}


def classify(name):
    base, ext = os.path.splitext(name)
    ext = ext.lower()
    if ext not in (".html", ".htm", ".pdf"):
        return None
    m = re.match(r"^\s*0*(\d{1,2})\s*([sS])?(?=[\s_\-.]|$)", base)
    if m:
        n, solution = int(m.group(1)), bool(m.group(2))
    else:
        nums = [int(x) for x in re.findall(r"\d+", base) if len(x) <= 2]
        if not nums:
            return None
        n, solution = nums[0], False
    if ext in (".html", ".htm"):
        return n, "mock", ".html"
    low = base.lower()
    if solution or re.search(r"key|ans|solution", low):
        return n, "key", ".pdf"
    return n, "paper", ".pdf"


# Every mock test has the same template. Right at the start of its finishTest() the patch hands the
# result to window.__mstCapture (see record_hook.js), so the score lands in "Test Records".
PATCH = (
    "\ntry{ if(!practice) window.__mstCapture(N, subjectRanges, function(i){ var g = grade(i), u = userAns[i];"
    " return {ch: (typeof u === 'number' ? u : (Array.isArray(u) ? u.join(',') : (u ? String(u) : 0))),"
    " key: DATA.answers[i], c: g.c, m: g.m, bonus: BON.has(i)}; }, timeLeft, 180 * 60); }catch(e){}\n"
)
ANCHOR = re.compile(r"function finishTest\s*\(\s*\)\s*\{")


def copy_mock(src, dst):
    with open(os.path.join(ROOT, "scripts", "record_hook.js"), encoding="utf-8") as f:
        hook = f.read()
    with open(src, "r", encoding="utf-8", errors="surrogateescape", newline="") as f:
        html = f.read()
    ok = False
    if 'id="mst-hook"' not in html:
        m = ANCHOR.search(html)
        if m and "const DATA" in html and "subjectRanges" in html:
            html = html[: m.end()] + PATCH + html[m.end():]
            ok = True
        tag = '<script id="mst-hook">\n' + hook + "\n</script>\n"
        i = html.lower().rfind("</body>")
        html = html[:i] + tag + html[i:] if i != -1 else html + "\n" + tag
    else:
        ok = True
    with open(dst, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
        f.write(html)
    return ok


def main():
    if not os.path.isdir(SRC):
        print("ERROR: 'files/' folder not found.")
        sys.exit(1)

    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)

    found, patched, skipped, conflicts = {}, {}, [], []

    for name in sorted(os.listdir(SRC)):
        path = os.path.join(SRC, name)
        if not os.path.isfile(path):
            continue
        res = classify(name)
        if not res:
            skipped.append(name)
            continue
        n, kind, ext = res
        if (n, kind) in found:
            conflicts.append("Test %d %s: '%s' and '%s'" % (n, kind, found[(n, kind)], name))
            continue
        found[(n, kind)] = name
        dest = os.path.join(OUT, "%s%02d%s" % (PREFIX[kind], n, ext))
        if kind == "mock":
            patched[(n, kind)] = copy_mock(path, dest)
        else:
            shutil.copyfile(path, dest)

    manifest = {}
    for (n, kind), name in sorted(found.items()):
        ext = ".html" if kind == "mock" else ".pdf"
        manifest.setdefault(str(n), {})[kind] = "files/%s%02d%s" % (PREFIX[kind], n, ext)
        print("test %02d  %-6s <- %s" % (n, kind, name))

    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    for (n, kind), ok in sorted(patched.items()):
        if not ok:
            print("WARNING: test %02d mock has a new layout, its result will NOT be saved in Test Records" % n)

    for s in sorted(manifest, key=int):
        missing = [{"paper": "question paper", "key": "solutions", "mock": "mock"}[k] for k in ("paper", "key", "mock") if k not in manifest[s]]
        if missing:
            print("NOTE: test %s has no %s yet" % (s, ", ".join(missing)))
    for name in skipped:
        print("skipped (not recognised): " + name)

    if conflicts:
        print("\nERROR: two files match the same slot, rename one of them:")
        for c in conflicts:
            print("  - " + c)
        sys.exit(1)
    if not manifest:
        print("ERROR: no usable files found in files/")
        sys.exit(1)
    print("\n%d tests ready." % len(manifest))


if __name__ == "__main__":
    main()
