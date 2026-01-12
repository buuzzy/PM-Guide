import sys
import re

def fix_image_path(match):
    alt_text = match.group(1)
    original_path = match.group(2)
    
    # print(f"DEBUG: Found match! Alt: {alt_text}, Path: {original_path}")
    
    # 1. Normalize slashes
    path = original_path.replace('\\', '/')
    
    # 2. Add /static if missing
    if path.startswith('/img/'):
         path = '/static' + path
    elif path.startswith('img/'):
         path = '/static/' + path
    
    return f'![{alt_text}]({path})'

file_path = sys.argv[1]

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The simplest regex known to mankind.
    # Non-greedy match for content inside brackets and parens.
    new_content = re.sub(r'!\\[(.*?)\\]\((.*?)\\\)', fix_image_path, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed: {file_path}")
    else:
        print(f"No changes for: {file_path}")

except Exception as e:
    print(f"Error: {e}")
