import re

path = "/home/user/OG-youtube/264_image_prompts.txt"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Current format has lines like "1.\n" followed by prompt text.
# Replace "N.\n" (number-dot-newline) with "N. " (number-dot-space) inline.
result = re.sub(r"^(\d+)\.\n", lambda m: f"{m.group(1)}. ", content, flags=re.MULTILINE)

with open(path, "w", encoding="utf-8") as f:
    f.write(result)

# Verify count
matches = re.findall(r"^\d+\. ", result, re.MULTILINE)
print(f"Total prompts in file: {len(matches)}")
print("Done.")
