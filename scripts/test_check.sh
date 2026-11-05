#!/usr/bin/env bash
# Mutation tests for check.py. Run: bash scripts/test_check.sh
# Each mutation gets its own copy of the skill; check.py must FAIL on every one, and the FAIL output
# must contain the expected text, so a mutation caught by the wrong check does not count.
SRC="$(cd "$(dirname "$0")/.." && pwd)"
# Python 3 under either name (macOS and some Linux distributions have only python3).
PY=""
for p in python3 python; do
  if command -v "$p" >/dev/null && "$p" -c 'import sys; sys.exit(sys.version_info < (3, 7))' 2>/dev/null; then
    PY="$(command -v "$p")"; break
  fi
done
[ -n "$PY" ] || { echo "SETUP FAILED: no Python 3 found as python3 or python"; exit 2; }
# The mutations use GNU sed (-i without a suffix, 0,/re/). On macOS install it as gsed (brew install gnu-sed).
if sed --version 2>/dev/null | grep -q GNU; then SED=sed
elif command -v gsed >/dev/null; then SED=gsed
else echo "SETUP FAILED: GNU sed not found (on macOS: brew install gnu-sed)"; exit 2
fi
sed() { command "$SED" "$@"; }
pass=0; fail=0
run() {
  local label="$1" expect="$2" cmd="$3"
  local T out; T=$(mktemp -d)
  cp -r "$SRC" "$T/slop-stop"
  ( cd "$T/slop-stop" && eval "$cmd" )
  if out=$(cd "$T/slop-stop" && "$PY" -I scripts/check.py 2>&1); then
    echo "MISSED: $label"; fail=$((fail+1))
  elif ! grep -qF -- "$expect" <<<"$out"; then
    echo "WRONG CHECK: $label (expected '$expect')"; echo "$out" | grep FAIL; fail=$((fail+1))
  else
    echo "caught: $label"; pass=$((pass+1))
  fi
  rm -rf "$T"
}
# A valid change that check.py must accept: guards against false FAILs.
run_ok() {
  local label="$1" cmd="$2"
  local T out; T=$(mktemp -d)
  cp -r "$SRC" "$T/slop-stop"
  ( cd "$T/slop-stop" && eval "$cmd" )
  if out=$(cd "$T/slop-stop" && "$PY" -I scripts/check.py 2>&1); then
    echo "accepted: $label"; pass=$((pass+1))
  else
    echo "FALSE FAIL: $label"; echo "$out" | grep FAIL; fail=$((fail+1))
  fi
  rm -rf "$T"
}
# Baseline: on the untouched skill check.py must pass. A crashing checker exits non-zero on every
# copy and would otherwise "catch" every mutation.
if ! ( cd "$SRC" && "$PY" -I scripts/check.py >/dev/null 2>&1 ); then
  echo "BASELINE FAILED: check.py does not pass on the untouched skill"; exit 1
fi
# 1. Frontmatter
run "no frontmatter"              "no frontmatter"            "sed -i '1d' SKILL.md"
run "name != directory"           "does not match directory"  "sed -i 's/^name: slop-stop$/name: slop-stopper/' SKILL.md"
run "name in upper case"          "must be lowercase"         "sed -i 's/^name: slop-stop$/name: Slop-Stop/' SKILL.md"
run "name too long"               "must be lowercase"         "sed -i 's/^name: slop-stop$/name: slop-stop$(printf -- '-x%.0s' {1..40})/' SKILL.md"
run "yaml colon in description"   "contains ': '"             "sed -i '/^description:/s/in Russian and English (/in Russian and English: (/' SKILL.md"
run "yaml ' #' in description"    "contains ': '"             "sed -i '/^description:/s/ (ADRs/ #ADRs (ADRs/' SKILL.md"
run "description starts with ["   "YAML indicator"            "sed -i 's/^description: Removes/description: [Removes/' SKILL.md"
run "description trailing space"  "edge spaces"               "sed -i '/^description:/s/\$/ /' SKILL.md"
run "description too long"        "characters, limit"         "sed -i '/^description:/s/\$/ $(printf 'x%.0s' {1..600})/' SKILL.md"
# 2. Rule references
run "no Core rules section"       "no '## Core rules' section" "sed -i 's/^## Core rules\$/## Main rules/' SKILL.md"
run "bad core rule number"        "'core rule 9' but"         "sed -i 's/(core rule 5)/(core rule 9)/' references/structures.md"
run "capitalised Core rule"       "'Core rule 9' but"         "sed -i 's/(core rule 5)/. Core rule 9 applies/' references/structures.md"
run "bare 'rule N' out of range"  "'rule 9' but"              "sed -i 's/(see rule 7)/(see rule 9)/' SKILL.md"
run "range end out of range"      "'core rules 1–9' but"      "sed -i 's/follows core rules 1–3:/follows core rules 1–9:/' references/examples.md"
run "'and N' out of range"        "'core rules 1–5 and 9' but" "sed -i 's/core rules 1–5 and 8/core rules 1–5 and 9/' SKILL.md"
# 3. Marker definitions
run "leaked marker definition"    "restates a marker definition" "echo 'Counts when three signs meet.' >> references/phrases-en.md"
run "capitalised marker definition" "restates a marker definition" "echo 'A Single occurrence means nothing.' >> references/phrases-en.md"
# 4. One marker per pattern
run "two markers on a pattern"    "needs exactly one"         "sed -i 's/^### Connective pile-up\$/### Connective pile-up *(weak)*/' references/structures.md"
run "pattern with no marker"      "needs exactly one"         "sed -i 's/^### Fake depth \*(first sight)\*\$/### Fake depth/' references/structures.md"
# 5. Examples
run "example without Changes"     "has no Changes line"       "sed -i '0,/\*\*Changes:\*\* padding removed/s//**Notes:** padding removed/' references/examples.md"
# 6. Cross-references
run "missing see-section"         "no section 'Run ups'"      "sed -i 's/see \"Run-ups\"/see \"Run ups\"/' references/phrases-en.md"
run "capitalised See"             "no section 'Chatbot linez'" "sed -i 's/See \"Chatbot lines\"/See \"Chatbot linez\"/' references/genres.md"
run "see X in the wrong file"     "no section 'Run-ups' in genres.md" "sed -i 's/see \"Run-ups\" in structures.md/see \"Run-ups\" in genres.md/' references/phrases-en.md"
run "missing (file, section)"     "no section 'Warning list'" "sed -i '0,/(SKILL.md, Output modes, Warnings)/s//(SKILL.md, Output modes, Warning list)/' references/structures.md"
run "(file, A, B) with B not in A" "no section 'Warnings' inside" "sed -i '0,/(SKILL.md, Output modes, Warnings)/s//(SKILL.md, Core rules, Warnings)/' references/structures.md"
run "'follows \"X\" in file.md'"    "no section 'One notation per numbers'" "sed -i 's/follows \"One notation per number\" in structures.md/follows \"One notation per numbers\" in structures.md/' SKILL.md"
run "missing references/ path"    "missing file 'references/genre.md'" "sed -i 's#(references/genres.md)#(references/genre.md)#' SKILL.md"
run "bare missing file name"      "missing file 'genre.md'"   "echo 'See genre.md for genres.' >> references/structures.md"
run "Process step out of range"   "'Process, step 9' but"     "sed -i 's/(Process, step 1)/(Process, step 9)/' SKILL.md"
run_ok "(MAINTAINING.md, Section) reference" "echo 'Rules live in one place (MAINTAINING.md, Where each rule lives).' >> references/genres.md"
run_ok "'see \"X\" in SKILL.md' reference"   "echo 'For modes see \"Output modes\" in SKILL.md.' >> references/genres.md"
run "(core rule N, Label) missing" "no label 'Roles' in core rule 2" "sed -i 's/\*\*Roles\.\*\*/**Role.**/' SKILL.md"
# 7. Warnings
run "unlinked 'warns'"            "says 'warn'"               "echo 'The skill warns the author here.' >> references/genres.md"
run "unlinked 'with a warning'"   "says 'warn'"               "echo 'Remove it with a warning.' >> references/genres.md"
# 8. One phrase, one pattern
run "phrase under two patterns"   "is listed under 2 patterns" "sed -i 's/«По своей сути», /«По своей сути», «Давайте разберёмся», /' references/structures.md"
# 9. Pairs
run "translation pair split"      "pair 'Интересно, что'"     "sed -i 's/inherently, deeply\\./inherently, deeply, interestingly./' references/phrases-en.md"
run "pair phrase removed"         "pair 'Примечательно, что'" "sed -i 's/«Примечательно, что», //' references/structures.md"
run "same-language pair split"    "pair 'произвести перезапуск'" "sed -i '/^| на текущий момент/a | осуществляет проверку | проверяет |' references/phrases-ru.md"
run "asymmetric pair unexplained"  "names the other pattern"  "sed -i '/^Stricter than English \"Filler phrases\" on purpose/d' references/phrases-ru.md"
run "asymmetric pair same marker"  "move the pair to PAIRS"   "sed -i 's/^## Filler phrases \*(cluster)\*\$/## Filler phrases *(first sight)*/' references/phrases-en.md"
# 10. List vs own Exception
run "listed item kept in Exception" "'importantly' is listed"  "sed -i 's/\"Note that the limit is per project\"\\./\"Note that the limit is per project\", \"Importantly, the lock is not reentrant\"./' references/structures.md"
run "stale REVIEWED_OVERLAPS entry" "no longer overlaps"     "sed -i 's/\"максимально\", \"по сути\",/\"максимально\", \"полностью\", \"по сути\",/' scripts/check.py"
# 11. Claim words and hedges in examples
run "claim word lost in an example" "lost 'только'"          "sed -i 's/у инстанса нет домена и остаются только тома/у инстанса нет домена и остаются тома/' references/examples.md"
run "rule 2 word without translation" "Russian and"         "sed -i 's/\"пока\" \/ \"may\"/\"пока\", \"вероятно\" \/ \"may\"/' SKILL.md"
run "rule 2 bullet renamed"       "no 'Hedges and scope' bullet" "sed -i 's/\*\*Hedges and scope\.\*\*/**Hedges.**/' SKILL.md"
# 12. Example signs
run "example below its threshold" "on 2 cluster sign(s)"      "sed -i 's/, (\"say most\", \"False agency\")//' scripts/check.py"
run "sign not in Before"          "'tells us' is not in the Before" "sed -i 's/> The data tells us that/> The data shows us that/' references/examples.md"
run "example without signs"       "has no entry in EXAMPLE_SIGNS" "printf '\n## 10. New\n\n**Before:**\n> X\n\n**After:**\n> Y\n\n**Changes:** none.\n' >> references/examples.md"
run "stale EXAMPLE_SIGNS key"     "'E4' matches no example"   "sed -i 's/^### E4\. False agency/### E5. False agency/' references/examples.md"
# 13. Regression cases
run "cases.json not JSON"         "not valid JSON"            "echo garbage >> tests/cases.json"
run "case with a bad mode"        "mode must be"              "sed -i 's/\"mode\": \"diagnosis\"/\"mode\": \"review\"/' tests/cases.json"
run "case with an unknown key"    "unknown keys"              "sed -i '0,/\"text_contains\"/s//\"text_contain\"/' tests/cases.json"
run "duplicate case id"           "duplicate id"              "sed -i 's/\"id\": \"interestingly-is-a-run-up\"/\"id\": \"hedges-survive-run-up-cut\"/' tests/cases.json"
run "assertion as a string"       "must be a non-empty list"  "sed -i '0,/\"text_contains\": \[\"как правило\", \"примерно\", \"30%\"\]/s//\"text_contains\": \"как правило\"/' tests/cases.json"
run "judge as a string"           "judge must be a non-empty list" "sed -i '0,/\"judge\": \[/s//\"judge\": \"x\", \"judge2\": [/' tests/cases.json"
run "unchanged not true"          "unchanged must be true"    "sed -i '0,/\"unchanged\": true/s//\"unchanged\": \"yes\"/' tests/cases.json"
run "embedded case without context" "needs a 'context'"       "sed -i '/\"context\": \"you are writing release notes for the user\",/d' tests/cases.json"
run "cases not a list"            "must be a list of objects" "printf '{\"a\": 1}' > tests/cases.json"
run "case with a broken regex"    "text_contains '(?i)never('" "sed -i 's/\"(?i)never\"/\"(?i)never(\"/' tests/cases.json"
# 15. Leftovers
run "__pycache__ left behind"     "leftover file"             "mkdir -p scripts/__pycache__ && touch scripts/__pycache__/eval.cpython-313.pyc"
# 14. grep
run "grep pattern drift"          "grep pattern changed"      "sed -i 's/x{2060}/x{2061}/' references/structures.md"
# No grep on the machine: a warning, not a failure.
if out=$(cd "$SRC" && PATH=/nonexistent "$PY" -I scripts/check.py 2>&1) && grep -q "WARN: grep not found" <<<"$out"; then
  echo "ok: missing grep is a warning"; pass=$((pass+1))
else
  echo "WRONG: missing grep must warn and pass"; echo "$out"; fail=$((fail+1))
fi
echo "caught=$pass missed=$fail"
[ "$fail" -eq 0 ]
