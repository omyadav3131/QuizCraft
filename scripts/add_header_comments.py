#!/usr/bin/env python3
"""
Add header comments to project files to help future edits and improvements.
This script will insert a standardized header comment at the top of each textual
file found under the project root (excluding `venv`, `.git` and other binary folders).

It avoids double-inserting by checking for the marker string: "HEADER_COMMENT_AUTOGEN".

Run from the project root:
    python scripts/add_header_comments.py

The script edits files in-place. Review diffs with git after running.
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'venv', '.git', '__pycache__', 'migrations'}
TEXT_EXTS = {
    '.py', '.html', '.css', '.md', '.txt', '.json', '.yml', '.yaml', '.ini', '.cfg', '.rst'
}
MARKER = 'HEADER_COMMENT_AUTOGEN'

HEADER_TEMPLATES = {
    '.py': '"""\n{marker}\nFILE: {rel}\nPURPOSE: Brief description of this file and where to edit it.\n\nTIPS: Add your notes here to help future edits.\n"""\n\n',
    '.html': '<!-- {marker} -->\n<!-- FILE: {rel} -->\n<!-- PURPOSE: Brief description of this template and common edit points. -->\n\n',
    '.css': '/* {marker} */\n/* FILE: {rel} */\n/* PURPOSE: Styles for related templates/components. Edit in `app/static/css`. */\n\n',
    '.md': '<!-- {marker} -->\n<!-- FILE: {rel} -->\n<!-- PURPOSE: Documentation file. -->\n\n',
    '.txt': '<!-- {marker} -->\n<!-- FILE: {rel} -->\n<!-- PURPOSE: Text file. -->\n\n',
    '.json': '/* {marker} */\n/* FILE: {rel} */\n/* PURPOSE: JSON config - be careful editing. */\n\n',
    '.yml': '<!-- {marker} -->\n<!-- FILE: {rel} -->\n<!-- PURPOSE: YAML config. -->\n\n',
    '.yaml': '<!-- {marker} -->\n<!-- FILE: {rel} -->\n<!-- PURPOSE: YAML config. -->\n\n',
    '.ini': '; {marker}\n; FILE: {rel}\n; PURPOSE: INI config. -->\n\n',
    '.cfg': '; {marker}\n; FILE: {rel}\n; PURPOSE: Config file. -->\n\n',
    '.rst': '.. {marker}\n.. FILE: {rel}\n.. PURPOSE: ReStructuredText file.\n\n',
}

changed = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    parts = Path(dirpath).parts
    if any(p in SKIP_DIRS for p in parts):
        continue
    for fname in filenames:
        fpath = Path(dirpath) / fname
        ext = fpath.suffix.lower()
        if ext not in TEXT_EXTS:
            continue
        try:
            text = fpath.read_text(encoding='utf-8')
        except Exception:
            continue
        if MARKER in text:
            continue
        rel = fpath.relative_to(ROOT)
        header_template = HEADER_TEMPLATES.get(ext)
        if not header_template:
            # default to HTML comment style
            header = f'<!-- {MARKER} -->\n<!-- FILE: {rel} -->\n<!-- PURPOSE: File. -->\n\n'
        else:
            header = header_template.format(marker=MARKER, rel=rel)
        new_text = header + text
        try:
            fpath.write_text(new_text, encoding='utf-8')
            changed.append(str(rel))
        except Exception as e:
            print('Failed to write', fpath, e)

print('Header insertion complete. Files modified:')
for p in changed:
    print('-', p)

if not changed:
    print('No files were changed (maybe headers already present).')
