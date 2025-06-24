import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime
import re

class ConferenceHTMLGenerator:
    def __init__(self, df):
        """
        Initialize with a DataFrame containing columns: ID, Title, Authors, Final Topic, Session, Date, Time
        """
        self.df = df.copy()
        
        # Debug: Print available columns
        print(f"Available columns in DataFrame: {list(self.df.columns)}")
        if 'Date' in self.df.columns and 'Time' in self.df.columns:
            print("Date and Time columns found!")
            # Show sample of date/time values
            sample = self.df[['Date', 'Time']].head(3)
            print(f"Sample date/time values:\n{sample}")
        else:
            print("Warning: Date and/or Time columns not found")
        
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
        
        # Get unique sessions
        self.sessions = sorted(self.df['Session'].dropna().unique().tolist())
        
        # Generate colors for sessions
        self.session_colors = self._generate_session_colors()
        
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
    
    def _generate_session_colors(self):
        """Generate different shades of gray for sessions"""
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
        
        session_colors = {}
        for i, session in enumerate(self.sessions):
            session_colors[session] = gray_shades[i % len(gray_shades)]
        
        return session_colors
    
    def _get_css_class_name(self, topic):
        """Convert topic name to CSS class name"""
        # Remove special characters and convert to lowercase
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
        return clean_name.lower().replace(' ', '-')
    
    def _group_papers_by_session(self):
        """
        Group papers by session using the Session column
        """
        sessions = defaultdict(lambda: {'info': {}, 'papers': []})
        
        # Process all papers
        for _, paper in self.df.iterrows():
            if pd.isna(paper.get('Session')):
                continue
                
            session_name = paper['Session']
            
            # Initialize session info if not exists
            if session_name not in sessions:
                # Get all papers in this session
                session_papers = self.df[self.df['Session'] == session_name]
                session_paper_count = len(session_papers)
                
                # Get the most common topic for this session
                all_topics = []
                for _, p in session_papers.iterrows():
                    if not pd.isna(p['Final Topic']):
                        topics = [t.strip() for t in str(p['Final Topic']).split(';')]
                        all_topics.extend(topics)
                
                # Find most common topic
                if all_topics:
                    topic_counter = Counter(all_topics)
                    session_topic = topic_counter.most_common(1)[0][0]
                else:
                    session_topic = "Mixed Topics"
                
                # Determine session type based on session name
                if session_name.startswith('S-'):
                    session_type = 'Speaker-Driven Session'
                elif session_name.startswith('P-'):
                    session_type = 'Parallel Session'
                else:
                    session_type = 'Catalytic Interface Presentation'
                
                sessions[session_name]['info'] = {
                    'title': f"{session_name}, {session_topic}",
                    'topics': session_topic,
                    'time': session_type,
                    'paper_count': session_paper_count
                }
            
            # Format timestamp if Date and Time columns exist
            timestamp = ''
            if 'Date' in self.df.columns and 'Time' in self.df.columns:
                date_val = paper.get('Date')
                time_val = paper.get('Time')
                
                if date_val is not None and time_val is not None and not pd.isna(date_val) and not pd.isna(time_val):
                    # Convert date format from 2025/07/01 to a more readable format
                    try:
                        # Handle both string and datetime objects
                        if isinstance(date_val, str):
                            date_obj = datetime.strptime(date_val, '%Y/%m/%d')
                        else:
                            date_obj = pd.to_datetime(date_val)
                        
                        formatted_date = date_obj.strftime('%b %d')  # e.g., "Jul 01"
                        
                        # Handle time formatting
                        if isinstance(time_val, str):
                            timestamp = f"{formatted_date}, {time_val}"
                        else:
                            # If time is a datetime object, extract just the time part
                            time_str = pd.to_datetime(time_val).strftime('%H:%M')
                            timestamp = f"{formatted_date}, {time_str}"
                    except Exception as e:
                        # Fallback to raw values if parsing fails
                        timestamp = f"{date_val}, {time_val}"
            
            sessions[session_name]['papers'].append({
                'id': paper['ID'],
                'title': paper['Title'],
                'authors': paper['Authors'],
                'topics': paper['topic_list'] if paper['topic_list'] else [],
                'topics_str': paper['Final Topic'],
                'session': paper['Session'],
                'abstract': paper.get('Abstract', 'No abstract available'),
                'timestamp': timestamp
            })
        
        return dict(sessions)
    
    def generate_filter_buttons_html(self):
        """Generate HTML for filter buttons - using Final Topics as filters with gray colors"""
        html = '    <div class="filters">\n'
        html += '        <div class="filter-tag all active" data-topic="all">ALL</div>\n'
        
        # Generate gray shades for topics
        gray_shades = [
            '#404040', '#4A4A4A', '#545454', '#5E5E5E', '#686868',
            '#727272', '#7C7C7C', '#464646', '#505050', '#5A5A5A',
            '#646464', '#6E6E6E', '#787878', '#424242', '#4C4C4C'
        ]
        
        # Add topic-based filters with gray colors
        for i, topic in enumerate(self.topics):
            css_class = self._get_css_class_name(topic)
            color = gray_shades[i % len(gray_shades)]
            html += f'        <div class="filter-tag {css_class}" data-topic="{topic}" style="background-color: {color}; color: white;">{topic}</div>\n'
        
        html += '    </div>\n'
        return html
    
    def generate_sessions_html(self):
        """Generate HTML for all sessions and papers"""
        sessions = self._group_papers_by_session()
        html = ''
        
        # Sort sessions: S- first, then P-, then others
        def session_sort_key(item):
            session_id, session_data = item
            if session_id.startswith('S-'):
                return ('A', session_id)  # Sort S- sessions first
            elif session_id.startswith('P-'):
                return ('B', session_id)  # Sort P- sessions after S- sessions
            else:
                return ('C', session_id)  # Other sessions last
        
        sorted_sessions = sorted(sessions.items(), key=session_sort_key)
        
        for session_id, session_data in sorted_sessions:
            if not session_data['papers']:  # Skip empty sessions
                continue
                
            session_info = session_data['info']
            papers = session_data['papers']
            
            # Add paper count to session header
            paper_count_info = f" ({len(papers)} papers)"
            
            html += f'''    <div class="session">
        <div class="session-header">
            <div class="session-title">{session_info['title']}{paper_count_info}</div>
            <div class="session-info">{session_info['time']}</div>
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
                
                # Add session badge for all papers
                session_badge = ''
                if paper.get('session'):
                    session_color = self.session_colors.get(paper['session'], '#6c757d')
                    session_badge = f'<span class="session-badge" style="background-color: {session_color}; color: white; margin-left: 5px;">Session: {paper["session"]}</span>'
                
                # Add presentation type badge based on session code
                presentation_badge = ''
                if paper.get('session'):
                    if paper['session'].startswith('S-'):
                        presentation_badge = '<span class="presentation-badge" style="background-color: #5F9EA0; color: white; margin-left: 5px;">Speaker-led</span>'
                    elif paper['session'].startswith('P-'):
                        presentation_badge = '<span class="presentation-badge" style="background-color: #708090; color: white; margin-left: 5px;">Parallel</span>'
                
                # Add timestamp if available
                timestamp_html = ''
                if paper.get('timestamp'):
                    timestamp_html = f'<span class="paper-timestamp">{paper["timestamp"]}</span>'
                
                # Escape quotes in abstract for HTML attributes
                abstract_text = paper.get('abstract', 'No abstract available').replace('"', '&quot;').replace("'", "&#39;")
                
                html += f'''            <div class="paper-row" data-topics="{paper['topics_str']}" data-session="{paper.get('session', '')}" data-abstract="{abstract_text}" onmouseenter="showTooltip(this)" onmouseleave="hideTooltip()">
                <div class="paper-id">{paper['id']}</div>
                <div class="paper-content">
                    <div class="paper-title">{paper['title']}</div>
                    <div class="paper-meta">
                        <div class="author-tag">{paper['authors']}</div>'''
                
                if topic_badges or session_badge or presentation_badge:
                    html += f'''
                        <div class="additional-topics">{topic_badges}{session_badge}{presentation_badge}</div>'''
                
                html += '''
                    </div>
                </div>'''
                
                # Add timestamp at the end
                if timestamp_html:
                    html += f'''
                {timestamp_html}'''
                
                html += '''
            </div>\n'''
            
            html += '''        </div>
    </div>\n\n'''
        
        return html
    
    def generate_css_for_topics(self):
        """Generate CSS rules for topic-specific highlighting"""
        css = ''
        
        # Topic CSS
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
        
        # Add CSS for badges, hover effects, and timestamp
        css += '''
.session-badge, .presentation-badge {
    font-size: 0.8em;
    padding: 2px 6px;
    border-radius: 3px;
    margin-left: 5px;
}

/* Session filter buttons hover effect - turn red like Chinese seals */
.filter-tag[data-topic]:hover {
    background-color: #B22222 !important; /* Chinese seal red */
    transform: translateY(-1px);
    transition: all 0.2s ease;
}

/* Session badges hover effect */
.session-badge:hover, .presentation-badge:hover {
    background-color: #B22222 !important;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

/* Paper row hover for session highlighting */
.paper-row:hover .session-badge {
    background-color: #B22222 !important;
}

.paper-row:hover .presentation-badge {
    background-color: #8B0000 !important;
}

/* Timestamp styling */
.paper-timestamp {
    margin-left: auto;
    font-size: 0.75rem;
    color: #999;
    opacity: 0.7;
    white-space: nowrap;
    padding-left: 15px;
}

.paper-row:hover .paper-timestamp {
    color: #ccc;
}

/* Custom tooltip styling for abstracts */
.paper-row {
    position: relative;
}

.session, .papers-container {
    overflow: visible !important;
}
'''
        
        return css
    
    def generate_javascript_topic_mapping(self):
        """Generate JavaScript object mapping topics to CSS classes"""
        mapping = {}
        
        # Only add topics (not sessions) since we're filtering by topics
        for topic in self.topics:
            css_class = self._get_css_class_name(topic)
            mapping[topic] = css_class
        
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
        
        # Count papers by session type
        s_papers = len(self.df[self.df['Session'].str.startswith('S-', na=False)])
        p_papers = len(self.df[self.df['Session'].str.startswith('P-', na=False)])
        
        components = {
            'filter_buttons': self.generate_filter_buttons_html(),
            'sessions': self.generate_sessions_html(),
            'topic_css': self.generate_css_for_topics(),
            'js_topic_mapping': self.generate_javascript_topic_mapping(),
            'stats': {
                'total_papers': len(self.df),
                'speaker_led_papers': s_papers,
                'parallel_papers': p_papers,
                'total_topics': len(self.topics),
                'total_sessions': len(self.sessions),
                'session_count': session_count,
                'topics_list': self.topics,
                'sessions_list': self.sessions
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
        print(f"Speaker-led presentations: {components['stats']['speaker_led_papers']}")
        print(f"Parallel presentations: {components['stats']['parallel_papers']}")
        print(f"Total sessions: {components['stats']['total_sessions']}")
        print(f"Sessions: {', '.join(components['stats']['sessions_list'])}")


# Usage example with the new columns:
def process_conference_data(excel_file_path, output_file='conference_components.py'):
    """
    Main function to process conference data and generate HTML components
    Expected columns: ID, Title, Authors, Final Topic, Session
    Optional columns: Date, Time, Abstract
    """
    # Read the data
    df = pd.read_excel(excel_file_path)
    
    # Verify required columns exist
    required_columns = ['ID', 'Title', 'Authors', 'Final Topic', 'Session']
    optional_columns = ['Date', 'Time', 'Abstract']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"Warning: Missing required columns: {missing_columns}")
        print(f"Available columns: {list(df.columns)}")
    
    missing_optional = [col for col in optional_columns if col not in df.columns]
    if missing_optional:
        print(f"Note: Missing optional columns: {missing_optional}")
    
    # Generate HTML components
    generator = ConferenceHTMLGenerator(df)
    generator.save_html_components(output_file)
    
    return generator