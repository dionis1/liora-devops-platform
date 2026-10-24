#!/usr/bin/env python3
"""Read-only integrity/coverage checks for the graduation evidence pack."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'docs/screenshots'
x=json.loads((S/'manifest.json').read_text())
expected=[
'Dockerize Your Application',
'Deploy the Application in Multiple Environments (Dev & Prod)',
'Run Tests on the Application',
'Container Orchestration with Kubernetes',
'Automate Deployment (CI/CD Pipeline)',
'Create IaC (Infrastructure as Code) Templates',
'Monitor the Application',
'Think About Security (DevSecOps)',
'Think About Disaster Recovery',
'Documentation']
assert [r['title'] for r in x['requirements']]==expected
assert [r['number'] for r in x['requirements']]==list(range(1,11))
seen=set();counts={i:0 for i in range(1,11)};kinds={}
for a in x['screenshots']:
 assert a['id'] not in seen;seen.add(a['id']);p=S/a['file'];b=p.read_bytes()
 assert b.startswith(b'\xff\xd8\xff'),p
 assert hashlib.sha256(b).hexdigest()==a['sha256'],p
 counts[a['requirement']]+=1;kinds[a['kind']]=kinds.get(a['kind'],0)+1
 assert a['result'] in x['status_legend'],(a['id'],a['result'])
 for field in ['scope','capture_date','observed_date','environment','result','command','software']:assert a[field],(a['id'],field)
 for source in a['sources']:
  p=ROOT/source['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==source['sha256'],p
 if 'view' in a:
  p=ROOT/'docs/presentation-evidence'/a['view'];assert p.is_file()
  text=p.read_text();assert 'NOT A LIVE TERMINAL' in text or 'NOT DEPLOYMENT PROOF'in text,p
assert all(counts.values()),counts
actual={str(p.relative_to(S))for p in S.rglob('*.jpg')}
assert actual=={a['file']for a in x['screenshots']},'Unindexed or missing screenshot'
old=json.loads((ROOT/'docs/presentation-evidence/raw/original-screenshot-manifest.json').read_text())
oldhash={s['sha256']for s in old['screenshots']};newhash={s['sha256']for s in x['screenshots']}
assert oldhash<=newhash,'A reused original image changed'
preserved=ROOT/'docs/presentation-evidence/raw/screenshot-manifest-through-E51.json'
if preserved.exists():
 prior=json.loads(preserved.read_text())['screenshots']
 current={item['id']:item for item in x['screenshots']}
 for item in prior:
  assert current[item['id']]['file']==item['file'],item['id']
  assert current[item['id']]['sha256']==item['sha256'],item['id']
  for field in ['capture_date','observed_date','result','command','scope','kind']:
   assert current[item['id']][field]==item[field],(item['id'],field)
 print('PASS all',len(prior),'earlier screenshots and dated observation metadata preserved')
for file in ['docs/presentation-evidence.md','docs/requirements-validation-checklist.md','docs/final-compliance-report.md']:
 text=(ROOT/file).read_text();positions=[text.index(f'{i+1}. {title}')for i,title in enumerate(expected)];assert positions==sorted(positions),file
# Check local links in the evidence documents/indexes. External URLs and anchors
# do not need a network request, and temporary localhost demo URLs are not assets.
files=[ROOT/'README.md',ROOT/'docs/presentation-evidence.md',ROOT/'docs/final-compliance-report.md',ROOT/'docs/requirements-validation-checklist.md',*S.rglob('*.md'),ROOT/'docs/presentation-evidence/missing-evidence.md']
for f in files:
 for link in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if '://' in link or link.startswith('#') or link.startswith('mailto:'):continue
  target=link.split('#',1)[0]
  if target:assert (f.parent/target).resolve().exists(),(f,link)
index=(ROOT/'docs/presentation-evidence/index.html').read_text()
assert not re.search(r'<script|https?://',index),'Offline gallery must not depend on external assets'
for img in re.findall(r'<img[^>]+src="([^"]+)"',index):assert (ROOT/'docs/presentation-evidence'/img).resolve().is_file(),img
plan=(ROOT/'docs/presentation-evidence.md').read_text()
slots=[tuple(map(int,t))for t in re.findall(r'\| (\d+):(\d+)–(\d+):(\d+) \|',plan)]
assert len(slots)==18,len(slots)
for group in [slots[:8],slots[8:]]:
 previous=0
 for a,b,c,d in group:
  start=a*60+b;stop=c*60+d;assert start==previous and stop>start
  previous=stop
 assert previous==600
print('PASS exact official titles/order, 10/10 coverage, screenshot/source hashes, JPEG format and local links')
print('PASS all five original screenshots preserved byte-for-byte')
print('Screenshots:',len(seen),'Types:',kinds,'By requirement:',counts)
print('PASS offline gallery image dependencies; both live/fallback schedules independently total 600 seconds')
