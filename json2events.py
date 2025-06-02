import json
from pathlib import Path

# Load JSON
with open("events.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Render thumbnail card safely
def render_card(event):
    html = f"""
<div class="thumbnail-card">
  <a href="event_details.html#{event.get('id', '')}">
    <img src="{event.get('image', '')}" alt="{event.get('title', '')}">
  </a>
  <div class="caption">
    <h3>{event.get('title', '')}<br></h3>
    <p class="event-category">{event.get('type', '')}</p>
    <p class="writeup">{event.get('intro', '')}</p>"""

    if 'date' in event:
        html += f'\n    <p><strong>Date:</strong> {event["date"]}</p>'
    if 'quota' in event:
        html += f'\n    <p><strong>Quota:</strong> {event["quota"]}</p>'
    if 'cost' in event:
        html += f'\n    <p><strong>Cost:</strong> {event["cost"]}</p>'

    html += "\n  </div>\n</div>"
    return html

# Begin full .qmd document
output_html = """---
title: "Events Lineup"
format:
  html:
    toc: false
---

```{=html}
<style>
.thumbnail-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  padding: 20px;
}

.thumbnail-grid {
  display: contents;
}

.divider {
  grid-column: 1 / -1;
  height: 2px;
  background: #ddd;
  margin: 20px 0;
}

.thumbnail-card {
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
  text-align: left;
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
  letter-spacing: normal;       /* ✅ Reset letter spacing */
  font-family: sans-serif;      /* ✅ Optional, if overridden globally */
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

<div class="thumbnail-wrapper">
<div class="thumbnail-grid">
"""

# Add "tours"
for event in data["tours"]:
    output_html += render_card(event)

# Add divider
output_html += """
</div>
<div class="divider"></div>
<div class="thumbnail-grid">
"""

# Add "social"
for event in data["social"]:
    output_html += render_card(event)

# Close out the HTML block
output_html += """
</div>
</div>
```
"""

output_path = "events_lineup.qmd"
with open(output_path, "w", encoding="utf-8") as f:
  f.write(output_html)

print(f"Saved to {output_path}")