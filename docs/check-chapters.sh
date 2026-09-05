#!/usr/bin/env bash
# Mechanical review rubric for skilled-writer chapters.
# usage: docs/check-chapters.sh novels/<your-slug>
# Every check here is one the toolkit's own revision-pass claims to enforce,
# so a hit is a QC-gate failure, not merely a prose blemish.
# Usage: check_chapters.sh [novel-dir]
set -uo pipefail
N="${1:?usage: check-chapters.sh novels/<slug>}"
CH="$N/chapters"
shopt -s nullglob
FILES=("$CH"/[0-9]*.md)
if [ ${#FILES[@]} -eq 0 ]; then echo "No chapters yet in $CH"; exit 0; fi

hr(){ printf '\n=== %s ===\n' "$1"; }

hr "INVENTORY"
tot=0
printf '%-42s %7s %9s %9s\n' file wc_real fm_wc status
for f in "${FILES[@]}"; do
  # body = everything after the closing --- of frontmatter
  w=$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$f" | wc -w)
  fm=$(grep -m1 -E '^wordcount:' "$f" | grep -oE '[0-9]+' || echo "-")
  st=$(grep -m1 -E '^status:' "$f" | awk '{print $2}')
  printf '%-42s %7s %9s %9s\n' "$(basename "$f")" "$w" "$fm" "$st"
  tot=$((tot+w))
done
echo "TOTAL BODY WORDS: $tot"

hr "DIALOGUE SHARE (target 25-40%, under 10% = defect)"
TGT=$(grep -m1 -E 'target_words:' "$N/novel.md" | grep -oE '[0-9]+')
for f in "${FILES[@]}"; do
  body=$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$f")
  t=$(echo "$body" | wc -w); d=$(echo "$body" | grep -oE '"[^"]*"' | wc -w)
  pct=$(( d*100/t ))
  flag=""; [ "$pct" -lt 10 ] && flag="  <-- DEFECT (<10%)"
  [ "$pct" -ge 10 ] && [ "$pct" -lt 25 ] && flag="  <-- below target"
  dev=$(( (t-TGT)*100/TGT ))
  printf '  %-40s dlg=%2d%%  words=%s (%+d%% vs target %s)%s\n' "$(basename "$f")" "$pct" "$t" "$dev" "$TGT" "$flag"
done

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
# strip "..." spans, then look for ! in what remains
ex=0
for f in "${FILES[@]}"; do
  n=$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$f" \
      | perl -pe 's/[\x{201C}"][^\x{201D}"]*[\x{201D}"]//g' | grep -c '!' || true)
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
  n=$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$f" \
      | perl -pe 's/[\x{201C}"][^\x{201D}"]*[\x{201D}"]//g' | grep -c '?' || true)
  [ "$n" -gt 0 ] && echo "  $(basename "$f"): $n"
done

hr "CCS LEDGER INTEGRITY (continuity-summary)"
LED="$N/state/continuity.md"
if [ -f "$LED" ]; then
  echo "blocks:   $(grep -cE '^=C[0-9]+=' "$LED")   chapters on disk: ${#FILES[@]}"
  echo "missing kno>:  $(grep -cE '^=C' "$LED")-blocks vs $(grep -c '^kno>' "$LED") kno> lines"
  echo "missing hook>: $(grep -c '^hook>' "$LED") hook> lines"
  echo "wld> lines:    $(grep -c '^wld>' "$LED")"
  awk '/^=C/{if(b&&c>13)printf "  OVER 13 LINES: %s (%d)\n",b,c; b=$1; c=0; inb=1; next}
       /^=(ARC|BOOK)/{if(b&&c>13)printf "  OVER 13 LINES: %s (%d)\n",b,c; inb=0; b=""}
       inb&&NF{c++} END{if(b&&c>13)printf "  OVER 13 LINES: %s (%d)\n",b,c}' "$LED"
  echo "--- thread ids in ledger not in threads.md ---"
  grep -oE '[~^vx]T[0-9]+' "$LED" | sed 's/^.//' | sort -u | while read -r t; do
    grep -q "$t" "$N/state/threads.md" || echo "  ORPHAN $t"
  done
else
  echo "  NO LEDGER FILE"
fi

hr "SUMMARY"
echo "chapters=${#FILES[@]} words=$tot banned=$hits narration_bangs=$ex"
