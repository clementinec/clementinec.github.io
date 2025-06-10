import pandas as pd
import numpy as np
from collections import defaultdict
import re

class ConferenceHTMLGenerator:
    def __init__(self, df):
        """
        Initialize with a DataFrame containing columns: ID, Title, Authors, Final Topic, assigned_cluster, Decisions
        """
        self.df = df.copy()
        
        # Clean up the data
        self.df = self.df.dropna(subset=['Final Topic'])  # Remove NaN topics
        self.df = self.df[self.df['Final Topic'] != 'NaN']  # Remove string 'NaN'
        
        # Parse multiple topics if they exist (assume semicolon separated)
        self.df['topic_list'] = self.df['Final Topic'].apply(self._parse_topics)
        
        # Get all unique topics
        all_topics = []
        for topics in self.df['topic_list']:
            all_topics.extend(topics)
        self.topics = sorted(list(set(all_topics)))
        
        # Generate colors for topics
        self.topic_colors = self._generate_topic_colors()
        
        # NEW: Get unique clusters for session generation
        self.clusters = sorted(self.df['assigned_cluster'].dropna().unique().tolist())
        
        # NEW: Generate gray colors for clusters (simplified)
        self.cluster_colors = self._generate_cluster_gray_colors()
        
    def _parse_topics(self, topic_str):
        """Parse topic string, handling multiple topics separated by semicolons"""
        if pd.isna(topic_str) or topic_str == 'NaN':
            return []
        topics = [topic.strip() for topic in str(topic_str).split(';')]
        return [t for t in topics if t]  # Remove empty strings
    
    def _generate_topic_colors(self):
        colors = [
            # Warm earth tones
            '#8B4513',  # saddle brown
            '#A0522D',  # sienna
            '#CD853F',  # peru
            '#D2691E',  # chocolate
            '#BC8F8F',  # rosy brown
            
            # Cool grays and blues
            '#708090',  # slate gray
            '#4682B4',  # steel blue
            '#5F9EA0',  # cadet blue
            '#6B8E23',  # olive drab
            '#556B2F',  # dark olive green
            
            # Muted jewel tones
            '#483D8B',  # dark slate blue
            '#663399',  # rebecca purple
            '#8B4789',  # medium orchid
            '#B22222',  # firebrick
            '#CD5C5C',  # indian red
            
            # Sophisticated neutrals
            '#696969',  # dim gray
            '#808080',  # gray
            '#A9A9A9',  # dark gray
            '#2F4F4F',  # dark slate gray
            '#36454F',  # charcoal
            
            # Deep accent colors
            '#800020',  # burgundy
            '#4B0082',  # indigo
            '#191970',  # midnight blue
            '#228B22',  # forest green
            '#8B0000',  # dark red
            
            # Additional muted tones
            '#9370DB',  # medium purple
            '#3CB371',  # medium sea green
            '#FF6347',  # tomato
            '#4169E1',  # royal blue
            '#32CD32',  # lime green
        ]
        
        topic_colors = {}
        for i, topic in enumerate(self.topics):
            topic_colors[topic] = colors[i % len(colors)]
        
        return topic_colors
    
    def _generate_cluster_gray_colors(self):
        """Generate different shades of gray for clusters - ensuring uniqueness"""
        # More distinct gray shades - wider range to ensure visual distinction
        gray_shades = [
            '#404040',  # very dark gray
            '#4A4A4A',  # dark gray  
            '#545454',  # dark-medium gray
            '#5E5E5E',  # medium-dark gray
            '#686868',  # medium gray
            '#727272',  # medium-light gray
            '#7C7C7C',  # light-medium gray
            '#464646',  # another dark
            '#505050',  # dark variant
            '#5A5A5A',  # medium-dark variant
            '#646464',  # medium variant
            '#6E6E6E',  # medium-light variant
            '#787878',  # lighter variant
            '#424242',  # very dark variant
            '#4C4C4C',  # dark-ish variant
        ]
        
        cluster_colors = {}
        for i, cluster in enumerate(self.clusters):
            cluster_colors[cluster] = gray_shades[i % len(gray_shades)]
        
        return cluster_colors
    
    def _get_css_class_name(self, topic):
        """Convert topic name to CSS class name"""
        # Remove special characters and convert to lowercase
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
        return clean_name.lower().replace(' ', '-')
    
    def _group_papers_by_session(self):
        """
        MODIFIED: Group papers by session using assigned_cluster and handling poster sessions
        """
        sessions = defaultdict(lambda: {'info': {}, 'papers': []})
        
        # First, separate poster papers (Decisions == 'Companion')
        poster_papers = self.df[self.df['Decisions'] == 'Companion']
        regular_papers = self.df[self.df['Decisions'] != 'Companion']
        
        # Create poster session if there are poster papers
        if not poster_papers.empty:
            sessions['Poster']['info'] = {
                'title': 'Poster Session',
                'topics': 'Various Topics',
                'time': 'Poster Session',
                'chair': 'TBD'
            }
            
            for _, paper in poster_papers.iterrows():
                sessions['Poster']['papers'].append({
                    'id': paper['ID'],
                    'title': paper['Title'],
                    'authors': paper['Authors'],
                    'topics': paper['topic_list'] if paper['topic_list'] else [],
                    'topics_str': paper['Final Topic'],
                    'cluster': paper.get('assigned_cluster', 'N/A'),
                    'decision': paper['Decisions'],
                    'abstract': paper['Abstract']
                })
        
        # Group regular papers by assigned_cluster
        cluster_session_counter = defaultdict(int)
        
        for _, paper in regular_papers.iterrows():
            if pd.isna(paper.get('assigned_cluster')):
                continue
                
            cluster_name = paper['assigned_cluster']
            
            # Create session identifier based on cluster
            # If multiple papers per cluster, they go in the same session
            session_id = f"Session_{cluster_name}"
            
            # Initialize session info if not exists
            if session_id not in sessions:
                # Count how many papers are in this cluster to determine session numbering
                cluster_paper_count = len(regular_papers[regular_papers['assigned_cluster'] == cluster_name])
                
                sessions[session_id]['info'] = {
                    'title': f"{cluster_name}",
                    'topics': cluster_name,
                    'time': 'Conference Session',
                    'chair': 'TBD',
                    'paper_count': cluster_paper_count
                }
            
            sessions[session_id]['papers'].append({
                'id': paper['ID'],
                'title': paper['Title'],
                'authors': paper['Authors'],
                'topics': paper['topic_list'] if paper['topic_list'] else [],
                'topics_str': paper['Final Topic'],
                'cluster': paper['assigned_cluster'],
                'decision': paper['Decisions'],
                'abstract': paper['Abstract']
            })
        
        return dict(sessions)
    
    def generate_filter_buttons_html(self):
        """Generate HTML for filter buttons - only clusters now"""
        html = '    <div class="filters">\n'
        html += '        <div class="filter-tag all active" data-topic="all">ALL</div>\n'
        
        # Only add cluster-based filters
        for cluster in self.clusters:
            css_class = self._get_css_class_name(cluster)
            color = self.cluster_colors.get(cluster, '#6c757d')
            html += f'        <div class="filter-tag {css_class}" data-topic="{cluster}" style="background-color: {color}; color: white;">{cluster}</div>\n'
        
        html += '    </div>\n'
        return html
    
    def generate_sessions_html(self):
        """Generate HTML for all sessions and papers - MODIFIED to show cluster info"""
        sessions = self._group_papers_by_session()
        html = ''
        
        # Sort sessions: Poster session last, others by cluster name
        def session_sort_key(item):
            session_id, session_data = item
            if session_id == 'Poster':
                return ('Z', 'Poster')  # Sort posters last
            else:
                return ('A', session_data['info']['title'])  # Sort regular sessions by title
        
        sorted_sessions = sorted(sessions.items(), key=session_sort_key)
        
        for session_id, session_data in sorted_sessions:
            if not session_data['papers']:  # Skip empty sessions
                continue
                
            session_info = session_data['info']
            papers = session_data['papers']
            
            # Add paper count to session header for regular sessions
            paper_count_info = f" ({len(papers)} papers)" if session_id != 'Poster' else f" ({len(papers)} posters)"
            
            html += f'''    <div class="session">
        <div class="session-header">
            <div class="session-title">{session_info['title']}{paper_count_info}</div>
            <div class="session-info">{session_info['time']} // Session Chair: {session_info['chair']}</div>
        </div>
        
        <div class="papers-container">\n'''
            
            for paper in papers:
                # Create topic badges for papers with multiple topics
                topic_badges = ''
                if len(paper['topics']) > 1:
                    secondary_topics = paper['topics'][1:]
                    for topic in secondary_topics:
                        color = self.topic_colors.get(topic, '#6c757d')
                        topic_badges += f'<span class="topic-badge" style="background-color: {color};">{topic}</span>'
                
                # Add cluster badge for regular papers
                cluster_badge = ''
                if paper.get('cluster') and paper['cluster'] != 'N/A' and session_id != 'Poster':
                    cluster_color = self.cluster_colors.get(paper['cluster'], '#6c757d')
                    cluster_badge = f'<span class="cluster-badge" style="background-color: {cluster_color}; color: white; margin-left: 5px;">Cluster: {paper["cluster"]}</span>'
                
                # Add decision type badge for poster papers
                decision_badge = ''
                if paper.get('decision') == 'Companion':
                    decision_badge = '<span class="decision-badge" style="background-color: #D3D3D3; color: #333333; margin-left: 5px;">Poster</span>'
                
                # Escape quotes in abstract for HTML attributes
                abstract_text = paper.get('abstract', 'No abstract available').replace('"', '&quot;').replace("'", "&#39;")
                
                html += f'''            <div class="paper-row" data-topics="{paper['topics_str']}" data-cluster="{paper.get('cluster', '')}" data-decision="{paper.get('decision', '')}" data-abstract="{abstract_text}" onmouseenter="showTooltip(this)" onmouseleave="hideTooltip()">
                <div class="paper-id">{paper['id']}</div>
                <div class="paper-content">
                    <div class="paper-title">{paper['title']}</div>
                    <div class="paper-meta">
                        <div class="author-tag">{paper['authors']}</div>'''
                
                if topic_badges or cluster_badge or decision_badge:
                    html += f'''
                        <div class="additional-topics">{topic_badges}{cluster_badge}{decision_badge}</div>'''
                
                html += '''
                    </div>
                </div>
            </div>\n'''
            
            html += '''        </div>
    </div>\n\n'''
        
        return html
    
    def generate_css_for_topics(self):
        """Generate CSS rules for topic-specific highlighting - now includes clusters"""
        css = ''
        
        # Original topic CSS
        for topic in self.topics:
            css_class = self._get_css_class_name(topic)
            color = self.topic_colors[topic]
            
            # Convert hex to rgba for subtle background
            hex_color = color.lstrip('#')
            if len(hex_color) == 6:
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                rgba_bg = f"rgba({r}, {g}, {b}, 0.05)"
                
                css += f'''
.paper-row.topic-highlight.{css_class} {{
    border-left: 4px solid {color};
    background-color: {rgba_bg};
}}'''
        
        # Add cluster CSS
        for cluster in self.clusters:
            css_class = self._get_css_class_name(cluster)
            color = self.cluster_colors.get(cluster, '#6c757d')
            
            # Convert hex to rgba for subtle background
            hex_color = color.lstrip('#')
            if len(hex_color) == 6:
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                rgba_bg = f"rgba({r}, {g}, {b}, 0.05)"
                
                css += f'''
.paper-row.cluster-highlight.{css_class} {{
    border-left: 4px solid {color};
    background-color: {rgba_bg};
}}'''
        
        # Add CSS for badges and hover effects
        css += '''
.cluster-badge, .decision-badge {
    font-size: 0.8em;
    padding: 2px 6px;
    border-radius: 3px;
    margin-left: 5px;
}

/* Cluster filter buttons hover effect - turn red like Chinese seals */
.filter-tag[data-topic]:hover {
    background-color: #B22222 !important; /* Chinese seal red */
    transform: translateY(-1px);
    transition: all 0.2s ease;
}

/* Cluster badges hover effect */
.cluster-badge:hover {
    background-color: #B22222 !important;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

/* Paper row hover for cluster highlighting */
.paper-row:hover .cluster-badge {
    background-color: #B22222 !important;
}

/* Custom tooltip styling for abstracts */
.paper-row {
    position: relative;
}

.session, .papers-container {
    overflow: visible !important;  /* Add this to parent containers */
}
'''
        
        return css
    
    def generate_javascript_topic_mapping(self):
        """Generate JavaScript object mapping topics and clusters to CSS classes"""
        mapping = {}
        
        # Add topics
        for topic in self.topics:
            css_class = self._get_css_class_name(topic)
            mapping[topic] = css_class
        
        # Add clusters
        for cluster in self.clusters:
            css_class = self._get_css_class_name(cluster)
            mapping[cluster] = css_class
        
        # Convert to JavaScript object string
        js_map = "{\n"
        for item, css_class in mapping.items():
            js_map += f"        '{item}': '{css_class}',\n"
        js_map = js_map.rstrip(',\n') + "\n    }"
        
        return js_map
    
    def generate_complete_html_components(self):
        """Generate all HTML components needed for the QMD file"""
        sessions = self._group_papers_by_session()
        session_count = len([s for s in sessions.values() if s['papers']])
        
        # Count poster papers separately
        poster_count = len(self.df[self.df['Decisions'] == 'Companion'])
        regular_count = len(self.df[self.df['Decisions'] != 'Companion'])
        
        components = {
            'filter_buttons': self.generate_filter_buttons_html(),
            'sessions': self.generate_sessions_html(),
            'topic_css': self.generate_css_for_topics(),
            'js_topic_mapping': self.generate_javascript_topic_mapping(),
            'stats': {
                'total_papers': len(self.df),
                'regular_papers': regular_count,
                'poster_papers': poster_count,
                'total_topics': len(self.topics),
                'total_clusters': len(self.clusters),
                'total_sessions': session_count,
                'topics_list': self.topics,
                'clusters_list': self.clusters
            }
        }
        
        return components
    
    def save_html_components(self, output_file='conference_components.py'):
        """Save HTML components as Python variables for easy import"""
        components = self.generate_complete_html_components()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('# Generated HTML components for conference papers\n\n')
            
            f.write('FILTER_BUTTONS_HTML = """\n')
            f.write(components['filter_buttons'])
            f.write('"""\n\n')
            
            f.write('SESSIONS_HTML = """\n')
            f.write(components['sessions'])
            f.write('"""\n\n')
            
            f.write('TOPIC_CSS = """\n')
            f.write(components['topic_css'])
            f.write('"""\n\n')
            
            f.write('JS_TOPIC_MAPPING = """\n')
            f.write(components['js_topic_mapping'])
            f.write('"""\n\n')
            
            f.write(f'STATS = {components["stats"]}\n')
        
        print(f"HTML components saved to {output_file}")
        print(f"Total papers: {components['stats']['total_papers']}")
        print(f"Regular papers: {components['stats']['regular_papers']}")
        print(f"Poster papers: {components['stats']['poster_papers']}")
        print(f"Total clusters: {components['stats']['total_clusters']}")
        print(f"Clusters: {', '.join(components['stats']['clusters_list'])}")


# Usage example with the new columns:
def process_conference_data(excel_file_path, output_file='conference_components.py'):
    """
    Main function to process conference data and generate HTML components
    Expected columns: ID, Title, Authors, Final Topic, assigned_cluster, Decisions
    """
    # Read the data
    df = pd.read_excel(excel_file_path)
    
    # Verify required columns exist
    required_columns = ['ID', 'Title', 'Authors', 'Final Topic', 'assigned_cluster', 'Decisions']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"Warning: Missing columns: {missing_columns}")
        print(f"Available columns: {list(df.columns)}")
    
    # Generate HTML components
    generator = ConferenceHTMLGenerator(df)
    generator.save_html_components(output_file)
    
    return generator