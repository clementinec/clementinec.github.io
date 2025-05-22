import re
from bs4 import BeautifulSoup
from pathlib import Path

# Load your Quarto file
input_path = Path("event_old.qmd")  # Ensure this file exists
with open(input_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract .table-container blocks
pattern = re.compile(r'<div class="table-container">.*?</div>\s*</div>', re.DOTALL)
blocks = pattern.findall(content)

# Helper to convert each block
def to_thumbnail(block):
    soup = BeautifulSoup(block, "html.parser")

    # Image and optional link
    img_tag = soup.select_one(".image-cell img")
    a_tag = img_tag.find_parent("a") if img_tag else None
    img_src = img_tag["src"] if img_tag else ""
    link_href = a_tag["href"] if a_tag and a_tag.has_attr("href") else ""

    # Category from div.event-category
    cat_tag = soup.select_one(".event-category")
    category = cat_tag.get_text(strip=True) if cat_tag else ""

    # Title from h1.event-heading (remove span first)
    title_tag = soup.select_one(".event-heading")
    if title_tag:
        span = title_tag.find("span")
        if span:
            span.decompose()
        title = title_tag.get_text(strip=True)
    else:
        title = "Untitled"

    # Writeup fallback from <p> or <h3> in .text-cell
    writeup = ""
    text_cell = soup.select_one(".text-cell")
    if text_cell:
        all_p = text_cell.find_all("p")
        for p in all_p:
            if "event-category" not in p.get("class", []):
                writeup = p.get_text(strip=True)
                break
        if not writeup:
            h3 = text_cell.find("h3")
            if h3:
                writeup = h3.get_text(strip=True)

    # Image wrapped in link if applicable
    image_html = f'<img src="{img_src}" alt="{title}">'
    if link_href:
        image_html = f'<a href="{link_href}">{image_html}</a>'

    return f"""
<div class="thumbnail-card">
  {image_html}
  <div class="caption">
    <h3>{title}</h3>
    <p class="event-category">{category}</p>
    <p class="writeup">{writeup}</p>
  </div>
</div>
""".strip()

# Convert all blocks
converted_blocks = [to_thumbnail(block) for block in blocks]
converted_html = "\n\n".join(converted_blocks)

# CSS styling
css = """
<style>
.thumbnail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  padding: 20px;
}
.thumbnail-card {
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
  text-align: center;
  background: #fff;
  transition: transform 0.2s ease;
}
.thumbnail-card:hover {
  transform: scale(1.03);
}
.thumbnail-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}
.caption {
  padding: 10px;
}
.caption h3 {
  font-size: 1.2em;
  font-weight: 600;
  margin: 0 0 0.2em 0;
}
.caption .event-category {
  font-size: 0.9em;
  color: #666;
  margin: 0 0 0.5em 0;
}
.caption .writeup {
  font-size: 0.95em;
  color: #444;
  line-height: 1.4;
}
</style>
"""

# Quarto header and passthrough HTML block
header = """---
title: "Events Lineup"
format:
  html:
    toc: false
---

```{=html}
""" + css + f"""

<div class="thumbnail-grid">
{converted_html}
</div>
```"""

# Save to .qmd
output_path = Path("event_thumbnails.qmd")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(header)

print("✅ .qmd file with HTML passthrough saved as:", output_path)
