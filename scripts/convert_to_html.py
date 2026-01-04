"""
Professional Markdown to HTML Converter
Converts TECHNICAL_ANALYSIS.md to beautifully formatted HTML with print-ready CSS
"""

import re
import html

def markdown_to_html(markdown_text):
    """Convert markdown to HTML with proper formatting"""
    
    # Escape HTML characters first
    lines = markdown_text.split('\n')
    html_lines = []
    in_code_block = False
    code_block_content = []
    
    for line in lines:
        # Handle code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                code_html = html.escape('\n'.join(code_block_content))
                html_lines.append(f'<pre><code>{code_html}</code></pre>')
                code_block_content = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            continue
        
        if in_code_block:
            code_block_content.append(line)
            continue
        
        # Process regular lines
        processed_line = line
        
        # Headers
        if processed_line.startswith('#### '):
            processed_line = f'<h4>{processed_line[5:]}</h4>'
        elif processed_line.startswith('### '):
            processed_line = f'<h3>{processed_line[4:]}</h3>'
        elif processed_line.startswith('## '):
            processed_line = f'<h2>{processed_line[3:]}</h2>'
        elif processed_line.startswith('# '):
            processed_line = f'<h1>{processed_line[2:]}</h1>'
        elif processed_line.strip() == '---':
            processed_line = '<hr>'
        elif processed_line.strip() == '':
            processed_line = '<br>'
        else:
            # Bold
            processed_line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', processed_line)
            # Italic  
            processed_line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', processed_line)
            # Inline code
            processed_line = re.sub(r'`([^`]+)`', r'<code>\1</code>', processed_line)
            # Wrap in paragraph if not empty and not already a tag
            if processed_line.strip() and not processed_line.strip().startswith('<'):
                processed_line = f'<p>{processed_line}</p>'
        
        html_lines.append(processed_line)
    
    return '\n'.join(html_lines)

# Read markdown file
with open('TECHNICAL_ANALYSIS.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Convert to HTML
html_body = markdown_to_html(markdown_content)

# HTML template
html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitoring Stack - Technical Analysis</title>
    <style>
        {open('enhanced_styles.css', 'r').read() if __import__('os').path.exists('enhanced_styles.css') else """
        /* Professional Technical Documentation Styles */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 11pt;
            line-height: 1.8;
            color: #2c3e50;
            max-width: 1000px;
            margin: 0 auto;
            padding: 60px 80px;
            background: #ffffff;
        }}
        
        h1 {{
            font-size: 2.5em;
            color: #2c3e50;
            border-bottom: 4px solid #3498db;
            padding-bottom: 0.3em;
            margin: 2em 0 1em 0;
            page-break-after: avoid;
        }}
        
        h1:first-of-type {{
            margin-top: 0;
        }}
        
        h2 {{
            font-size: 1.8em;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.25em;
            margin: 2.5em 0 1em 0;
            page-break-after: avoid;
        }}
        
        h3 {{
            font-size: 1.4em;
            color: #34495e;
            margin: 2em 0 0.8em 0;
        }}
        
        h4 {{
            font-size: 1.15em;
            color: #7f8c8d;
            margin: 1.5em 0 0.6em 0;
        }}
        
        p {{
            margin-bottom: 1.2em;
            text-align: justify;
            orphans: 3;
            widows: 3;
        }}
        
        strong {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        em {{
            font-style: italic;
            color: #7f8c8d;
        }}
        
        code {{
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            background: #f8f9fa;
            border: 1px solid #e1e4e8;
            border-radius: 3px;
            padding: 0.15em 0.4em;
            color: #d73a49;
        }}
        
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            border-radius: 6px;
            padding: 1.5em;
            margin: 1.5em 0;
            overflow-x: auto;
            page-break-inside: avoid;
        }}
        
        pre code {{
            background: transparent;
            border: none;
            color: #ecf0f1;
            padding: 0;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #bdc3c7;
            margin: 3em 0;
        }}
        
        br {{
            content: "";
            display: block;
            margin: 0.5em 0;
        }}
        
        @media print {{
            body {{
                padding: 40px;
                font-size: 10pt;
                max-width: 100%;
            }}
            
            h1, h2, h3, h4 {{
                page-break-after: avoid;
            }}
            
            pre, code {{
                page-break-inside: avoid;
            }}
        }}
        
        @page {{
            margin: 1in;
        }}
        """}
    </style>
</head>
<body>
    <div style="text-align: center; margin-bottom: 3em; padding-bottom: 2em; border-bottom: 3px double #bdc3c7;">
        <h1 style="font-size: 3em; margin-bottom: 0.3em; border: none;">Production Monitoring Stack</h1>
        <p style="font-size: 1.5em; color: #7f8c8d; margin-bottom: 1em;">Complete Technical Analysis & Expert Guide</p>
        <p style="font-size: 0.9em; color: #7f8c8d;">
            <strong>Version:</strong> 1.0 | 
            <strong>Date:</strong> January 2026 | 
            <strong>Status:</strong> Production Ready
        </p>
    </div>
    
    {html_body}
</body>
</html>'''

# Write HTML file
with open('TECHNICAL_ANALYSIS_PRO.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✓ Professional HTML version created: TECHNICAL_ANALYSIS_PRO.html")
print("  Size:", len(html_template) // 1024, "KB")
print("\\nOpen in browser and press Ctrl+P to create PDF!")
