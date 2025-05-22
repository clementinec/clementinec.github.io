import re
from bs4 import BeautifulSoup
from pathlib import Path

# Load your Quarto file
input_path = Path("event_old.qmd")
with open(input_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract .table-container blocks
pattern = re.compile(r'<div class="table-container">.*?</div>\s*</div>', re.DOTALL)
blocks = pattern.findall(content)

# Convert each block
def to_thumbnail(block):
    soup = BeautifulSoup(block, "html.parser")

    # Image and optional link
    img_tag = soup.select_one(".image-cell img")
    a_tag = img_tag.find_parent("a") if img_tag else None
    img_src = img_tag["src"] if img_tag else ""
    link_href = a_tag["href"] if a_tag and a_tag.has_attr("href") else ""

    # Category
    cat_tag = soup.select_one(".event-category")
    category = cat_tag.get_text(strip=True) if cat_tag else ""

    # Title
    title_tag = soup.select_one(".event-heading")
    if title_tag:
        for span in title_tag.select("span"):
            span.decompose()
        title = title_tag.get_text(strip=True)
    else:
        title = ""

    # Description
    desc_tag = soup.select_one(".event-description")
    desc_html = str(desc_tag) if desc_tag else ""

    # Date and Quota (new)
    date_match = re.search(r'<strong>Date:</strong>\s*(.*?)<br>', block)
    quota_match = re.search(r'<strong>Quota:</strong>\s*(.*?)<', block)
    date_html = f"<p><strong>Date:</strong> {date_match.group(1).strip()}</p>" if date_match else ""
    quota_html = f"<p><strong>Quota:</strong> {quota_match.group(1).strip()}</p>" if quota_match else ""

    # Add date and quota just before closing desc_html
    desc_html = desc_html.rstrip("</div>") + date_html + quota_html + "</div>" if desc_html else date_html + quota_html

    # Format into output block
    result = f"""
::: {{.thumbnail-card}}

![{title}]({img_src}){{.thumbnail-img}}

### {title}

**{category}**

{desc_html}

:::
"""
    return result

# Convert and write to file
output = "\n".join(to_thumbnail(block) for block in blocks)

with open("event_thumbnails_n.qmd", "w", encoding="utf-8") as f:
    f.write(output)

print("Done. Output written to event_thumbnails_n.qmd")
