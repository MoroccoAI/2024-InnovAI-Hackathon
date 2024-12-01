import re

def clean_response_for_html(response):
    # Remove markdown-style bold and italic markers
    response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
    response = re.sub(r'\*(.*?)\*', r'\1', response)
    
    # Convert lists to proper HTML lists
    def convert_lists(text):
        # Convert unordered lists
        text = re.sub(r'^-\s*(.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
        # Wrap consecutive list items in <ul>
        text = re.sub(r'(<li>.*?</li>\n)+', lambda m: f'<ul>\n{m.group(0)}</ul>\n', text, flags=re.DOTALL)
        
        # Convert numbered lists
        text = re.sub(r'^\d+\.\s*(.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
        # Wrap consecutive numbered list items in <ol>
        text = re.sub(r'(<li>.*?</li>\n)+', lambda m: f'<ol>\n{m.group(0)}</ol>\n', text, flags=re.DOTALL)
        
        return text
    
    # Apply list conversion
    response = convert_lists(response)
    
    # Add paragraph tags to plain text
    if not re.search(r'<[/]?(ul|ol|li|p)>', response):
        response = f'<p>{response}</p>'
    
    return response