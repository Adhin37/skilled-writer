#!/usr/bin/env bash
# Mechanical review rubric for skilled-writer chapters.
# usage: docs/check-chapters.sh novels/<your-slug>
#        ANCHORS="Konoha,Uchiha,chakra" docs/check-chapters.sh novels/<slug>
#
# Every check here is one the toolkit's own revision-pass claims to enforce, so a hit is a
# QC-gate failure, not merely a prose blemish. This script is deliberately independent of the
# model that wrote the chapters, so the gate cannot mark its own homework.
#
# NOTE ON LENGTH: word count is reported as a FACT and is never scored. A chapter passes on what
# it delivers (revision-pass Pass 9). The only length check here is that the frontmatter number
# is TRUE, because a wrong one propagates into state/continuity.md and corrupts every share.
set -uo pipefail
N="${1:?usage: check-chapters.sh novels/<slug>}"
CH="$N/chapters"
shopt -s nullglob
FILES=("$CH"/[0-9]*.md)
if [ ${#FILES[@]} -eq 0 ]; then echo "No chapters yet in $CH"; exit 0; fi

hr(){ printf '\n=== %s ===\n' "$1"; }
body(){ awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$1"; }

hr "INVENTORY  (wordcount is a fact, not a score — only its accuracy is checked)"
tot=0; stale=0; nodel=0
printf '%-42s %8s %8s %-9s %s\n' file wc_real fm_wc status delivers
for f in "${FILES[@]}"; do
  w=$(body "$f" | wc -w)
  fm=$(grep -m1 -E '^wordcount:' "$f" | grep -oE '[0-9]+' || echo "-")
  st=$(grep -m1 -E '^status:' "$f" | awk '{print $2}')
  dl=$(grep -m1 -E '^delivers:' "$f" | sed 's/^delivers:[[:space:]]*//' | tr -d '"')
  mark=""
  if [ "$fm" != "-" ] && [ "$fm" != "$w" ]; then mark="STALE"; stale=$((stale+1)); fi
  if [ -z "$dl" ]; then dl="** MISSING **"; nodel=$((nodel+1)); fi
  printf '%-42s %8s %8s %-9s %s %s\n' "$(basename "$f")" "$w" "$fm" "$st" "$dl" "$mark"
  tot=$((tot+w))
done
echo "TOTAL BODY WORDS: $tot   stale wordcounts: $stale   missing delivers: $nodel"
[ "$stale" -gt 0 ] && echo "  !! a stale wordcount propagates into state/continuity.md — fix both"
[ "$nodel" -gt 0 ] && echo "  !! delivers: is the Pass 9 gate. A chapter without one was never checked"

hr "CHANNEL SHARES  (speech 25-40%; thought 1-3 marks/ch; meta as needed)"
python3 - "$@" <<'PYEOF'
import re, sys, glob, os
n = sys.argv[1]; files = sorted(glob.glob(os.path.join(n, "chapters", "[0-9]*.md")))
SPEECH = re.compile(r'[“"][^”"]*[”"]')
META   = re.compile(r'\[[^\]\n]*\]')
# A thought mark opens at a word boundary and closes before punctuation/space, so bare
# contractions (don't, she'd) and plural possessives (the boys' room) can never match. An
# apostrophe is allowed INSIDE a thought only when it is word-internal — i.e. a contraction —
# which is what lets 'Start with what you're sure of.' parse as one thought and not zero.
# Nested quotes inside speech are handled by stripping speech spans first.
THOUGHT = re.compile(r"(?:(?<=^)|(?<=[\s(\"“—–]))'((?:[^'\n]|(?<=\w)'(?=\w))+?)'(?=[\s.,;:!?)\"”—–]|$)", re.M)
print("  %-40s %6s %6s %6s %6s" % ("file", "words", "speech", "thght", "meta"))
bad = 0
for f in files:
    txt = open(f, encoding="utf-8").read().split("---", 2)[-1]
    total = len(txt.split())
    sp = SPEECH.findall(txt); sp_w = sum(len(x.split()) for x in sp)
    outside = SPEECH.sub(" ", txt)          # thought/meta may not live inside speech
    th = THOUGHT.findall(outside)
    mt = META.findall(outside)
    pct = (sp_w * 100 // total) if total else 0
    flag = ""
    if pct < 10: flag = "  <-- DEFECT speech <10%: the cast is scenery"; bad += 1
    elif pct < 25: flag = "  <-- speech below target"
    if len(th) > 3: flag += "  <-- thought over budget (max 3)"
    print("  %-40s %6d %5d%% %6d %6d%s" % (os.path.basename(f), total, pct, len(th), len(mt), flag))
print("  speech-share defects: %d" % bad)
PYEOF

hr "CHANNEL COLLISIONS  (apostrophes / nested quotes misread as thought)"
coll=0
for f in "${FILES[@]}"; do
  # a ' that opens at a word boundary but never closes cleanly on the same line
  n=$(body "$f" | grep -coE "(^|[[:space:]([-])'[^']{2,}$" || true)
  [ "${n:-0}" -gt 0 ] && { echo "  $(basename "$f"): $n unterminated thought-open"; coll=$((coll+n)); }
done
echo "unterminated thought marks: $coll"

hr "WORLD ANCHOR  (story-opening §1 — first 5 chapters, ZERO is a bug)"
LEX="$N/bible/lexicon.md"
if [ -n "${ANCHORS:-}" ]; then
  IFS=',' read -r -a TERMS <<< "$ANCHORS"; echo "  anchor terms from \$ANCHORS"
elif [ -f "$LEX" ] && grep -qi 'anchor?' "$LEX"; then
  # split slash-separated aliases (Konoha / the Leaf) into separate terms; drop parentheticals
  mapfile -t TERMS < <(awk -F'|' '/^\|/ && tolower($3) ~ /yes|no/ && tolower($6) ~ /yes/ {
        t=$2; gsub(/\(.*\)/,"",t); n=split(t,a,"/");
        for(i=1;i<=n;i++){gsub(/^[ \t]+|[ \t]+$/,"",a[i]); if(a[i]!="" && a[i]!="term") print a[i]}}' "$LEX")
  echo "  anchor terms from lexicon.md (anchor? = yes)"
else
  TERMS=(); echo "  !! no anchor terms declared — add an 'anchor?' column to bible/lexicon.md"
fi
if [ ${#TERMS[@]} -gt 0 ]; then
  echo "  terms: ${TERMS[*]}"
  i=0; for f in "${FILES[@]}"; do
    i=$((i+1)); [ "$i" -gt 5 ] && break
    c=0; for t in "${TERMS[@]}"; do
      [ -z "$t" ] && continue
      # match with or without a leading article: "the Academy" also counts a bare "Academy"
      bare="${t#[Tt]he }"
      c=$((c + $(body "$f" | grep -oiF "$bare" | wc -l)))
    done
    fl=""; [ "$c" -eq 0 ] && fl="  <-- BUG: reader cannot place this chapter"
    printf '  %-40s anchor hits=%d%s\n' "$(basename "$f")" "$c" "$fl"
  done
fi

hr "MTL BANNED PHRASES (mtl-detox Part 1 — target ZERO)"
BANNED=(
 "expression changed drastically" "as expected of" "unexpectedly" "to his surprise"
 "to her surprise" "in the next instant" "in the next moment" "little did (he|she|they)"
 "couldn't help but" "could not help but" "flashed through (his|her|their) eyes"
 "trash!" "you dare" "court death" "do you know who I am"
 "at this moment" "at that time" "not simple"
 "heart trembled" "scalp went numb" "how could this be possible"
 "was speechless" "were speechless"
)
hits=0
for p in "${BANNED[@]}"; do
  m=$(grep -rniE "$p" "${FILES[@]}" 2>/dev/null)
  if [ -n "$m" ]; then echo "--- $p"; echo "$m" | sed 's/^/    /'; hits=$((hits+$(echo "$m"|wc -l))); fi
done
echo "banned-phrase hits: $hits"

hr "NARRATION EXCLAMATION MARKS (target ZERO outside dialogue)"
ex=0
for f in "${FILES[@]}"; do
  n=$(body "$f" | perl -pe 's/[\x{201C}"][^\x{201D}"]*[\x{201D}"]//g' | grep -c '!' || true)
  [ "$n" -gt 0 ] && { echo "  $(basename "$f"): $n"; ex=$((ex+n)); }
done
echo "narration '!' total: $ex"

hr "DEFAULT GESTURE SET (voice-separation §4 — target ZERO as identification)"
g=$(grep -rnoiE 'nodded|shrugged|sighed|raised an eyebrow|raised (his|her|their) eyebrow|crossed (his|her|their) arms|let out a breath|let out a sigh' "${FILES[@]}" 2>/dev/null)
echo "$g" | grep -oiE 'nodded|shrugged|sighed|raised an eyebrow|crossed .* arms|let out a breath|let out a sigh' \
  | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn
echo "gesture total: $(echo "$g" | grep -c . || echo 0)"

hr "RHETORICAL QUESTIONS IN NARRATION (ceiling 1 per 10 ch)"
for f in "${FILES[@]}"; do
  n=$(body "$f" | perl -pe 's/[\x{201C}"][^\x{201D}"]*[\x{201D}"]//g' | grep -c '?' || true)
  [ "$n" -gt 0 ] && echo "  $(basename "$f"): $n"
done

hr "CCS LEDGER INTEGRITY (continuity-summary)"
LED="$N/state/continuity.md"
if [ -f "$LED" ]; then
  nb=$(grep -cE '^=C[0-9]+=' "$LED")
  echo "blocks:   $nb   chapters on disk: ${#FILES[@]}"
  echo "dlv> lines:    $(grep -c '^dlv>' "$LED")  (must equal blocks — Pass 9 gate)"
  echo "kno> lines:    $(grep -c '^kno>' "$LED")  (must equal blocks)"
  echo "hook> lines:   $(grep -c '^hook>' "$LED")"
  echo "wld> lines:    $(grep -c '^wld>' "$LED")"
  echo "fk> lines:     $(grep -c '^fk>' "$LED")  (only if mc.foreknowledge is set)"
  grep -q '^done>.*no chapters drafted' "$LED" && [ "$nb" -gt 0 ] && \
    echo "  !! BOOK DIGEST STALE: done> says no chapters drafted, but $nb blocks exist"
  awk '/^=C/{if(b&&c>15)printf "  OVER 15 LINES: %s (%d)\n",b,c; b=$1; c=0; inb=1; next}
       /^=(ARC|BOOK)/{if(b&&c>15)printf "  OVER 15 LINES: %s (%d)\n",b,c; inb=0; b=""}
       inb&&NF{c++} END{if(b&&c>15)printf "  OVER 15 LINES: %s (%d)\n",b,c}' "$LED"
  echo "--- wc: in ledger vs measured body ---"
  for f in "${FILES[@]}"; do
    num=$(basename "$f" | grep -oE '^[0-9]+'); w=$(body "$f" | wc -w)
    lw=$(grep -m1 "^=C0*${num#"${num%%[!0]*}"}\|^=C$num=" "$LED" | grep -oE 'wc:[0-9]+' | grep -oE '[0-9]+' || true)
    [ -n "$lw" ] && [ "$lw" != "$w" ] && echo "  MISMATCH ch$num: ledger wc:$lw vs body $w"
  done
  echo "--- thread ids in ledger not in threads.md ---"
  grep -oE '[~^vx]T[0-9]+' "$LED" | sed 's/^.//' | sort -u | while read -r t; do
    grep -q "$t" "$N/state/threads.md" || echo "  ORPHAN $t"
  done
else
  echo "  NO LEDGER FILE"
fi

hr "SUMMARY"
echo "chapters=${#FILES[@]} words=$tot banned=$hits narration_bangs=$ex stale_wc=$stale missing_delivers=$nodel"
