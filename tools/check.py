#!/usr/bin/env python3
"""Check the quiz data in index.html.

Rules:
  * IDs are unique (topics; words, tasks and grammar sections inside a topic).
  * Every word's theme exists, every task's grammar section exists.
  * The vocabulary rule: a task or an example sentence in topic N may use only
    words from topics 1..N (plus basic grammar words below).
    A word that first appears in a LATER topic is an error.
    A word that is in no topic at all is a warning (maybe fine, maybe add it).

Usage:  python3 tools/check.py [index.html | data.json]
Exit code 1 if there are errors.
"""
import json, re, sys
from pathlib import Path

# Words every exercise may use without them being taught in a topic.
BASIC = set("""
i you he she it we they me him her us them my your his its our their
a an the and or but not no yes
is am are be have has got
to of in on at for with from
""".split())

WORD = re.compile(r"[a-z]+(?:'[a-z]+)?")


def load(path):
    text = Path(path).read_text(encoding="utf-8")
    if path.endswith(".json"):
        return json.loads(text)
    m = re.search(r'<script id="words" type="application/json">(.*?)</script>', text, re.S)
    if not m:
        sys.exit("No <script id=\"words\"> block found")
    return json.loads(m.group(1))


def tokens(text):
    text = text.lower().replace("’", "'")
    out = []
    for w in WORD.findall(text):
        if w.endswith("'s"):
            w = w[:-2]
        elif "'" in w:            # I'm, isn't, we're, I've
            base, tail = w.split("'", 1)
            out.append(base)
            w = {"m": "am", "re": "are", "ve": "have", "t": "not", "ll": "will", "d": "would"}.get(tail, tail)
            if base.endswith("n") and tail == "t":
                out[-1] = base[:-1]  # isn't -> is, aren't -> are
        out.append(w)
    return out


def forms(w):
    """Possible dictionary forms of a word seen in a sentence (very small stemmer)."""
    f = {w}
    if w.endswith("ies") and len(w) > 4: f.add(w[:-3] + "y")
    if w.endswith("es") and len(w) > 3: f.add(w[:-2])
    if w.endswith("s") and len(w) > 2: f.add(w[:-1])
    return f


def vocab_words(item):
    """All single words an item teaches: 'sunglasses / glasses', '(to be) late', 'I know'."""
    return set(tokens(re.sub(r"[()]", " ", item["en"])))


def main(path):
    data = load(path)
    topics = sorted(data["topics"], key=lambda t: t["order"])
    errors, warnings = [], []

    seen_topic = set()
    first_topic = {}  # word -> order of the topic that introduces it
    for t in topics:
        if t["id"] in seen_topic: errors.append(f"duplicate topic id {t['id']}")
        seen_topic.add(t["id"])
        for kind in ("words", "tasks", "grammar"):
            ids = [x["id"] for x in t.get(kind, [])]
            dup = {i for i in ids if ids.count(i) > 1}
            if dup: errors.append(f"{t['id']}: duplicate {kind} ids {sorted(dup)}")
        themes, gids = t.get("themes", {}), {g["id"] for g in t.get("grammar", [])}
        for w in t.get("words", []):
            if w.get("topic") and w["topic"] not in themes:
                errors.append(f"{t['id']}/{w['id']}: unknown theme '{w['topic']}'")
            for v in vocab_words(w):
                first_topic.setdefault(v, t["order"])
        for k in t.get("tasks", []):
            if k.get("grammar") not in gids:
                errors.append(f"{t['id']}/{k['id']}: unknown grammar section '{k.get('grammar')}'")
            if not k.get("en") or not isinstance(k["en"], list):
                errors.append(f"{t['id']}/{k['id']}: 'en' must be a non-empty list")

    def check_sentence(t, where, text):
        for w in tokens(text):
            if w in BASIC: continue
            known = [first_topic[f] for f in forms(w) if f in first_topic]
            if not known:
                warnings.append(f"{t['id']}/{where}: '{w}' is not in any topic — \"{text}\"")
            elif min(known) > t["order"]:
                errors.append(f"{t['id']}/{where}: '{w}' is from Topic {min(known)} — \"{text}\"")

    for t in topics:
        for w in t.get("words", []):
            if w.get("ex"): check_sentence(t, w["id"] + " example", w["ex"])
        for k in t.get("tasks", []):
            if k.get("en"):              # the main answer; the other variants only widen what is accepted
                check_sentence(t, k["id"], k["en"][0])

    for w in warnings: print("warning:", w)
    for e in errors: print("ERROR:  ", e)
    n_words = sum(len(t.get("words", [])) for t in topics)
    n_tasks = sum(len(t.get("tasks", [])) for t in topics)
    print(f"{len(topics)} topics, {n_words} words, {n_tasks} tasks: {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    here = Path(__file__).resolve().parent.parent
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else str(here / "index.html")))
