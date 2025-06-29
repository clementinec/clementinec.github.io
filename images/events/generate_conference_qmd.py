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
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
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
    <h1>Technical Programme</h1>
    <p>This technical programme only reflects author names and abstracts from <strong>EasyChair</strong> submission records. 
    Edits to authorship/abstract made in camera-ready submission will be reflected in conference proceedings.</p>
    <p><strong>{components['stats']['total_papers']} papers</strong> across <strong>{components['stats']['total_topics']} topics</strong> in <strong>{components['stats']['total_sessions']} sessions</strong></p>
    
{components['day_filters']}

{components['filter_buttons']}

{components['sessions']}
</div>

<script>
let showTimer, hideTimer, tooltipDiv;

function createTooltip(text) {{
  if (tooltipDiv) tooltipDiv.remove();
  tooltipDiv = document.createElement('div');
  tooltipDiv.innerHTML = text;
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
    opacity: 0;
    transition: opacity 0.2s ease-in-out;
  `;
  document.body.appendChild(tooltipDiv);
  requestAnimationFrame(() => {{
    tooltipDiv.style.opacity = '1';
  }});
}}

function showTooltip(element) {{
  clearTimeout(hideTimer);
  const text = element.getAttribute('data-abstract');
  showTimer = setTimeout(() => {{
    createTooltip(text);
  }}, 200);  // delay before showing
}}

function hideTooltip() {{
  clearTimeout(showTimer);
  if (!tooltipDiv) return;
  tooltipDiv.style.opacity = '0';
  hideTimer = setTimeout(() => {{
    if (tooltipDiv) {{
      tooltipDiv.remove();
      tooltipDiv = null;
    }}
  }}, 200);  // match the fade-out duration
}}

// Attach to your elements:
document.querySelectorAll('.has-abstract').forEach(el => {{
  el.addEventListener('mouseenter', () => showTooltip(el));
  el.addEventListener('mouseleave', hideTooltip);
}});


document.addEventListener('DOMContentLoaded', function() {{
    const dayFilterTags = document.querySelectorAll('.day-filter-tag');
    const filterTags = document.querySelectorAll('.filter-tag');
    const paperRows = document.querySelectorAll('.paper-row');
    const sessions = document.querySelectorAll('.session');
    
    // Current filter states
    let currentDay = 'all';
    let currentTopic = 'all';
    
    // Map topics to CSS classes
    const topicClassMap = {components['js_topic_mapping']};
    
    function applyFilters() {{
        // Reset all rows and sessions visibility
        paperRows.forEach(row => {{
            row.classList.remove('hidden', 'day-hidden');
            row.classList.remove('topic-highlight');
            // Remove all possible topic classes
            Object.values(topicClassMap).forEach(cssClass => {{
                row.classList.remove(cssClass);
            }});
        }});
        
        sessions.forEach(session => {{
            session.style.display = 'block';
        }});
        
        // Apply day filter
        if (currentDay !== 'all') {{
            paperRows.forEach(row => {{
                const paperDate = row.getAttribute('data-paper-date');
                if (paperDate !== currentDay) {{
                    row.classList.add('day-hidden');
                }}
            }});
            
            sessions.forEach(session => {{
                const sessionDate = session.getAttribute('data-session-date');
                if (sessionDate !== currentDay) {{
                    session.style.display = 'none';
                }}
            }});
        }}
        
        // Apply topic filter
        if (currentTopic !== 'all') {{
            const topicClass = topicClassMap[currentTopic];
            
            paperRows.forEach(row => {{
                if (row.classList.contains('day-hidden')) return; // Skip day-hidden papers
                
                const paperTopics = row.getAttribute('data-topics');
                if (paperTopics && paperTopics.split(';').some(topic => topic.trim() === currentTopic)) {{
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
                if (session.style.display === 'none') return; // Skip day-hidden sessions
                
                const visiblePapers = session.querySelectorAll('.paper-row:not(.hidden):not(.day-hidden)');
                if (visiblePapers.length === 0) {{
                    session.style.display = 'none';
                }}
            }});
        }}
    }}
    
    // Day filter event listeners
    dayFilterTags.forEach(tag => {{
        tag.addEventListener('click', function() {{
            const selectedDay = this.getAttribute('data-day');
            
            // Update active day filter
            dayFilterTags.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            currentDay = selectedDay;
            applyFilters();
        }});
    }});
    
    // Topic filter event listeners
    filterTags.forEach(tag => {{
        tag.addEventListener('click', function() {{
            const selectedTopic = this.getAttribute('data-topic');
            
            // Update active topic filter
            filterTags.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            currentTopic = selectedTopic;
            applyFilters();
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
    print(f"Days: {', '.join([d[1] for d in components['stats']['days_list']])}")
    
    return output_qmd

# Usage
if __name__ == "__main__":
    # Replace with your actual Excel file path
    excel_file = "cf25dat.xlsx"  # Update this path
    qmd_file = generate_conference_qmd(excel_file)
    print(f"\nTo render: quarto render {qmd_file}")