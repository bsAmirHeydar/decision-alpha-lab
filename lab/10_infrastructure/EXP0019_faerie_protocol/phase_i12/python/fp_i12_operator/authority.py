from pathlib import Path
from .constants import FORBIDDEN_AUTHORITIES

def scan_text(text):return tuple(x for x in FORBIDDEN_AUTHORITIES if x.lower() in text.lower())
def scan_tree(root):
 bad=[]
 for p in Path(root).rglob('*'):
  if p.is_file() and p.suffix.lower() in ('.py','.mqh','.mq5'):
   found=scan_text(p.read_text(encoding='utf-8',errors='ignore'))
   if found:bad.append((str(p),found))
 return tuple(bad)
