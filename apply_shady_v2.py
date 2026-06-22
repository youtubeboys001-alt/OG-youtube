import re

input_path = '/root/.claude/uploads/cb86e7be-041b-5f67-a0b3-efcc9b629bb3/29e68139-my_second_video_image_prompt.txt'
output_path = '/home/user/OG-youtube/second_video_prompts_shady_v2.txt'

with open(input_path, 'r', encoding='utf-8') as f:
    text = f.read()

# ──────────────────────────────────────────────────────────────
# PROTECTION — Shield secondary characters from global replacement
# ──────────────────────────────────────────────────────────────
text = text.replace('The researcher stickman', '__RES_STICK__')
text = text.replace('the researcher stickman', '__res_stick__')
text = text.replace('a RESEARCHER in a lab coat', '__RES_LAB__')
text = text.replace('a stickman in a lab coat', '__STICK_LAB__')
text = text.replace('The IMAGINARY stickman', '__IMAGINARY_STICK__')
text = text.replace('the IMAGINARY stickman', '__imaginary_stick__')
text = text.replace('an IMAGINARY stickman', '__imaginary_stick_a__')
# Patient stickman is a secondary character, not @shady
text = text.replace('a sleeping patient stickman', '__PATIENT_STICK__')

# ──────────────────────────────────────────────────────────────
# STEP 1 — Replace main character references with @shady
# ──────────────────────────────────────────────────────────────
text = re.sub(r'\bSiffre\b', '@shady', text)
text = re.sub(r"\bSIFFRE\b(?!')", '@shady', text)

# "The [multi-word adj] stickman" — IGNORECASE catches STICKMAN all-caps labels
text = re.sub(
    r'\b[Tt]he (?:(?:\w+)\s+)*stickman\b(?!\s+in\s+a\s+lab|\s+icon)',
    '@shady', text, flags=re.IGNORECASE
)
# "A [multi-word adj] stickman [figure]"
text = re.sub(
    r'\b[Aa]n? (?:(?:\w+)\s+)*stickman(?:\s+figure)?\b(?!\s+in\s+a\s+lab|\s+icon)',
    '@shady', text, flags=re.IGNORECASE
)
text = re.sub(r'\b[Ss]ame-?(?:proportioned\s+)?stickman\b', '@shady', text, flags=re.IGNORECASE)

# ──────────────────────────────────────────────────────────────
# STEP 2 — Remove @shady's physical description
# HEAD covers all circle-head variants (no inline (?i) — use flags=re.IGNORECASE)
# ──────────────────────────────────────────────────────────────
HEAD = (
    r'(?:(?:slightly\s+)?(?:same\s+|very\s+|tiny\s+)?(?:medium|small|large|larger|tiny)\s+circle\s+head'
    r'|very\s+small\s+circle\s+head'
    r'|dotted-?line\s+circle\s+head'
    r'|dotted\s+circle\s+head)'
    r'\s*(?:\([^)]*\))?'
)

# 2a: colon separator — allow em-dash inside intro (up to 200 chars before colon)
text = re.sub(
    r'(@shady[^:.\n]{0,200}?):\s*' + HEAD + r'[^.]*\.',
    r'\1.', text, flags=re.IGNORECASE
)
# 2a': dash separator — no em-dash in intro, up to 100 chars
text = re.sub(
    r'(@shady[^:—.\n]{0,100}?)\s*—\s*' + HEAD + r'[^.]*\.',
    r'\1.', text, flags=re.IGNORECASE
)
# 2b: "@shady has a [head]" → remove sentence
text = re.sub(
    r'@shady has (?:a\s+)?' + HEAD + r'[^.]*\.\s*',
    '', text, flags=re.IGNORECASE
)
# 2c: bare @shady + head (any separator or none)
text = re.sub(
    r'(@shady)\s*[:;—]?\s*' + HEAD + r'[^.]*\.',
    r'\1.', text, flags=re.IGNORECASE
)
# 2d: "stickman [action phrase] — HEAD" (before/after panels, no colon in intro)
# Exclude ':' so "LABEL: stickman..." contexts are not matched here (handled by 2g)
text = re.sub(
    r'\bstickman\b([^:—]{0,80}?)—\s*' + HEAD + r'[^.]*\.',
    r'stickman\1.', text, flags=re.IGNORECASE
)
# 2e: "LEFT STICKMAN: HEAD" → "LEFT STICKMAN: @shady." (left figure = @shady)
text = re.sub(
    r'LEFT STICKMAN:\s*' + HEAD + r'[^.]*\.',
    'LEFT STICKMAN: @shady.', text, flags=re.IGNORECASE
)
# 2f: "RIGHT STICKMAN: HEAD" when NOT a researcher/secondary (uses negative lookahead on label)
text = re.sub(
    r'RIGHT STICKMAN(?!\s*\([^)]*(?:researcher|surface team|scientist)[^)]*\)):\s*' + HEAD + r'[^.]*\.',
    'RIGHT STICKMAN: @shady.', text, flags=re.IGNORECASE
)

# ──────────────────────────────────────────────────────────────
# STEP 2g — STICKMAN labels for @shady's progressive-stage prompts
# HOUR X / DAY X / DOCTOR STICKMAN labels are all @shady
# Remove the circle-head item from their comma-separated descriptions
# ──────────────────────────────────────────────────────────────
text = re.sub(
    r'((?:HOUR\s+\d+|DAY\s+\d+)\s+STICKMAN[^:]*:\s*(?:[^—.]{0,60}—\s*)?)' + HEAD + r'[^,]*,\s*',
    r'\1', text, flags=re.IGNORECASE
)
text = re.sub(
    r'(DOCTOR\s+STICKMAN[^:]*:\s*)' + HEAD + r'[^,]*,\s*',
    r'\1', text, flags=re.IGNORECASE
)
# FIGURE H-stage labels (deterioration stages)
text = re.sub(
    r'(FIGURE\s+H\d+:\s*)' + HEAD + r'(?:\s+(?:tilted|severely|heavily|further)[^,]*)?,?\s*',
    r'\1', text, flags=re.IGNORECASE
)

# ──────────────────────────────────────────────────────────────
# STEP 3 — Remove standalone body-line sentences
# ──────────────────────────────────────────────────────────────
text = re.sub(r'Single vertical body(?: line)?\.?\s*', '', text, flags=re.IGNORECASE)
text = re.sub(r'[Tt]he body is one vertical[^.]*\.\s*', '', text)
text = re.sub(r'[Tt]he body line is white\.\s*', '', text)
text = re.sub(r'[Bb]ody line is (?:one )?(?:horizontal|vertical)[^.]*\.\s*', '', text)
text = re.sub(r'One vertical(?:\s+white)? body(?:\s+line)?\.\s*', '', text)
text = re.sub(r'Below the head, a single body line\.\s*', '', text)

# ──────────────────────────────────────────────────────────────
# STEP 4 — Remove standalone mouth sentences
# ──────────────────────────────────────────────────────────────
text = re.sub(
    r'(?<=\. )[Aa] (?:[a-z/\-]+ ){1,6}(?:mouth|straight-line mouth)\b[^.]*\.\s*',
    '', text
)

# ──────────────────────────────────────────────────────────────
# STEP 4b — Targeted orphan physical descriptions
# ──────────────────────────────────────────────────────────────
# Back-view: "@shady's back is visible: the circle head..." → strip the list
text = re.sub(
    r"(@shady)'s back is visible:\s*the circle head[^.]*\.",
    r"\1's back is visible.", text, flags=re.IGNORECASE
)
# Brain-diagram head: "A medium circle head (outline) with inside..." (standalone)
text = re.sub(
    r'[Aa] (?:medium|small|large|tiny)\s+circle head\s*\([^)]*\)\s*with[^.]*\.\s*',
    '', text, flags=re.IGNORECASE
)
# "@shady outline (the same circle head and stick body)" parenthetical
text = re.sub(
    r'@shady\s*outline\s*\([^)]*circle head[^)]*\)',
    '@shady outline', text, flags=re.IGNORECASE
)
# Orphan head sentence after a sentence-ending punctuation
text = re.sub(
    r'([.\"\']\s+)(?:Tiny|Small|Medium|Large)\s+circle head\b[^.]*\.',
    r'\1', text, flags=re.IGNORECASE
)
# Orphan head sentence at line start
text = re.sub(
    r'(?m)^(?:Tiny|Small|Medium|Large)\s+circle head\b[^.]*\.\s*',
    '', text, flags=re.IGNORECASE
)
# Leftover "dotted body and arms" after dotted-circle-head removal
text = re.sub(r',\s*dotted body and arms\b[^.]*\.', '.', text)

# ──────────────────────────────────────────────────────────────
# STEP 5 — Restore protected secondary stickmen
# ──────────────────────────────────────────────────────────────
text = text.replace('__RES_STICK__', 'The researcher stickman')
text = text.replace('__res_stick__', 'the researcher stickman')
text = text.replace('__RES_LAB__', 'a RESEARCHER in a lab coat')
text = text.replace('__STICK_LAB__', 'a stickman in a lab coat')
text = text.replace('__IMAGINARY_STICK__', 'The IMAGINARY stickman')
text = text.replace('__imaginary_stick__', 'the IMAGINARY stickman')
text = text.replace('__imaginary_stick_a__', 'an IMAGINARY stickman')
text = text.replace('__PATIENT_STICK__', 'a sleeping patient stickman')

# Catch any contamination that slipped through
text = re.sub(r'\b(?:RESEARCHER|researcher)\s+@shady\b', 'RESEARCHER stickman', text)
text = re.sub(r'\b@shady in a lab coat\b', 'a stickman in a lab coat', text)

# ──────────────────────────────────────────────────────────────
# STEP 6 — Cleanup artifacts and whitespace
# ──────────────────────────────────────────────────────────────
text = re.sub(r'@shady\s*\(@shady\b', '@shady (', text)
text = re.sub(r'@shady\s*\(\s*\)', '@shady', text)
text = re.sub(r'@shady\.\s+@shady\.', '@shady.', text)
text = re.sub(
    r'\b[Tt]he (?:standing|walking|running|sitting|lying|real|main|REAL|MAIN)\s+@shady\b',
    '@shady', text
)
text = re.sub(r'[ \t]{2,}', ' ', text)
text = re.sub(r' \.', '.', text)
text = re.sub(r'\. \.', '.', text)
text = re.sub(r',\s+\.', '.', text)
text = re.sub(r':\s+\.', '.', text)
text = re.sub(r'\.\s+,', '.', text)
# Clean up hanging em-dash at end of label prefix (e.g. "HOUR 6 STICKMAN: small proportions — ")
text = re.sub(r'—\s*\.', '.', text)
text = re.sub(r'—\s*,', ',', text)
text = re.sub(r'\n{3,}', '\n\n', text)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(text)

# ──────────────────────────────────────────────────────────────
# Verify
# ──────────────────────────────────────────────────────────────
with open(output_path, 'r', encoding='utf-8') as f:
    out = f.read()

shady_count = out.count('@shady')
remaining_head = out.lower().count('circle head')
paragraphs = re.split(r'\n\n+', out)
cooccur = [p for p in paragraphs if '@shady' in p and 'circle head' in p.lower()]

print(f"@shady references:                    {shady_count}")
print(f"Total 'circle head' remaining:        {remaining_head}  (secondary chars only ideally)")
print(f"Prompts with @shady + circle head:    {len(cooccur)}  (ideally 0 for main-char prompts)")
if cooccur:
    for p in cooccur[:15]:
        idx = p.lower().find('circle head')
        print(f"  → ...{p[max(0,idx-60):idx+80]}...")
print(f"Output file size:                     {len(out)} characters")
print("Done.")
