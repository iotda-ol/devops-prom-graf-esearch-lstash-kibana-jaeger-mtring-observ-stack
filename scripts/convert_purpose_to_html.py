"""
Convert PURPOSE.md to beautiful HTML webpage
"""

import re
import html as html_module

def markdown_to_html(markdown_text):
    """Convert markdown to HTML with proper formatting and structure"""
    
    lines = markdown_text.split('\n')
    html_lines = []
    in_code_block = False
    code_block_content = []
    in_list = False
    skip_first_h1 = False  # Track first H1 to avoid duplicate
    
    for line in lines:
        # Handle code blocks
        if line.strip().startswith('```'):
            # Close list if open
            if in_list:
                html_lines.append('</ul>')
                in_list = False
                
            if in_code_block:
                # End code block
                code_html = html_module.escape('\n'.join(code_block_content))
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
        
        # Skip empty lines in lists
        if in_list and line.strip() == '':
            continue
            
        # Process regular lines
        processed_line = line
        
        # Headers (close list first if needed)
        if processed_line.startswith('#'):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
                
            if processed_line.startswith('#### '):
                processed_line = f'<h4>{processed_line[5:]}</h4>'
            elif processed_line.startswith('### '):
                processed_line = f'<h3>{processed_line[4:]}</h3>'
            elif processed_line.startswith('## '):
                processed_line = f'<h2>{processed_line[3:]}</h2>'
            elif processed_line.startswith('# '):
                # Skip first H1 (it's already in the header)
                if not skip_first_h1:
                    skip_first_h1 = True
                    continue
                processed_line = f'<h2>{processed_line[2:]}</h2>'  # Make it H2 instead
        elif processed_line.strip() == '---':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            processed_line = '<hr>'
        elif processed_line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            continue  # Skip empty lines
        elif processed_line.strip().startswith(('- ', '* ')):
            # List item
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
                
            item_text = processed_line.strip()[2:]
            # Process inline formatting
            item_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_text)
            item_text = re.sub(r'`([^`]+)`', r'<code>\1</code>', item_text)
            item_text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', item_text)
            processed_line = f'<li>{item_text}</li>'
        else:
            # Close list if we're starting new content
            if in_list and not processed_line.strip().startswith(('- ', '* ')):
                html_lines.append('</ul>')
                in_list = False
            
            # Skip if line starts with a tag already
            if processed_line.strip().startswith('<'):
                html_lines.append(processed_line)
                continue
                
            # Apply inline formatting
            processed_line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', processed_line)
            processed_line = re.sub(r'`([^`]+)`', r'<code>\1</code>', processed_line)
            processed_line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', processed_line)
            
            # Wrap in paragraph if not empty
            if processed_line.strip():
                processed_line = f'<p>{processed_line}</p>'
            else:
                continue
        
        html_lines.append(processed_line)
    
    # Close any remaining lists
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)

# Read markdown file
with open('PURPOSE.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Convert to HTML
html_body = markdown_to_html(markdown_content)

# HTML template with professional styling
html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitoring Stack - Purpose & Real-World Usage</title>
    <style>
        /* Professional Documentation Styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Helvetica Neue', sans-serif;
            font-size: 11pt;
            line-height: 1.7;
            color: #2c3e50;
            background: #f8f9fa;
            padding: 0;
            margin: 0;
        }}
        
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 80px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 3.5em;
            font-weight: 700;
            margin-bottom: 0.3em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.4em;
            opacity: 0.95;
            margin: 0;
        }}
        
        .content {{
            padding: 60px 80px;
        }}
        
        h1 {{
            font-size: 2.5em;
            color: #2c3e50;
            border-bottom: 4px solid #667eea;
            padding-bottom: 0.3em;
            margin: 2em 0 1em 0;
            page-break-after: avoid;
        }}
        
        h2 {{
            font-size: 2em;
            color: #2c3e50;
            margin: 2.5em 0 1em 0;
            padding-bottom: 0.3em;
            border-bottom: 2px solid #667eea;
            page-break-after: avoid;
        }}
        
        h3 {{
            font-size: 1.5em;
            color: #34495e;
            margin: 2em 0 0.8em 0;
            font-weight: 600;
        }}
        
        h4 {{
            font-size: 1.2em;
            color: #7f8c8d;
            margin: 1.5em 0 0.6em 0;
            font-weight: 600;
        }}
        
        p {{
            margin-bottom: 1.3em;
            text-align: justify;
            line-height: 1.8;
        }}
        
        strong {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        em {{
            font-style: italic;
            color: #546e7a;
        }}
        
        code {{
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            background: #f0f4f8;
            border: 1px solid #d1dce5;
            border-radius: 4px;
            padding: 0.2em 0.5em;
            color: #c7254e;
        }}
        
        pre {{
            background: #263238;
            color: #aed581;
            border-radius: 8px;
            padding: 1.5em;
            margin: 1.5em 0;
            overflow-x: auto;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            page-break-inside: avoid;
        }}
        
        pre code {{
            background: transparent;
            border: none;
            color: #aed581;
            padding: 0;
            font-size: 0.95em;
        }}
        
        ul, ol {{
            margin: 1em 0 1.5em 2.5em;
            padding-left: 0;
        }}
        
        li {{
            margin-bottom: 0.7em;
            line-height: 1.7;
        }}
        
        ul li {{
            list-style-type: disc;
        }}
        
        ul li::marker {{
            color: #667eea;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #e1e8ed;
            margin: 3em 0;
        }}
        
        /* Scenario boxes */
        h3 + p {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 1.2em 1.5em;
            margin: 1em 0;
            border-radius: 4px;
        }}
        
        /* Success metrics box */
        .metrics-box {{
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            border-left: 4px solid #4caf50;
            padding: 1.5em;
            margin: 2em 0;
            border-radius: 8px;
         }}
        
        /* Links */
        a {{
            color: #667eea;
            text-decoration: none;
            border-bottom: 1px dotted #667eea;
            transition: all 0.3s ease;
        }}
        
        a:hover {{
            color: #764ba2;
            border-bottom-color: #764ba2;
        }}
        
        /* Table of Contents */
        .toc {{
            background: #f8f9fa;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            padding: 2em;
            margin: 2em 0 3em 0;
        }}
        
        .toc h2 {{
            margin-top: 0;
            border-bottom: none;
            color: #667eea;
        }}
        
        /* Print styles */
        @media print {{
            body {{
                background: white;
                font-size: 10pt;
            }}
            
            .container {{
                box-shadow: none;
                max-width: 100%;
            }}
            
            .header {{
                background: #667eea;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            
            .content {{
                padding: 40px;
            }}
            
            h1, h2, h3, h4 {{
                page-break-after: avoid;
            }}
            
            pre, code {{
                page-break-inside: avoid;
            }}
        }}
        
        @page {{
            margin: 0.75in;
        }}
        
        /* Responsive */
        @media screen and (max-width: 768px) {{
            .header, .content {{
                padding: 30px 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            body {{
                font-size: 10pt;
            }}
        }}
        
        /* Footer */
        .footer {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 40px 80px;
            text-align: center;
            margin-top: 60px;
        }}
        
        .footer p {{
            margin: 0.5em 0;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Monitoring Stack</h1>
            <p>Purpose & Real-World Usage Guide</p>
        </div>
        
        <div class="content">
            {html_body}
        </div>
        
        <div class="footer">
            <p><strong>Monitoring Stack Documentation</strong></p>
            <p>Version 1.0 | January 2026 | Production Ready</p>
            <p style="margin-top: 1em; font-size: 0.9em; opacity: 0.8;">
                Press Ctrl+P to save as PDF
            </p>
        </div>
    </div>
</body>
</html>'''

# Write HTML file
with open('PURPOSE.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✓ HTML webpage created: PURPOSE.html")
print(f"  Size: {len(html_template) // 1024} KB")
print("\n📄 File created successfully!")
print("Opening in browser...")
