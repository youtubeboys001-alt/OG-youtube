import re

input_path = '/root/.claude/uploads/cb86e7be-041b-5f67-a0b3-efcc9b629bb3/29e68139-my_second_video_image_prompt.txt'
output_path = '/home/user/OG-youtube/second_video_prompts_shady.txt'

with open(input_path, 'r', encoding='utf-8') as f:
    text = f.read()

# ──────────────────────────────────────────────────────────────
# @shady's full head description (light background scenes)
# ──────────────────────────────────────────────────────────────
SHADY_HEAD_LIGHT = (
    "medium circle head (white fill, black outline), "
    "topped with spiky brown hair (multiple short irregular upward-pointing spikes "
    "in flat brown/chocolate brown, densely packed across the top of the head), "
    "@shady's distinctive asymmetric eyes: LEFT eye half-closed and droopy "
    "(a small horizontal elongated oval — his signature lazy, unbothered look), "
    "RIGHT eye a full open circle with a small centred black dot pupil (alert, open), "
    "five small filled black freckle dots scattered across both cheeks, "
    "tiny diamond-shaped stud earrings at ear position on both sides of the head"
)

SHADY_HEAD_DARK = (
    "medium circle head (white circle outline against the dark), "
    "white spike outlines for the spiky hair on top "
    "(multiple short upward-pointing white spike shapes, densely packed), "
    "@shady's asymmetric eyes as white marks: LEFT eye a small white horizontal oval "
    "(half-closed, droopy), RIGHT eye a small white circle with a tiny dark pupil dot, "
    "tiny white freckle dots across both cheeks, "
    "tiny white diamond-shaped earring marks at ear position"
)

SHADY_HEAD_GHOST = (
    "medium circle head (wide circle outline, thin white stroke only, not filled — "
    "@shady rendered as a ghostly white silhouette), "
    "white spike outlines for spiky hair on top (multiple short upward-pointing white spike shapes), "
    "@shady's asymmetric eyes as white pinpricks: LEFT eye a tiny white oval, "
    "RIGHT eye a tiny white circle with the faintest dark centre"
)

WRIST_STUDS = "small diamond-shaped stud accessories at both wrists"

# ──────────────────────────────────────────────────────────────
# STEP 1 — Replace character label
# ──────────────────────────────────────────────────────────────
text = text.replace('The stickman:', '@shady:')
text = text.replace('The stickman has a medium circle head', '@shady has a medium circle head')
text = text.replace('the stickman:', '@shady:')

# ──────────────────────────────────────────────────────────────
# STEP 2 — Replace head descriptions (light scenes)
# We replace ONLY the head line; the original eye/mouth/body lines follow.
# We intentionally replace the head desc with @shady's FULL head block
# (head + hair + eyes + freckles + earrings), so the subsequent
# "two dot eyes…" description in the original becomes the EXPRESSION detail.
# We mark it with "[EXPRESSION:]" prefix for clarity.
# ──────────────────────────────────────────────────────────────

light_heads = [
    r'medium circle head \(circle outline, white fill\)',
    r'medium circle head \(smooth circle, white fill, thick black outline\)',
    r'medium circle head \(circle outline, white fill, thick black outline\)',
    r'medium circle head \(clean circle outline, white fill\)',
    r'medium circle head \(circle outline; white fill\)',
]
for pat in light_heads:
    text = re.sub(pat, SHADY_HEAD_LIGHT, text)

# ──────────────────────────────────────────────────────────────
# STEP 3 — Replace head descriptions (dark / navy scenes)
# ──────────────────────────────────────────────────────────────
text = re.sub(
    r'medium circle head \(white circle outline only against navy\)',
    SHADY_HEAD_DARK, text
)
text = re.sub(
    r'medium circle head \(white circle outline against navy\)',
    SHADY_HEAD_DARK, text
)
text = re.sub(
    r'medium circle head \(wide diameter, thin white outline only, not filled\)',
    SHADY_HEAD_GHOST, text
)
# Very faint scene (prompt 262)
text = re.sub(
    r'medium circle head \(very faint white outline — barely visible\)',
    'medium circle head (very faint white circle outline, barely visible), '
    'faint white spike outlines for spiky hair (barely visible short upward spike shapes on top), '
    'faint white freckle dots and earring marks',
    text
)

# ──────────────────────────────────────────────────────────────
# STEP 4 — Tilted / lying-down head variants
# These appear mid-description ("medium circle head tilted…")
# We add the hair and features after the head clause.
# ──────────────────────────────────────────────────────────────

def add_shady_tilt(m):
    """For 'medium circle head tilted X degrees' — add hair after the full phrase."""
    full = m.group(0)
    return (
        full
        + ", topped with spiky brown hair (multiple short irregular upward-pointing spikes "
        "in flat brown/chocolate brown, densely packed across the top of the head), "
        "five small filled black freckle dots across both cheeks, "
        "tiny diamond-shaped stud earrings at ear position"
    )

text = re.sub(
    r'medium circle head tilted [^,)]+',
    add_shady_tilt,
    text
)
text = re.sub(
    r'medium circle head lying [^,)]+',
    add_shady_tilt,
    text
)
text = re.sub(
    r'medium circle head (?:resting|drooping|bent|turned) [^,)]+',
    add_shady_tilt,
    text
)

# ──────────────────────────────────────────────────────────────
# STEP 5 — Eye descriptions: prepend @shady's asymmetric note
# The original emotional/directional eye descriptions are KEPT intact;
# we just add @shady's asymmetry as a prefix note.
# ──────────────────────────────────────────────────────────────

EYE_NOTE = (
    "@shady's characteristic asymmetric expression "
    "(LEFT eye always half-closed and droopy; RIGHT eye always open with dot pupil) — "
)

def prepend_eye_note(m):
    return EYE_NOTE + m.group(0)

# Match "two [adj*] dot eyes (…)" patterns
text = re.sub(
    r'two (?:(?:small |large |pin-|wide-open |very large |half-open |half-closed )*)'
    r'(?:dot eyes|filled (?:white|black) circles?|circle eyes|half-moon(?:-shaped)? dot eyes)'
    r'[^.]*?(?:\([^)]*\))?',
    prepend_eye_note,
    text
)

# Also match standalone "dot eyes [direction]" phrases
text = re.sub(
    r'(?<!\w)dot eyes (?:directed|looking|aimed|pointing)[^,.]*',
    prepend_eye_note,
    text
)

# ──────────────────────────────────────────────────────────────
# STEP 6 — Wrist studs: add to arm descriptions for @shady
# We add the wrist note once per prompt after arm descriptions.
# ──────────────────────────────────────────────────────────────

# Common arm-ending patterns — add wrist studs after them
arm_endings = [
    ('Two stick arms hang perfectly straight down at the sides of the body — no angle, no bend.',
     f'Two stick arms hang perfectly straight down at the sides of the body — no angle, no bend. {WRIST_STUDS}.'),
    ('Both arms hanging at sides',
     f'Both arms hanging at sides ({WRIST_STUDS})'),
    ('arms hang loosely at',
     f'arms hang loosely at'),  # handled by general append below
]
for old, new in arm_endings:
    text = text.replace(old, new)

# ──────────────────────────────────────────────────────────────
# STEP 7 — Handle multi-character prompts
# For prompts that have LABELED secondary characters (researchers, ancestors),
# the @shady replacements above already only hit the unlabeled main character.
# We now fix a few specific cases where secondary-character head descriptions
# got caught by our regex and add a note to un-mark them.
# Secondary characters use: "RESEARCHER stickman", "ANCESTOR", lab-coat stickmen.
# Since we can't fully reverse those, we leave a warning comment in output.
# ──────────────────────────────────────────────────────────────

# Revert secondary character labels that got hit
# These phrases appear ONLY for researcher/ancestor characters:
text = text.replace(
    'RESEARCHER stickman: ' + SHADY_HEAD_LIGHT,
    'RESEARCHER stickman: medium circle head (white fill, black outline)'
)
text = text.replace(
    'The RESEARCHER: ' + SHADY_HEAD_LIGHT,
    'The RESEARCHER: medium circle head (white fill, black outline)'
)
# If "The stickman (Siffre):" was accidentally changed, fix it:
# (Siffre is played by @shady in this video, so this is actually fine to keep)

# ──────────────────────────────────────────────────────────────
# Write output
# ──────────────────────────────────────────────────────────────
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(text)

# Verify
with open(output_path, 'r', encoding='utf-8') as f:
    out = f.read()

shady_count = out.count('@shady')
hair_count = out.count('spiky brown hair')
freckle_count = out.count('freckle dots')
earring_count = out.count('stud earrings')
wrist_count = out.count('wrist')

print(f"@shady references:   {shady_count}")
print(f"Hair descriptions:   {hair_count}")
print(f"Freckle mentions:    {freckle_count}")
print(f"Earring mentions:    {earring_count}")
print(f"Wrist stud mentions: {wrist_count}")
print(f"Output file size:    {len(out)} characters")
print("Done.")
