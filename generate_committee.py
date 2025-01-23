import json

# Load the committee data
with open("committee.json", "r") as file:
    data = json.load(file)

# Initialize Quarto `.qmd` content with the required YAML front matter
qmd_content = """---
title: "Organizing Team for CAAD Futures 2025"
format:
  html:
    theme: quartz
    toc: true
---
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
for member in data["committee"]:
    qmd_content += f"""
```{{=html}}
<div class="table-container">
    <div class="image-cell">
        <img src="{member['image']}" alt="{member['name']}">
    </div>
    <div class="text-cell">
        <h3>{member['role']}: {member['name']}</h3>
        <p>{member['bio']}</p>
    </div>
</div>
```
"""

# Write the output to a `.qmd` file
with open("committee.qmd", "w") as file:
    file.write(qmd_content)

print("Quarto file 'committee.qmd' has been generated.")