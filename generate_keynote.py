import json

# Load the committee data
with open("keynotes.json", "r") as file:
    data = json.load(file)

# Initialize Quarto `.qmd` content with the required YAML front matter
qmd_content = """---
title: "CAADFutures 2025: Keynote Speakers"
format:
  html:
    theme: quartz
    toc: false
---
"""

qmd_content+="""
# Keynotes

As part of CAAD Futures 2025, Keynote Sessions will feature presentations by two distinguished keynote speakers and three outstanding early-career women researchers. They will share innovative insights across the conference days, July 2–4, 2025. 
"""

# Add styling for the table layout
qmd_content += """
```{=html}
<style>
.table-container {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    padding: 25px;
    border: 0.25px dotted #aaa;
    border-radius: 10px;
}
.image-cell {
    flex: 0 0 200px;
    text-align: center;
    padding-right: 30px;
}
.image-cell img {
    max-width: 300px;
    max-height: 300px;
    object-fit: cover;
    border-radius: 10px;
}
.text-cell {
    flex: 1;
}
.text-cell h3 {
    margin: 0;
    font-size: 1.2em;
    font-weight: bold;
}
.text-cell p {
    margin: 5px 0;
    font-size: 1.1em;
    line-height: 1.5;
}
</style>
```
"""

# Add each committee member as a styled table
for member in data["keynotes"]:
    qmd_content += f"""
```{{=html}}
<div class="table-container">
    <div class="image-cell">
        <img src="{member['image']}" alt="{member['name']}">
    </div>
    <div class="text-cell">
        <h3>{member['role']}: {member['name']}</h3>
        <p>{member['shortbio']}</p>
    </div>
</div>
```
"""



# Write the output to a `.qmd` file
with open("keynote.qmd", "w") as file:
    file.write(qmd_content)

print("Quarto file 'keynote.qmd' has been generated.")