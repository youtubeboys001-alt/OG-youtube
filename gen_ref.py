import csv

input_path = "/home/user/OG-youtube/video_editing_guide.csv"
output_path = "/home/user/OG-youtube/editing_reference.txt"

rows = []
with open(input_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

lines = []
lines.append("VIDEO EDITING REFERENCE — THE ANCIENT BRAIN")
lines.append('"What Happens to the Human Brain During Total Darkness"')
lines.append("Total Runtime: 8:49 | 264 Images | ~2 seconds each")
lines.append("=" * 65)
lines.append("")

for row in rows:
    img = row["IMAGE #"].strip()
    t_in = row["TIME IN"].strip()
    t_out = row["TIME OUT"].strip()
    audio = row["AUDIO / SCRIPT CONTENT"].strip().strip('"')
    lines.append(f"IMAGE {img:<4}  {t_in} → {t_out}   {audio}")

lines.append("")
lines.append("=" * 65)
lines.append("HOW TO USE THIS:")
lines.append("  Place IMAGE [#] on your timeline at the TIME IN shown.")
lines.append("  Each image holds for 2 seconds then cuts to the next.")
lines.append("  Match the audio/voiceover line to confirm correct sync.")
lines.append("=" * 65)

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Done. {len(rows)} entries written.")
