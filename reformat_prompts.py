import re

input_path = "/home/user/OG-youtube/264_image_prompts.txt"
output_path = "/home/user/OG-youtube/264_image_prompts.txt"

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

prompts = []
current_prompt_lines = []
in_prompt = False

for line in lines:
    stripped = line.strip()

    # Skip title block, section headers, dividers, empty metadata
    if re.match(r"^═+", stripped):
        in_prompt = False
        if current_prompt_lines:
            prompts.append(" ".join(current_prompt_lines).strip())
            current_prompt_lines = []
        continue

    if re.match(r"^SECTION\s+\d+", stripped):
        continue

    if re.match(r"^THE ANCIENT BRAIN", stripped):
        continue

    if re.match(r"^264 IMAGE PROMPTS", stripped):
        continue

    if re.match(r"^Visual Style:", stripped):
        continue

    if re.match(r"^All human characters:", stripped):
        continue

    if re.match(r"^Colour palette:", stripped):
        continue

    # Detect a PROMPT N [...] line
    if re.match(r"^PROMPT\s+\d+\s*\[", stripped):
        # Save previous prompt if any
        if current_prompt_lines:
            prompts.append(" ".join(current_prompt_lines).strip())
            current_prompt_lines = []
        in_prompt = True
        continue

    # Blank line — end of prompt body, flush
    if stripped == "":
        if in_prompt and current_prompt_lines:
            prompts.append(" ".join(current_prompt_lines).strip())
            current_prompt_lines = []
            in_prompt = False
        continue

    # If we're inside a prompt, accumulate the text
    if in_prompt:
        current_prompt_lines.append(stripped)

# Flush any remaining prompt
if current_prompt_lines:
    prompts.append(" ".join(current_prompt_lines).strip())

print(f"Total prompts extracted: {len(prompts)}")

# Write clean output
with open(output_path, "w", encoding="utf-8") as f:
    for i, prompt_text in enumerate(prompts, start=1):
        f.write(f"{i}.\n{prompt_text}\n\n")

print("Done. File written.")
