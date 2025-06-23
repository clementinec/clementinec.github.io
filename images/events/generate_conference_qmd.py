import pandas as pd
from dataframe_to_html_converter import ConferenceHTMLGenerator

def generate_conference_qmd(excel_file_path, output_qmd='conference_papers.qmd'):
    """
    Generate a complete Quarto file from Excel data
    """
    
    # Read and process the data
    df = pd.read_excel(excel_file_path)
    generator = ConferenceHTMLGenerator(df)
    components = generator.generate_complete_html_components()
    
    # Updated CSS with full-width support and proper font scaling
    base_css = '''html {
    font-size: 16px;
    -webkit-text-size-adjust: 100%;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 1rem;
    margin: 0;
    padding: 20px;
    background-color: #f8f9fa;
}

.container {
    max-width: 100%;
    margin: 0 auto;
    padding: 0 40px;
}


@media (max-width: 768px) {
    .container {
        padding: 0 20px;
    }
}

.filters {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 30px;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.filter-tag {
    padding: 8px 16px;
    border: 2px solid transparent;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.875rem;
    transition: all 0.2s ease;
    user-select: none;
}

.filter-tag:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.filter-tag.all {
    background-color: #6c757d;
    color: white;
}

.filter-tag.active {
    border-color: #000;
    box-shadow: 0 0 0 2px rgba(0,0,0,0.1);
}

.session {
    margin-bottom: 40px;
    background: white;
    border-radius: 8px;
    padding: 30px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.session-header {
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid #e9ecef;
}

.session-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    color: #212529;
}

.session-info {
    color: #6c757d;
    font-size: 0.875rem;
}

.session, .papers-container, .paper-row {
    overflow: visible !important;
}

.papers-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
    overflow: visible !important;  /* Add this line */
}

.paper-row {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    padding: 15px;
    border-radius: 6px;
    transition: all 0.3s ease;
    cursor: pointer;
    opacity: 1;
    overflow: visible !important;  /* Add this line */

}

.paper-row:hover {
    background-color: #000;
    color: white;
    transform: translateX(5px);
}

.paper-row:hover .paper-id {
    background-color: #333;
    color: white;
    border: 2px solid white;
}

.paper-row:hover .author-tag {
    background-color: #333;
    color: white;
}

.paper-row:hover .topic-badge {
    background-color: #444 !important;
    color: white;
}

.paper-row.hidden {
    opacity: 0.2;
    pointer-events: none;
}

.paper-row.topic-highlight:hover {
    background-color: #333 !important;
    color: white !important;
}

.paper-row.session-highlight:hover {
    background-color: #333 !important;
    color: white !important;
}


.paper-row[data-abstract]:hover::before {
    display: none !important;
}

.paper-id {
    background-color: #495057;
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.875rem;
    min-width: 45px;
    text-align: center;
    flex-shrink: 0;
}

.paper-content {
    flex: 1;
    min-width: 0;
}

.paper-title {
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 8px;
    line-height: 1.4;
    color: inherit;
}

.paper-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
}

.author-tag {
    display: inline-block;
    background-color: #e9ecef;
    color: #495057;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.8125rem;
    font-weight: 500;
    transition: all 0.2s ease;
}

.additional-topics {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}

.topic-badge {
    display: inline-block;
    color: white;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.6875rem;
    font-weight: 500;
    opacity: 0.8;
}

@media (max-width: 768px) {
    .paper-row {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .paper-id {
        align-self: flex-start;
    }
}'''

    # Generate the complete Quarto file with updated format options
    qmd_content = f'''---
title: ""
format: 
  html:
    toc: false
    page-layout: custom
    grid:
      sidebar-width: 30px
      body-width: 3000px
      margin-width: 30px
      gutter-width: 1.5rem
---

```{{=html}}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
{base_css}
{components['topic_css']}
</style>

<div class="container">
    <h1>Conference Papers</h1>
    <p><strong>{components['stats']['total_papers']} papers</strong> across <strong>{components['stats']['total_topics']} topics</strong> in <strong>{components['stats']['total_sessions']} sessions</strong></p>
    
{components['filter_buttons']}

{components['sessions']}
</div>

<script>
let tooltipDiv = null;

function showTooltip(element) {{
    const abstractText = element.getAttribute('data-abstract');
    
    // Create tooltip element
    tooltipDiv = document.createElement('div');
    tooltipDiv.innerHTML = abstractText;
    tooltipDiv.style.cssText = `
        position: fixed;
        top: 50px;
        left: 50px;
        right: 50px;
        z-index: 999999;
        background: #333;
        color: white;
        padding: 20px;
        border-radius: 8px;
        font-size: 0.95em;
        line-height: 1.6;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        max-height: 70vh;
        overflow-y: auto;
    `;
    
    document.body.appendChild(tooltipDiv);
}}

function hideTooltip() {{
    if (tooltipDiv) {{
        document.body.removeChild(tooltipDiv);
        tooltipDiv = null;
    }}
}}

document.addEventListener('DOMContentLoaded', function() {{
    const filterTags = document.querySelectorAll('.filter-tag');
    const paperRows = document.querySelectorAll('.paper-row');
    const sessions = document.querySelectorAll('.session');
    
    // Map topics to CSS classes
    const topicClassMap = {components['js_topic_mapping']};
    
    filterTags.forEach(tag => {{
        tag.addEventListener('click', function() {{
            const selectedTopic = this.getAttribute('data-topic');
            
            // Update active filter
            filterTags.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Remove all topic highlighting first
            paperRows.forEach(row => {{
                row.classList.remove('topic-highlight');
                // Remove all possible topic classes
                Object.values(topicClassMap).forEach(cssClass => {{
                    row.classList.remove(cssClass);
                }});
            }});
            
            // Filter papers
            if (selectedTopic === 'all') {{
                // Show all papers, no highlighting
                paperRows.forEach(row => {{
                    row.classList.remove('hidden');
                }});
                sessions.forEach(session => {{
                    session.style.display = 'block';
                }});
            }} else {{
                // Hide/show papers based on topic
                const topicClass = topicClassMap[selectedTopic];
                
                paperRows.forEach(row => {{
                    const paperTopics = row.getAttribute('data-topics');
                    // Check if any of the paper's topics match the selected topic
                    if (paperTopics && paperTopics.split(';').some(topic => topic.trim() === selectedTopic)) {{
                        row.classList.remove('hidden');
                        // Add topic highlighting for visible papers
                        if (topicClass) {{
                            row.classList.add('topic-highlight', topicClass);
                        }}
                    }} else {{
                        row.classList.add('hidden');
                    }}
                }});
                
                // Hide sessions that have no visible papers
                sessions.forEach(session => {{
                    const visiblePapers = session.querySelectorAll('.paper-row:not(.hidden)');
                    if (visiblePapers.length === 0) {{
                        session.style.display = 'none';
                    }} else {{
                        session.style.display = 'block';
                    }}
                }});
            }}
        }});
    }});
}});
</script>
```
'''

    # Write the QMD file
    with open(output_qmd, 'w', encoding='utf-8') as f:
        f.write(qmd_content)
    
    print(f"Conference QMD file generated: {output_qmd}")
    print(f"Stats: {components['stats']['total_papers']} papers, {components['stats']['total_sessions']} sessions, {components['stats']['total_topics']} topics")
    print(f"Sessions: {', '.join(components['stats']['sessions_list'][:5])}{'...' if len(components['stats']['sessions_list']) > 5 else ''}")
    
    return output_qmd

# Usage
if __name__ == "__main__":
    # Replace with your actual Excel file path
    excel_file = "cf25dat.xlsx"  # Update this path
    qmd_file = generate_conference_qmd(excel_file)
    print(f"\nTo render: quarto render {qmd_file}")