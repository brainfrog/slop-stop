"""Mechanical checks for the slop-stop skill. Run: python -I scripts/check.py

Exit code 0 means every check passed. Not loaded when the skill runs.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")  # Cyrillic in messages on any console
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = ["references/structures.md", "references/phrases-ru.md", "references/phrases-en.md"]
ALL = ["SKILL.md", "MAINTAINING.md", "references/genres.md", "references/examples.md"] + REFS
MARKERS = ("*(first sight)*", "*(cluster)*", "*(weak)*")
# Headings that group patterns or hold genre rules, not patterns themselves.
NOT_PATTERNS = re.compile(r"^(#+ [A-F]\. |#+ English only$|#+ Commit messages$)")
# Agent Skills limits for frontmatter fields.
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX, DESCRIPTION_MAX = 64, 1024
# A plain YAML scalar must not start with one of these.
YAML_INDICATORS = set("-?:,[]{}#&*!|>'\"%@`")

problems = []
warnings = []  # a check that could not run on this machine; printed, does not fail


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def anchors(rel):
    """Headings (without markers) and bold labels of a file: valid targets of a named reference."""
    text = read(rel)
    names = {h.strip() for h in re.findall(r"^#+ (.*?)(?: \*\(.*\)\*)?$", text, re.M)}
    names |= {b.strip().rstrip(".:") for b in re.findall(r"\*\*([^*]+?)\*\*", text)}
    names |= {re.sub(r"^[A-Z0-9]+\. ", "", n) for n in list(names)}  # "A. Staging…" -> "Staging…"
    return names


def outline(rel):
    """(position, level, names) of every heading and bold label, in order. A bold label ranks below every
    heading, so its section ends at the next heading or bold label."""
    text, items = read(rel), []
    for m in re.finditer(r"^(#+) (.*?)(?: \*\(.*\)\*)?$", text, re.M):
        name = m.group(2).strip()
        items.append((m.start(), len(m.group(1)), {name, re.sub(r"^[A-Z0-9]+\. ", "", name)}))
    for m in re.finditer(r"\*\*([^*]+?)\*\*", text):
        items.append((m.start(), 99, {m.group(1).strip().rstrip(".:")}))
    return sorted(items, key=lambda x: x[0])


skill = read("SKILL.md")

# 1. Frontmatter: name matches the directory, description is a valid plain YAML scalar within limits.
front = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
if not front:
    problems.append("SKILL.md: no frontmatter")
else:
    fields = dict(re.findall(r"^(\w+): (.*)$", front.group(1), re.M))
    name, desc = fields.get("name", ""), fields.get("description", "")
    if name != os.path.basename(ROOT):
        problems.append(f"SKILL.md: name '{name}' does not match directory '{os.path.basename(ROOT)}'")
    if not NAME_RE.match(name) or len(name) > NAME_MAX:
        problems.append(f"SKILL.md: name '{name}' must be lowercase letters, digits, hyphens, at most {NAME_MAX}")
    if not desc:
        problems.append("SKILL.md: no description")
    if re.search(r": | #", desc):
        problems.append("SKILL.md: description contains ': ' or ' #' (breaks YAML)")
    if desc[:1] in YAML_INDICATORS or desc != desc.strip():
        problems.append("SKILL.md: description starts with a YAML indicator or has edge spaces (breaks YAML)")
    if len(desc) > DESCRIPTION_MAX:
        problems.append(f"SKILL.md: description is {len(desc)} characters, limit {DESCRIPTION_MAX}")

# 2. Every rule reference ('rule 7', 'core rule 3', 'rules 1–5 and 8') points at an existing core rule.
core = re.search(r"## Core rules\n(.*?)\n## ", skill, re.S)
if not core:
    problems.append("SKILL.md: no '## Core rules' section")
n_rules = len(re.findall(r"^\d+\. \*\*", core.group(1), re.M)) if core else 0
for rel in ALL:
    for m in re.finditer(r"\b(?:core )?rules? (\d+)(?:[–-](\d+))?(?: and (\d+))?", read(rel), re.I):
        for g in m.groups():
            if g and not 1 <= int(g) <= n_rules:
                problems.append(f"{rel}: '{m.group(0)}' but there are {n_rules} core rules")

# 3. Marker definitions live only in SKILL.md.
for rel in REFS + ["references/genres.md"]:
    for phrase in ("three in a paragraph", "three signs", "on first sight", "single occurrence"):
        if phrase in read(rel).lower():
            problems.append(f"{rel}: restates a marker definition ('{phrase}')")

# 4. Every pattern carries exactly one marker: a tag in its heading or 'Own threshold:' in its body.
for rel in REFS:
    level = "###" if rel.endswith("structures.md") else "##"
    parts = re.split(rf"^({level} .*)$", read(rel), flags=re.M)
    for heading, body in zip(parts[1::2], parts[2::2]):
        if NOT_PATTERNS.match(heading):
            continue
        body = re.split(r"^#{2,3} ", body, flags=re.M)[0]
        tags = [t for t in MARKERS if t in heading]
        own = "Own threshold:" in body
        if len(tags) + own != 1:
            problems.append(f"{rel}: '{heading}' has {len(tags)} tag(s) and own threshold={own}; needs exactly one")

# 5. Every Before/After pair in examples.md has a Changes line.
for block in re.split(r"^#{2,3} ", read("references/examples.md"), flags=re.M)[1:]:
    if "**Before:**" in block and "**Changes:**" not in block:
        problems.append(f"examples.md: '{block.splitlines()[0]}' has no Changes line")

# 6. Named cross-references point at an existing heading or bold label. Case-insensitive: a sentence
# may start with "See".
every_anchor = set().union(*(anchors(r) for r in ALL))
# Bold labels of each core rule, for references like "(core rule 2, Roles)".
core_labels = {}
if core:
    for num, item in re.findall(r"^(\d+)\. (.*?)(?=^\d+\. |\Z)", core.group(1), re.M | re.S):
        core_labels[int(num)] = {b.strip().rstrip(".:") for b in re.findall(r"\*\*([^*]+?)\*\*", item)}
def target_of(file):
    """Path of a file named in the text: the two top-level files sit in the root, the rest in references/."""
    return file if file in ("SKILL.md", "MAINTAINING.md") or file.startswith("references/") else "references/" + file


MD_NAME = r"[A-Za-z][A-Za-z-]*\.md"
for rel in ALL:
    text = re.sub(r"`[^`\n]*`", "", read(rel))  # inline code shows syntax, not real references
    # Every file named outside code exists, whatever the sentence around it says.
    for name in sorted(set(re.findall(rf"(?<![\w/.-])((?:references/)?{MD_NAME})\b", text))):
        if not os.path.exists(os.path.join(ROOT, target_of(name))):
            problems.append(f"{rel}: reference to missing file '{name}'")
    # '"X" in file.md' is a section reference whatever verb comes before it ("see", "under", "follows").
    for m in re.finditer(rf'"([^"\n]+)" in ({MD_NAME})', text):
        section, file = m.group(1), m.group(2)
        if os.path.exists(os.path.join(ROOT, target_of(file))) and section not in anchors(target_of(file)):
            problems.append(f"{rel}: '{m.group(0)}': no section '{section}' in {file}")
    # 'see "X"' and 'under "X"' with no file name point at a section anywhere in the skill.
    for m in re.finditer(rf'\b(?:under|see) "([^"\n]+)"(?! in {MD_NAME})', text, re.I):
        if m.group(1) not in every_anchor:
            problems.append(f"{rel}: reference to missing section '{m.group(1)}'")
    for m in re.finditer(rf"\(({MD_NAME}), ([^()]+?)\)", text):
        target = target_of(m.group(1))
        if not os.path.exists(os.path.join(ROOT, target)):
            continue  # reported above as a missing file
        # Each part must sit inside the previous one: "Warnings" under "Output modes", not anywhere.
        # (A "(core rule N, Label)" reference is checked below.)
        lo, hi = 0, None
        for part in m.group(2).split(", "):
            found = next((x for x in outline(target) if x[0] >= lo and (hi is None or x[0] < hi) and part in x[2]), None)
            if not found:
                where = "in " + m.group(1) if lo == 0 else "inside the previous part"
                problems.append(f"{rel}: '{m.group(0)}': no section '{part}' {where}")
                break
            lo = found[0] + 1
            hi = next((x[0] for x in outline(target) if x[0] >= lo and x[1] <= found[1]), None)
    for m in re.finditer(r"\bProcess, step (\d+)", text):
        steps = re.search(r"^## Process\n(.*?)(?=^## )", skill, re.S | re.M)
        n_steps = len(re.findall(r"^\d+\. \*\*", steps.group(1), re.M)) if steps else 0
        if not 1 <= int(m.group(1)) <= n_steps:
            problems.append(f"{rel}: '{m.group(0)}' but Process has {n_steps} steps")
    for m in re.finditer(r"\(core rule (\d+), ([^()]+?)\)", text, re.I):
        labels = core_labels.get(int(m.group(1)))
        if labels is not None and m.group(2) not in labels:  # a missing rule number is check 2's finding
            problems.append(f"{rel}: '{m.group(0)}': no label '{m.group(2)}' in core rule {m.group(1)}")

# 7. Every instruction to warn ("warn", "warns", "warned", "with a warning") in the references points at
# the Warnings list, so the list cannot drift. The noun in a description ("lost a warning") is not one.
WARN_RE = re.compile(r"\bwarn(s|ed)?\b|\b(with|give|add|issue) an? warning\b", re.I)
for rel in REFS + ["references/genres.md"]:
    for n, line in enumerate(read(rel).splitlines(), 1):
        if WARN_RE.search(line) and "Warnings" not in line:
            problems.append(f"{rel}:{n}: says 'warn' without pointing at SKILL.md, Output modes, Warnings")

# 8. One phrase, one pattern: a quoted multi-word phrase listed under two patterns means two homes
# for one rule. One-word quotes are skipped: they are mostly replacements, not listed patterns.
def pattern_sections(rel):
    level = "###" if rel.endswith("structures.md") else "##"
    parts = re.split(rf"^({level} .*)$", read(rel), flags=re.M)
    for heading, body in zip(parts[1::2], parts[2::2]):
        if not NOT_PATTERNS.match(heading):
            yield heading, re.split(r"^#{2,3} ", body, flags=re.M)[0]


homes = {}
for rel in REFS:
    for heading, body in pattern_sections(rel):
        body = "\n".join(l for l in body.splitlines() if not l.lstrip("- ").startswith(("Bad:", "Good:")))
        for q in re.findall(r"«([^»\n]{4,})»|\"([^\"\n]{4,})\"", body):
            phrase = re.sub(r"[\s.,:;!?…]+$", "", (q[0] or q[1]).lower())
            if " " not in phrase or phrase in {a.lower() for a in every_anchor}:
                continue  # one-word replacements ("хранит", "use") recur legitimately; section names are references
            homes.setdefault(phrase, set()).add(f"{rel} / {heading}")
for phrase, where in sorted(homes.items()):
    if len(where) > 1:
        problems.append(f"phrase '{phrase}' is listed under {len(where)} patterns: {'; '.join(sorted(where))}")

# 9. One construction carries one marker, whether it is a phrase and its translation or two wordings of
# one construction in one language («произвести перезапуск», «осуществляет проверку»); otherwise it is
# fixed on first sight in one place and only in a cluster in the other. The script cannot translate or
# parse, so the pairs are listed here: add one whenever the skill lists the same construction twice.
# A phrase must occur only in the sections of its pattern, so pick a wording that does not recur
# elsewhere ("really" also sits in "What really matters is", so it is not a pair).
PAIRS = [
    ("Конечно! Вот", "Certainly! Here is"),
    ("произвести перезапуск", "осуществляет проверку"),
    ("Интересно, что", "Interestingly"),
    ("Примечательно, что", "Notably"),
    ("Важно отметить", "It's important to note"),
    ("Стоит отметить, что", "It's worth noting"),
    ("Давайте посмотрим", "Let's take a look"),
    ("Правда в том, что", "The truth is"),
    ("В современном мире", "In today's"),
    ("Как известно", "As is well known"),
    ("если честно", "To be honest"),
    ("Стоит уточнить", "To be precise"),
    ("По своей сути", "At its core"),
    ("настоящий вопрос в том", "The real question is"),
    ("Подводя итог", "In summary"),
    ("В заключение", "In conclusion"),
    ("Время покажет", "Time will tell"),
    ("Отличный вопрос", "Great question"),
    ("Надеюсь, это поможет", "I hope this helps"),
    ("Дайте знать, если", "Let me know if"),
    ("играет ключевую роль", "plays a key role"),
    ("закладывает основу для", "paves the way for"),
    ("Последствия значительны", "The implications are significant"),
    ("Эксперты считают", "experts say"),
    ("Связан с", "associated with"),
    ("Кроме того", "Additionally"),
    ("по-настоящему", "genuinely"),
    ("буквально", "literally"),
    ("на текущий момент", "at this point in time"),
    ("обеспечивая", "ensuring"),
]


def markers_of(phrase):
    found = set()
    for rel in REFS:
        for heading, body in pattern_sections(rel):
            if re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", body, re.I):
                found.add(next((t for t in MARKERS if t in heading), "Own threshold"))
    return found


def sections_of(phrase):
    """(heading name without marker, body, marker) of every pattern section that lists the phrase. A phrase
    is looked up only where its language is listed: the other phrase file may quote it to explain itself."""
    other = "references/phrases-en.md" if re.search(r"[а-яё]", phrase, re.I) else "references/phrases-ru.md"
    found = []
    for rel in [r for r in REFS if r != other]:
        for heading, body in pattern_sections(rel):
            if re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", body, re.I):
                name = re.sub(r"^#+ | \*\(.*\)\*$", "", heading)
                found.append((name, body, next((t for t in MARKERS if t in heading), "Own threshold")))
    return found


# A translation pair may carry different markers only when one of the two patterns names the other in
# quotes and so explains the difference («Является» against "Copula avoidance"). Such pairs are listed
# here; a pair that turns out to share a marker belongs in PAIRS.
ASYMMETRIC_PAIRS = [
    ("имеет возможность", "has the ability to"),
    ("в целях обеспечения", "in order to"),
    ("в случае возникновения", "in the event that"),
]
for a, b in ASYMMETRIC_PAIRS:
    s_a, s_b = sections_of(a), sections_of(b)
    if len(s_a) != 1 or len(s_b) != 1:
        problems.append(f"asymmetric pair '{a}' / '{b}': each phrase must sit in exactly one pattern, update check.py")
        continue
    (name_a, body_a, mark_a), (name_b, body_b, mark_b) = s_a[0], s_b[0]
    if mark_a == mark_b:
        problems.append(f"asymmetric pair '{a}' / '{b}': both are {mark_a}; move the pair to PAIRS")
    elif f'"{name_b}"' not in body_a and f'"{name_a}"' not in body_b:
        problems.append(f"asymmetric pair '{a}' / '{b}': markers differ ({mark_a} vs {mark_b}) and neither "
                        f"'{name_a}' nor '{name_b}' names the other pattern to explain why")

for a, b in PAIRS:
    m_a, m_b = markers_of(a), markers_of(b)
    if not m_a or not m_b:
        problems.append(f"pair '{a}' / '{b}': a phrase is in no pattern, update PAIRS in check.py")
    elif m_a != m_b or len(m_a) > 1:
        problems.append(f"pair '{a}' / '{b}': markers {sorted(m_a)} vs {sorted(m_b)}, need one and the same")

# 10. A listed item that reappears at the start of an example in its own pattern's "Exception:" is either
# a word that is usually empty and only sometimes protected (it stays, the exception names the rare
# case) or a word whose usual meaning the exception protects (it leaves the list). The script cannot
# tell which, so every such overlap must be reviewed by hand (MAINTAINING.md, "Before adding a rule")
# and then added here. "Importantly," once sat in the run-up list and in the run-up exception at once;
# «полностью» once sat here although its usual technical meaning ("entirely") is the protected one.
# An entry that no longer overlaps is stale and fails too, so the set cannot hide a future overlap.
REVIEWED_OVERLAPS = {
    "overall", "ultimately", "крайне", "принципиально", "максимально", "по сути",
    "just", "fundamentally", "inherently", "deeply", "genuinely",
}
seen_overlaps = set()


def quoted(text):
    return [q[0] or q[1] for q in re.findall(r"«([^»\n]+)»|\"([^\"\n]+)\"", text)]


for rel in REFS:
    for heading, body in pattern_sections(rel):
        if "Exception:" not in body:
            continue
        # The exception runs to the end of its paragraph; the list may stand before or after it.
        before, rest = body.split("Exception:", 1)
        exception, _, after = rest.partition("\n\n")
        listed = before + "\n\n" + after
        items = [re.sub(r"[\s.,:;!?…]+$", "", q).lower() for q in quoted(listed)]
        cut = re.search(r"^Cut: ([^.]*)", listed, re.M)  # bare word lists in the phrase files
        if cut:
            items += [w.split(" (")[0].strip().lower() for w in cut.group(1).split(",")]
        for example in quoted(exception):
            for item in items:
                if not item or not re.match(rf"{re.escape(item)}(?!\w)", example.lower()):
                    continue
                seen_overlaps.add(item)
                if item not in REVIEWED_OVERLAPS:
                    problems.append(f"{rel} / {heading}: '{item}' is listed and also kept in its Exception ('{example}'); review it, then add to REVIEWED_OVERLAPS")

for item in sorted(REVIEWED_OVERLAPS - seen_overlaps):
    problems.append(f"REVIEWED_OVERLAPS: '{item}' no longer overlaps any Exception; remove it from check.py")

# 11. Claim words and hedges survive every example. A word from those two lists of core rule 2 that is in
# "Before" must be in "After" or be quoted in the example's Changes or Change list, so a lost
# «как правило» cannot slip through. The lists are read from SKILL.md, their one home: the quoted words
# in the first sentence of each bullet.
def rule2_words():
    words = []
    for label in ("Claim words", "Hedges and scope"):
        m = re.search(rf"\*\*{label}\.\*\* (.*?[^.]\.) ", skill)
        if not m:
            problems.append(f"SKILL.md: no '{label}' bullet in core rule 2; update check.py")
            continue
        found = [w.lower() for w in re.findall(r'"([^"]+)"', m.group(1))]
        # The Russian and English halves are translations in the same order, so a word added to one
        # language without its pair (English once lacked "approximately", "still", "sole") shows here.
        ru = [w for w in found if re.search(r"[а-яё]", w)]
        if len(ru) != len(found) - len(ru):
            problems.append(f"SKILL.md: '{label}' lists {len(ru)} Russian and {len(found) - len(ru)} English words; "
                            "each word needs its translation in the same position")
        words += found
    return words


def examples():
    """(key, title, labelled parts) for every example in examples.md that has a Before."""
    for block in re.split(r"^#{2,3} ", read("references/examples.md"), flags=re.M)[1:]:
        title = block.splitlines()[0]
        parts = {k: v.strip() for k, v in re.findall(r"^\*\*([^*]+?):\*\*(.*?)(?=^\*\*|\Z)", block, re.M | re.S)}
        if "Before" not in parts:
            continue
        unquote = lambda s: "\n".join(l[2:] for l in s.splitlines() if l.startswith("> "))
        after = next((v for k, v in parts.items() if k.startswith("After")), "")
        parts["before_text"] = unquote(parts["Before"])
        parts["after_text"] = parts["before_text"] if after.startswith("unchanged") else unquote(after)
        parts["notes"] = parts.get("Changes", "") + "\n" + parts.get("Change list", "")
        yield title.split(".")[0], title, parts


def has_word(word, text):
    return re.search(rf"(?<!\w){re.escape(word)}(?!\w)", text, re.I) is not None


RULE2_WORDS = rule2_words()
for key, title, parts in examples():
    for word in RULE2_WORDS:
        if has_word(word, parts["before_text"]) and not has_word(word, parts["after_text"]) \
                and not any(has_word(word, q) for q in quoted(parts["notes"])):
            problems.append(f"examples.md: '{title}' lost '{word}' (core rule 2) without quoting it in Changes or Change list")

# 12. Every example meets the marker of the patterns it is edited for (MAINTAINING.md, written check 7).
# Each example lists its signs here: (phrase in Before, pattern heading). A *(first sight)* or
# "Own threshold:" sign is enough; *(cluster)* and *(weak)* signs need about three. An example edited for
# its genre, for a core rule, or left unchanged says so instead. A new example without an entry fails.
EXAMPLE_SIGNS = {
    "1": [("является ключевым", "Significance"), ("надёжную", "AI vocabulary (calques)"),
          ("обеспечивает", "AI vocabulary (calques)"), ("позволяя", "Participle tails")],
    "2": [("была проведена", "Verbal nouns and officialese")],
    "3": [("Важно отметить", "Run-ups")],
    "4": [("genre", "README")],
    "5": [("**Производительность:**", "Bold as decoration")],
    "6": [("genre", "Review or chat reply")],
    "7": [("не просто таймаут, а", '"Not X but Y"'), ("Именно в этом его главная ценность", "Closing morals and dramatic fragments")],
    "8": [("rule", "5")],
    "9": [("unchanged", "")],
    "E1": [("serves as", "Copula avoidance"), ("robust", "Overused AI words"),
           ("seamlessly", "Overused AI words"), ("ensuring reliable operation", "-ing riders")],
    "E2": [("Here's the thing:", "Run-ups"), ("Let that sink in.", "Closing morals and dramatic fragments")],
    "E3": [("genre", "Commit")],
    "E4": [("tells us", "False agency"), ("plays a key role", "Significance"), ("say most", "False agency")],
}
pattern_markers = {}
for rel in REFS:
    for heading, _ in pattern_sections(rel):
        name = re.sub(r"^#+ | \*\(.*\)\*$", "", heading)
        pattern_markers[name] = next((t for t in MARKERS if t in heading), "Own threshold")
genre_rows = [row.split("|")[1].strip() for row in read("references/genres.md").splitlines() if row.startswith("| ")]
seen_examples = set()
for key, title, parts in examples():
    seen_examples.add(key)
    signs = EXAMPLE_SIGNS.get(key)
    if not signs:
        problems.append(f"examples.md: '{title}' has no entry in EXAMPLE_SIGNS in check.py")
        continue
    enough, weak = False, 0
    for phrase, target in signs:
        if phrase == "genre":
            ok = any(target in row for row in genre_rows)
            enough |= ok
            if not ok:
                problems.append(f"EXAMPLE_SIGNS['{key}']: no genre '{target}' in genres.md")
        elif phrase == "rule":
            enough |= 1 <= int(target) <= n_rules
        elif phrase == "unchanged":
            enough |= parts["after_text"] == parts["before_text"]
        elif phrase.lower() not in parts["before_text"].lower():
            problems.append(f"EXAMPLE_SIGNS['{key}']: '{phrase}' is not in the Before of '{title}'")
        elif target not in pattern_markers:
            problems.append(f"EXAMPLE_SIGNS['{key}']: no pattern '{target}'")
        elif pattern_markers[target] in ("*(first sight)*", "Own threshold"):
            enough = True
        else:
            weak += 1
    if not enough and weak < 3:
        problems.append(f"examples.md: '{title}' is edited on {weak} cluster sign(s) and nothing stronger; a cluster needs about three")
for key in sorted(set(EXAMPLE_SIGNS) - seen_examples):
    problems.append(f"EXAMPLE_SIGNS: '{key}' matches no example; remove it from check.py")

# 13. The regression cases for scripts/eval.py are well formed. They are run by eval.py, not here: that
# costs model calls.
CASE_KEYS = {"id", "origin", "mode", "context", "input", "unchanged", "text_contains", "text_not_contains",
             "notes_contains", "judge"}
CASE_ASSERTS = {"unchanged", "text_contains", "text_not_contains", "notes_contains", "judge"}
cases_path = os.path.join(ROOT, "tests", "cases.json")
if os.path.exists(cases_path):
    try:
        with open(cases_path, encoding="utf-8") as f:
            cases = json.load(f)
    except ValueError as e:
        problems.append(f"tests/cases.json: not valid JSON ({e})")
        cases = []
    if not isinstance(cases, list) or not all(isinstance(c, dict) for c in cases):
        problems.append("tests/cases.json: must be a list of objects")
        cases = []
    ids = set()
    for case in cases:
        cid = case.get("id", "?")
        if cid in ids:
            problems.append(f"tests/cases.json: duplicate id '{cid}'")
        ids.add(cid)
        if set(case) - CASE_KEYS:
            problems.append(f"tests/cases.json: '{cid}' has unknown keys {sorted(set(case) - CASE_KEYS)}")
        if not case.get("origin") or not case.get("input"):
            problems.append(f"tests/cases.json: '{cid}' needs 'origin' and 'input'")
        if case.get("mode") not in ("chat", "embedded", "diagnosis"):
            problems.append(f"tests/cases.json: '{cid}' mode must be chat, embedded, or diagnosis")
        if not CASE_ASSERTS & set(case):
            problems.append(f"tests/cases.json: '{cid}' asserts nothing")
        if case.get("mode") == "embedded" and not case.get("context"):
            problems.append(f"tests/cases.json: '{cid}' is embedded and needs a 'context' (the calling task)")
        # A string where a list belongs would be iterated letter by letter and almost never fail.
        for key in ("id", "origin", "mode", "context", "input"):
            if key in case and not isinstance(case[key], str):
                problems.append(f"tests/cases.json: '{cid}' {key} must be a string")
        if "unchanged" in case and case["unchanged"] is not True:
            problems.append(f"tests/cases.json: '{cid}' unchanged must be true or absent")
        for key in ("text_contains", "text_not_contains", "notes_contains", "judge"):
            value = case.get(key, [])
            if not isinstance(value, list) or not value and key in case or not all(isinstance(v, str) and v for v in value):
                problems.append(f"tests/cases.json: '{cid}' {key} must be a non-empty list of non-empty strings")
        for key in ("text_contains", "text_not_contains", "notes_contains"):
            for pattern in case.get(key, []) if isinstance(case.get(key, []), list) else []:
                try:
                    re.compile(pattern)
                except re.error as e:
                    problems.append(f"tests/cases.json: '{cid}' {key} '{pattern}': {e}")

# 14. The grep commands in structures.md still work. Patterns go through files (-f): MSYS grep on
# Windows mangles backslash patterns passed as arguments by a native process, though the same
# commands work when typed in Git Bash.
samples = {
    r"[\x{200B}\x{200D}\x{2060}\x{00AD}\x{FEFF}]": "a​b\nclean\n",
    r"\p{Cyrillic}\p{Latin}|\p{Latin}\p{Cyrillic}": "сеrvice\nclean\n",
}
env = dict(os.environ, LC_ALL="C.UTF-8")
with tempfile.TemporaryDirectory() as tmp:
    for pattern, sample in samples.items():
        if pattern not in read("references/structures.md"):
            problems.append(f"structures.md: grep pattern changed, update check.py: {pattern}")
        pat_file, in_file = os.path.join(tmp, "pat"), os.path.join(tmp, "in")
        with open(pat_file, "w", encoding="utf-8", newline="\n") as f:
            f.write(pattern + "\n")
        with open(in_file, "w", encoding="utf-8", newline="\n") as f:
            f.write(sample)
        try:
            out = subprocess.run(["grep", "-cP", "-f", pat_file, in_file], capture_output=True, env=env)
        except FileNotFoundError:
            warnings.append("grep not found: the grep commands were not run (the patterns were still compared)")
            break
        if out.stdout.strip() != b"1":
            problems.append(f"grep -P '{pattern}' returned {out.stdout.strip()!r}, expected 1 ({out.stderr.decode(errors='replace').strip()})")

# 15. No build or editor leftovers in the skill directory: they get copied and shipped with the skill.
# py_compile once left scripts/__pycache__ behind.
JUNK = re.compile(r"^(__pycache__|\.DS_Store|Thumbs\.db|.*\.py[co]|.*~|.*\.orig|.*\.rej|.*\.tmp|.*\.swp)$")
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d != ".git"]
    for name in dirnames + filenames:
        if JUNK.match(name):
            problems.append(f"{os.path.relpath(os.path.join(dirpath, name), ROOT)}: leftover file, delete it")

for w in warnings:
    print("WARN:", w)
for p in problems:
    print("FAIL:", p)
print("ok" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
