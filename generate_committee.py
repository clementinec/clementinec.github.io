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
    toc: false
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

qmd_content+="""
# General Committee for CAADFutures

### The Foundation
CAAD Futures was set up under Dutch law in 1985 with three founding members; Tom Maver, Rik Schijf, and Harry Wagter with the purpose of promoting, through international conferences and publications, the advancement of Computer Aided Architectural Design in the service of those concerned with the quality of the built environment with initial capital provided by the Housing Ministry of the Netherlands Government. 

Many decades later, no longer based in the Netherlands, the Foundation continues to play a major global role in advancing the field and documenting progress in research with its biennial conference.  We work in collaboration with the several regionally focused groups that have been established over these years to support and cultivate a richly diverse research community. 

The mission of the CAAD Futures foundation continues to be:

to promote research interactions and collaborations between researchers, including PhD students and their supervisors;

to provide a platform for communication among researchers in the field of CAAD;

to play an active role in the dissemination of such progress to the scientific architectural community and the architectural practice.

### Next Conference
The CAAD Futures 2025 conference will take place in Asia, at the University of Hong Kong. 

The CAAD Futures 2027 conference will take place in the Americas. If you are interested in hosting the conference in 2027 at your institution, please email any board member by the end of the year 2024.

The CAAD Futures 2029 conference will take place in Europe.

### Board members
The current board members of the CAAD Futures Foundation are:

- Mine Özkar, Chair. Professor of Architecture at Istanbul Technical University, Türkiye.
- Christiane M. Herr, Vice-Chair. Professor, SUSTech School of Design.
- Daniel Cardoso Llach, Vice-Chair. Associate Professor, School of Architecture, Carnegie Mellon University, United States.  

Find out more about the CAAD Futures Foundation [here](https://sites.google.com/unicamp.br/caadfutures/).
"""

# Write the output to a `.qmd` file
with open("committee.qmd", "w") as file:
    file.write(qmd_content)

print("Quarto file 'committee.qmd' has been generated.")