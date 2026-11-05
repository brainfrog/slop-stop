"""Regression run of the slop-stop skill on tests/cases.json. Run: python -I scripts/eval.py [options]

Every case is a past review finding turned into an input and the behaviour it must produce. The skill
(SKILL.md and all references) goes to a fresh `claude -p` session as its system prompt; the answer is
checked by substring rules and, where a rule cannot judge, by one yes/no question to a second session.
Costs model calls: the run prints its cost. Not loaded when the skill runs.

Options: --case ID (repeatable), --runs N (repeat each case, all runs must pass), --model NAME,
--jobs N (parallel cases, default 4), --show (print every answer), --skill-dir DIR (run the cases
against another copy of the skill, e.g. a backup, to see that they catch its old defects),
--realistic (give the model only SKILL.md and the Read tool, as Claude Code does, and fail a case when
it does not open the references that SKILL.md, Process, step 1 requires; slower and dearer).
"""
import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ["SKILL.md", "references/genres.md", "references/structures.md", "references/phrases-ru.md",
         "references/phrases-en.md", "references/examples.md"]
SEPARATOR = "=== NOTES ==="
MODES = {
    "chat": "Edit the text below with the skill, in chat mode.",
    "embedded": "You are one step of a larger task ({context}). Apply the skill to the text below in embedded mode.",
    "diagnosis": "Does the text below sound AI-generated? Answer with the skill, in diagnosis mode.",
}
FORMAT = (f"Answer format, for this test harness only: first the final text (in diagnosis mode, your findings and "
          f"verdict), then a line that says exactly {SEPARATOR}, then everything else: the change list, warnings, "
          f"the report to the calling task. If there is nothing else, still write the line.")


def read(rel, root=ROOT):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return f.read()


def claude(system, prompt, model, read_dir=None):
    """One fresh session with no settings and no skills. Without read_dir it has no tools; with read_dir it
    may only Read, inside that directory. Returns (answer, cost in USD, files it read)."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as f:
        f.write(system)
        system_file = f.name
    cmd = ["claude", "-p", "--no-session-persistence", "--setting-sources", "", "--disable-slash-commands",
           "--system-prompt-file", system_file]
    if read_dir:
        cmd += ["--tools", "Read", "--allowedTools", "Read", "--add-dir", read_dir,
                "--output-format", "stream-json", "--verbose"]
    else:
        cmd += ["--tools", "", "--output-format", "json"]
    if model:
        cmd += ["--model", model]
    try:
        out = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                             timeout=900, shell=os.name == "nt")
    finally:
        os.unlink(system_file)
    events = []
    for line in out.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    data = next((e for e in reversed(events) if e.get("type") == "result"), None)
    if data is None:
        raise RuntimeError(f"claude returned no result: {(out.stdout or out.stderr)[:300]}")
    if data.get("is_error"):
        raise RuntimeError(f"claude error: {data.get('result')}")
    reads = [block.get("input", {}).get("file_path", "")
             for e in events if e.get("type") == "assistant"
             for block in e.get("message", {}).get("content", [])
             if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Read"]
    return data.get("result", ""), data.get("total_cost_usd", 0.0), reads


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def judge(case, answer, model):
    questions = case["judge"]
    system = ("You check one edit made by a text-editing tool. Answer every question about the response with "
              "true or false. Reply with JSON only: {\"answers\": [true, false, ...]}, one value per question, in order.")
    prompt = (f"Source text:\n<<<\n{case['input']}\n>>>\n\nThe tool's full response:\n<<<\n{answer}\n>>>\n\nQuestions:\n"
              + "\n".join(f"{i + 1}. {q}" for i, q in enumerate(questions)))
    verdict, cost, _ = claude(system, prompt, model)
    m = re.search(r"\{.*\}", verdict, re.S)
    try:
        answers = json.loads(m.group(0))["answers"] if m else None
    except ValueError:
        answers = None
    if not isinstance(answers, list) or len(answers) != len(questions):
        return [f"judge gave no usable answer: {verdict[:200]}"], cost
    return [f"judge said no: {q}" for q, a in zip(questions, answers) if a is not True], cost


def run_case(case, skill, model, read_dir=None):
    prompt = (MODES[case["mode"]].format(context=case.get("context", "")) + " "
              + ("" if case["mode"] == "embedded" else case.get("context", "")) + "\n\n" + FORMAT
              + f"\n\nText:\n<<<\n{case['input']}\n>>>")
    answer, cost, reads = claude(skill, prompt, model, read_dir)
    text, sep, notes = answer.partition(SEPARATOR)
    text = re.sub(r"^\s*<<<\s*|\s*>>>\s*$", "", text.strip())
    failures = [] if sep else [f"no '{SEPARATOR}' line in the answer"]
    if read_dir:  # SKILL.md, Process, step 1: what must be read before editing
        language = "ru" if re.search("[а-яё]", case["input"], re.I) else "en"
        needed = ["genres.md", "structures.md", f"phrases-{language}.md"]
        read_names = {os.path.basename(r) for r in reads}
        failures += [f"did not read references/{n}" for n in needed if n not in read_names]
    if case.get("unchanged") and norm(text) != norm(case["input"]):
        failures.append("text was changed, expected it unchanged")
    for p in case.get("text_contains", []):
        if not re.search(p, text):
            failures.append(f"text lacks /{p}/")
    for p in case.get("text_not_contains", []):
        if re.search(p, text):
            failures.append(f"text contains /{p}/")
    for p in case.get("notes_contains", []):
        if not re.search(p, notes):
            failures.append(f"notes lack /{p}/")
    if case.get("judge"):
        more, judge_cost = judge(case, answer, model)
        failures += more
        cost += judge_cost
    return answer, failures, cost


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", action="append", default=[])
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--model")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--skill-dir", default=ROOT)
    ap.add_argument("--realistic", action="store_true")
    args = ap.parse_args()

    if args.realistic:
        # As in Claude Code: only SKILL.md is loaded; the model opens the references itself, or does not.
        skill = (f"You have the slop-stop skill. Its SKILL.md follows. Relative links in it point into "
                 f"{os.path.abspath(args.skill_dir)}; the Read tool can open them.\n\n" + read("SKILL.md", args.skill_dir))
    else:
        skill = ("The following is the slop-stop skill: SKILL.md and every file it references. Follow it exactly.\n\n"
                 + "\n\n".join(f"===== {rel} =====\n{read(rel, args.skill_dir)}" for rel in FILES))
    cases = json.loads(read("tests/cases.json"))
    if args.case:
        unknown = set(args.case) - {c["id"] for c in cases}
        if unknown:
            sys.exit(f"unknown case id(s): {', '.join(sorted(unknown))}")
        cases = [c for c in cases if c["id"] in args.case]
    jobs = [(c, n) for c in cases for n in range(args.runs)]

    total, failed, errored = 0.0, set(), set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        read_dir = os.path.abspath(args.skill_dir) if args.realistic else None
        futures = {pool.submit(run_case, c, skill, args.model, read_dir): (c, n) for c, n in jobs}
        for fut in concurrent.futures.as_completed(futures):
            case, n = futures[fut]
            label = case["id"] + (f" #{n + 1}" if args.runs > 1 else "")
            try:
                answer, failures, cost = fut.result()
            except Exception as e:
                # A call that never produced an answer (usage limit, network, CLI) says nothing about the
                # skill: report it apart from failures, and do not let it hide the other results.
                print(f"ERROR: {label}\n      {e}")
                errored.add(case["id"])
                continue
            total += cost
            print(("FAIL: " if failures else "ok:   ") + label)
            for f in failures:
                print("      " + f)
            if failures:
                failed.add(case["id"])
                print("      origin: " + case["origin"])
            if args.show or failures:
                print("      answer: " + answer.replace("\n", "\n              "))
    errored -= failed
    passed = len(cases) - len(failed) - len(errored)
    print(f"{passed}/{len(cases)} cases passed, {len(failed)} failed, {len(errored)} not run (errors), cost ${total:.2f}")
    sys.exit(1 if failed else 2 if errored else 0)


if __name__ == "__main__":
    main()
