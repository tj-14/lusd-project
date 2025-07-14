import csv
from pathlib import Path

# Load the CSV prompts
csv_path = Path("prompt_tan_instruction.csv")
input_dir = Path("input")
results_dir = Path("results")

prompt_map = {}

with open(csv_path, newline="") as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        prompt_map[str(idx)] = row["instruction"].strip()


# Determine tag color based on instruction
def get_tag_class(instruction: str) -> str:
    lower = instruction.lower()
    if "add" in lower:
        return "is-info"
    elif "replace" in lower or "change" in lower:
        return "is-success"
    else:
        return "is-warning"


# Collect carousel HTML
carousel_items = []

for result_file in sorted(results_dir.glob("*.png")):
    result_name = result_file.name  # e.g. "1_4.png"
    input_id = result_name.split("_")[0]  # e.g. "1"
    input_file = input_dir / f"{input_id}.png"
    if not input_file.exists():
        continue

    instruction = prompt_map.get(input_id, "&nbsp;")
    tag_class = get_tag_class(instruction)

    html_block = f"""\
          <div class="item 100">
            <div class="box has-text-centered">
              <p><strong>Input</strong></p>
              <img src="./static/images/input/{input_id}.png" style="max-height: 150px;">
              <p class="mt-2">
                <span class="tag {tag_class} is-light is-medium">{instruction}</span>
              </p>
              <p class="mt-2"><strong>Output</strong></p>
              <img src="./static/images/results/{result_name}" style="max-height: 150px;">
            </div>
          </div>"""
    carousel_items.append(html_block)

# Write to output file
output_html = "\n".join(carousel_items)
with open("lusd_carousel_items.html", "w") as f:
    f.write(output_html)

print("✅ Carousel HTML generated in lusd_carousel_items.html")
