#!/usr/bin/env python3
"""Build a credential-free submission ZIP using an explicit package allowlist."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import sys
root = Path(__file__).resolve().parents[1]
target = Path(sys.argv[1] if len(sys.argv) > 1 else root / 'dist/termsquad-plugin.zip')
target.parent.mkdir(parents=True, exist_ok=True)
paths = ['plugin.json', 'mcp.json', '.mcp.json', '.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json', 'skills/termsquad-remote/SKILL.md', 'assets/termsquad-logo.png', 'README.md', 'LICENSE']
with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
    for name in paths:
        data = (root / name).read_bytes()
        if name.endswith(('.json', '.md')) and any(s in data for s in [b'BEGIN PRIVATE KEY', b'ghp_', b'gho_', b'github_pat_']):
            raise SystemExit('Credential pattern in ' + name)
        archive.writestr(name, data)
print(str(target))
print('sha256:' + hashlib.sha256(target.read_bytes()).hexdigest())
