#!/usr/bin/env python3
"""Render honest, source-linked evidence pages; does not run tests or fake terminal UIs.

Capture these pages with the browser tool. Archived-output views are explicitly
labeled, separate from real application/GitHub/monitoring screenshots.
"""
from pathlib import Path
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/presentation-evidence'
SHOTS = ROOT / 'docs/screenshots'
REQUIREMENTS = json.loads((OUT / 'requirements.json').read_text())
DATE = '2026-10-23'
ANSI = re.compile(r'\x1b\[[0-9;]*m')
CATALOG = []


def read(path):
    return ANSI.sub('', (ROOT / path).read_text()).replace('\ufeff', '')


def lines(path, start=0, stop=None):
    return '\n'.join(read(path).splitlines()[start:stop])


def block(path, anchor, count=18):
    a = read(path).splitlines()
    start = next(i for i, value in enumerate(a) if anchor in value)
    return '\n'.join(a[start:start + count])


def add(key, req, title, source, command, result='PASSED', observed=DATE,
        environment='Local', version='', scope='', content=None, kind='archived-output', file=None,
        also=None, url=None):
    paths = source if isinstance(source, list) else [source]
    item = dict(id=key, requirement=req, supports=also or [req], title=title,
                file=file or REQUIREMENTS[req-1]['directory'] + '/' + key + '.jpg',
                capture_date=DATE, observed_date=observed, environment=environment,
                software=version, result=result, scope=scope, command=command,
                kind=kind, workflow_url=url,
                sources=[dict(path=p, sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in paths])
    if content is not None:
        item['view'] = 'views/' + key + '.html'
        item['_content'] = content
    CATALOG.append(item)
    return item


# Reused, unedited UI captures; original bytes and dates are retained.
add('E01',1,'FastAPI Swagger documentation','docs/remediation-report.md','Open http://127.0.0.1:18000/docs',kind='actual-ui',file=REQUIREMENTS[0]['directory']+'/fastapi-swagger.jpg',version='Python 3.12 / FastAPI 0.161.0',scope='Original patched upstream app; screenshot fixture had no database.')
add('E02',1,'Original React login page','docs/remediation-report.md','Open http://127.0.0.1:18081/login',kind='actual-ui',file=REQUIREMENTS[0]['directory']+'/react-login.jpg',version='React 18 / Vite 6.4.4',scope='Login form rendering only. Authenticated functionality is proved separately by E06–E07.')
add('E03',7,'All three Prometheus targets UP','docs/remediation-evidence/monitoring-targets.json','Open http://127.0.0.1:18084/targets',kind='actual-ui',file=REQUIREMENTS[6]['directory']+'/prometheus-targets-up.jpg',version='Prometheus 3.15.0 / Grafana 13.2.4',scope='Isolated Docker targets; not proof of ServiceMonitor discovery in Kubernetes.')
add('E04',7,'Real request counts, error counts and latency','monitoring/dashboards/fastapi.json','Open http://127.0.0.1:18083/d/liora-fastapi',kind='actual-ui',file=REQUIREMENTS[6]['directory']+'/grafana-request-latency-errors.jpg',version='Grafana 13.2.4',scope='Synthetic local health requests and deliberate 404s; no production traffic.')
add('E05',7,'Unavailable alert FIRING after one minute','docs/remediation-evidence/alert-firing.json','Open http://127.0.0.1:18084/alerts',kind='actual-ui',file=REQUIREMENTS[6]['directory']+'/application-alert-firing.jpg',version='Prometheus 3.15.0',scope='Disposable backend deliberately stopped. Receiver notification delivery not tested.')
add('E06',1,'Authenticated application dashboard','docs/presentation-evidence/raw/application-live-health.txt','Sign in to isolated http://127.0.0.1:18081 with temporary local credentials',kind='actual-ui',file=REQUIREMENTS[0]['directory']+'/authenticated-dashboard.jpg',also=[1,3],version='Patched upstream app at platform 211199d / PostgreSQL 16.10',scope='Actual browser login against an isolated database; no password appears in the screenshot.')
add('E07',1,'Browser-created item persists after reload','docs/presentation-evidence/raw/postgres16-browser-record-restore.txt','Items → Add Item → Save → reload',kind='actual-ui',file=REQUIREMENTS[0]['directory']+'/item-created-and-persisted.jpg',also=[1,3,9],version='React / FastAPI / PostgreSQL 16.10',scope='Synthetic item persisted through the API and database; same ID/title restored in E34.')
add('E08',1,'Executed Swagger request returns HTTP 200','docs/presentation-evidence/raw/application-live-health.txt','Swagger → health-check → Try it out → Execute',kind='actual-ui',file=REQUIREMENTS[0]['directory']+'/swagger-real-health-200.jpg',version='FastAPI 0.161.0 / Uvicorn',scope='Server response 200 and body true, not the schema example. Database readiness separately returned 200.')
add('E09',5,'Current CI blocks publication','docs/presentation-evidence/raw/github-ci-211199d.json','Open current workflow run',result='FAILED',kind='actual-ui',file=REQUIREMENTS[4]['directory']+'/github-current-security-gate.jpg',environment='GitHub Actions',version='Commit 211199d',scope='Tests/lint/platform checks passed; backend image scan failed; publication/promotion skipped. PR publication is also restricted to main push events.',url='https://github.com/dionis1/liora-devops-platform/actions/runs/39920280796')
add('E10',5,'Historical successful GHCR publication and dev promotion','docs/presentation-evidence/raw/github-historical-ci-main.json','Open historical main workflow run',observed='2026-10-22',kind='actual-ui',file=REQUIREMENTS[4]['directory']+'/github-historical-publish-promote.jpg',environment='GitHub Actions',also=[1,5],version='Commit 3ca9925; older pipeline',scope='Historical publication/promotion only; not a release of 211199d and not Argo deployment proof.',url='https://github.com/dionis1/liora-devops-platform/actions/runs/39802778100')
add('E11',6,'Current Terraform, Ansible and Kustomize workflow passes','docs/presentation-evidence/raw/github-platform-211199d.json','Open platform validation workflow',kind='actual-ui',file=REQUIREMENTS[5]['directory']+'/github-platform-validation-passed.jpg',environment='GitHub Actions',also=[2,4,6],version='Commit 211199d',scope='Static checks only; no Terraform plan/apply or k3s provisioning.',url='https://github.com/dionis1/liora-devops-platform/actions/runs/39920280791')
add('E12',8,'Current source security workflow passes','docs/presentation-evidence/raw/github-source-security-211199d.json','Open source security workflow',kind='actual-ui',file=REQUIREMENTS[7]['directory']+'/github-source-security-passed.jpg',environment='GitHub Actions',version='Trivy 0.76.1 / commit 211199d',scope='Patched dependency/configuration/secret scan; not a passing backend-image scan.',url='https://github.com/dionis1/liora-devops-platform/actions/runs/39920280780')

p='docs/remediation-evidence/backend-build.txt'
add('E13',1,'Backend image build completed',p,'docker build -f docker/backend.Dockerfile -t liora-remediation-backend:local course-app/backend',version='Python 3.12 / uv 0.13.1 / Docker 29.1.3',scope='Original build log excerpt; build success does not waive its 44 HIGH OS findings.',content=lines(p,-14))
p='docs/remediation-evidence/frontend-build.txt'
add('E14',1,'Frontend TypeScript and production bundle completed',p,'docker build -f docker/frontend.Dockerfile -t liora-remediation-frontend:local course-app/frontend',version='Node 22 / Vite 6.4.4 / Nginx 1.30',scope='Exact archived build output. Later cached functional fixture reused this application source.',content=block(p,'vite v6.4.4',14))
p='docs/presentation-evidence/raw/docker-running-health.txt'
add('E15',1,'Running containers and health checks',[p,'docs/presentation-evidence/raw/functional-fixture.compose.yml'],'docker ps; docker inspect (selected health/security fields only)',version='Docker 29.1.3 / PostgreSQL 16.10',scope='Actual isolated containers with a temporary same-origin Nginx API proxy; no Kubernetes/monitoring was running.',content=read(p))
p='docs/remediation-evidence/backend-tests.txt'
add('E16',3,'55 upstream tests passed',p,'uv run --frozen bash scripts/tests-start.sh',version='Python 3.12.3 / pytest 7.4.4 / PostgreSQL 16.10',scope='Original captured test counts and result; passlib deprecation warning remains.',content=block(p,'collected 55 items',21))
p='docs/remediation-evidence/metrics-tests.txt'
add('E17',3,'Platform metrics and readiness tests passed',p,'python -m pytest tests/test_platform_metrics.py -q',version='Python 3.12 / pytest 7.4.4',scope='Request/status/duration metrics and safe database-unavailable 503 response.',content=read(p))
p='docs/remediation-evidence/backend-lint.txt'
add('E18',3,'Mypy and Ruff passed',p,'uv run --frozen bash scripts/lint.sh',version='Mypy / Ruff 0.17.2',scope='Actual archived lint output for 39 source files.',content=read(p))
p='docs/presentation-evidence/raw/dev-prod-configuration.txt'
add('E19',2,'Dev and prod separation: static manifests',p,'kubectl kustomize kubernetes/overlays/dev; kubectl kustomize kubernetes/overlays/prod',result='PARTIALLY_VALIDATED',version='kubectl 1.35.9 / Kustomize 5.7.1',scope='Namespaces, image references, hosts and TLS settings are configuration evidence only. Production was not deployed.',content=read(p))
p='docs/local-validation-evidence/kubernetes-live.log'
add('E20',4,'Historical dev pods and Services READY',p,'kubectl -n liora-dev get pods,services,pvc -o wide',observed='2026-10-22',version='k3d 5.9.0 / default k3s 1.35.5-k3s1 / PostgreSQL 16.10',scope='Archived actual first-pass local cluster; cluster deleted. Final second-pass hardening was not deployed.',content=block(p,'NAME                            READY',13))
add('E21',4,'Historical PVC and Kubernetes HTTP access',p,'kubectl get pvc; loopback port-forward HTTP requests; Traefik routing smoke',observed='2026-10-22',version='k3d 5.9.0 / PostgreSQL 16.10 / Traefik',scope='Actual first-pass bound 8 GiB PVC and local backend/frontend/Traefik checks. Not cloud/public HTTPS.',content=block(p,'NAME                                      STATUS',11))
p='docs/local-validation-evidence/argocd-live.log'
add('E22',5,'Argo CD ran, but private repository comparison failed',p,'Argo CD health; kubectl get applications',result='FAILED',observed='2026-10-22',version='Argo CD 3.5.5 / local k3d',scope='Health is not synchronization. Historical private-repo ComparisonError. Repository became public on 2026-10-23; new public reconciliation still not tested.',content=block(p,'PASS Argo CD health',7))
p='gitops/applications.yaml'
add('E23',5,'Production manual sync configuration',p,'Review gitops/applications.yaml; no automated production policy',result='PARTIALLY_VALIDATED',kind='configuration',version='Application manifests at 211199d',scope='Design/static proof only. No successful production sync or rollback is claimed.',content=lines(p,26,None))
p='docs/presentation-evidence/raw/terraform-validation.txt'
add('E24',6,'Terraform formatting and validation passed',p,'terraform fmt -check -recursive; terraform validate',version='Terraform 1.16.6',scope='Actual fresh command output; no plan/apply or cloud recreation.',content=read(p))
p='docs/presentation-evidence/raw/ansible-validation.txt'
add('E25',6,'Three Ansible syntax checks passed',p,'ansible-playbook --syntax-check prepare.yml / k3s.yml / kubeconfig.yml',version='Ansible core 2.16.3 / Python 3.12.3',scope='Actual fresh syntax output. No remote installation or cloud host validation.',content=lines(p,12,None))
p='docs/remediation-evidence/alert-resolved.json'
add('E26',7,'Application alert cleared after recovery',p,'GET http://127.0.0.1:18084/api/v1/alerts after backend restart',version='Prometheus 3.15.0',scope='Actual API record with alerts empty after the firing scenario; notification delivery not tested.',content=read(p))
p='monitoring/application-observability.yaml'
add('E27',7,'ServiceMonitor implemented: runtime discovery pending',p,'kubectl kustomize monitoring',result='PARTIALLY_VALIDATED',kind='configuration',version='monitoring.coreos.com/v1 / chart 92.11.0',scope='Rendered configuration only. The new ServiceMonitor was not live-tested against the hardened Kubernetes workloads.',content=lines(p,0,23))
a='docs/local-validation-evidence/security-findings.json';b='docs/remediation-evidence/security-summary.json'
x=json.loads(read(a))['summaries'];y=json.loads(read(b))
rows=['Comparable scanner: Trivy 0.76.1; HIGH/CRITICAL package occurrences.','Source final first-pass scan includes development dependencies.','Scope                         BEFORE 22 Oct       AFTER 23 Oct','                              CRITICAL / HIGH     CRITICAL / HIGH']
for label,old,new in [('Application dependency locks','source-final','source'),('Backend runtime','backend-final','backend_image'),('Frontend runtime','frontend-1.28-patched','frontend_image')]:
 z=x[old];c=y[new]['counts'];rows.append(f"{label:28} {z.get('Vulnerabilities:CRITICAL',0):3} / {z.get('Vulnerabilities:HIGH',0):3}          {c.get('CRITICAL',0):3} / {c.get('HIGH',0):3}")
rows+=['','Frontend before column: intermediate Nginx 1.28 patched image.','The first-pass FINAL Nginx 1.30 frontend was already 0 / 0.','Backend: 44 unfixed HIGH OS findings remain. Release policy FAILS.','No CVE suppressions or ignore-unfixed policy exceptions were used.']
add('E28',8,'Security before and after remediation',[a,b],'Compare original Trivy findings with final remediation scan counts',result='FAILED',version='Trivy 0.76.1',scope='Counts derived from archived reports, not a new scan. Different frontend stages are labeled explicitly; no claim that all findings are fixed.',content='\n'.join(rows))
p='docs/presentation-evidence/raw/github-backend-scan-failed.txt'
z=read(p).splitlines();clean=[line.split('\t',2)[-1]for line in z];selected=[line for line in clean if 'Run trivy image' in line or 'Total: 44' in line or 'Process completed with exit code 1' in line]
add('E29',8,'Hosted backend security gate fails closed',p,'trivy image --parallel 1 --severity HIGH,CRITICAL --exit-code 1 liora-backend:ci',result='FAILED',environment='GitHub Actions',version='Trivy 0.76.1 / 211199d',scope='Actual failed job output; 44 HIGH and 0 CRITICAL. Publication remains blocked.',content='\n'.join(selected),url='https://github.com/dionis1/liora-devops-platform/actions/runs/39920280796/job/120303913550')
p='docs/presentation-evidence/raw/container-security-context.txt'
add('E30',8,'Container security controls configured',p,'Review rendered workload security contexts',result='PARTIALLY_VALIDATED',kind='configuration',version='Kubernetes manifests at 211199d',scope='Static configuration. Fresh Docker fixture separately verified read-only/non-root operation; final Kubernetes deployment untested.',content=read(p))
p='kubernetes/base/networkpolicy.yaml'
add('E31',8,'Default-deny policy and explicit database traffic',p,'Review NetworkPolicy resources; kubectl kustomize overlays',result='PARTIALLY_VALIDATED',kind='configuration',version='networking.k8s.io/v1',scope='Configuration only. Policy enforcement on a live cluster remains NOT YET TESTED.',content=lines(p,0,10)+'\n\n'+lines(p,43,59))
p='docs/remediation-evidence/key-cleanup.json'
add('E32',8,'Temporary credential access removed',p,'Exact public-key match; approved removal; API absence verified',version='GitHub API / 2026-10-23',scope='Cleanup evidence only. A read-only repository deploy key was not verified or installed; no key material is shown.',content=read(p))
p='docs/presentation-evidence/raw/postgres16-browser-record-restore.txt'
add('E33',9,'Actual backup creation and mode 0600',p,'bash scripts/backup-postgres.sh liora-dev; stat BACKUP',version='PostgreSQL 16.10 / Docker isolated fixture',scope='Actual script via explicit kubectl-to-Docker adapter; no Kubernetes/cloud restore claim. Binary dump excluded from Git.',content=lines(p,0,10))
add('E34',9,'Restored record matches the browser-created item',p,'pg_restore into NEW defense_restore; SELECT id,title FROM item',version='PostgreSQL 16.10',scope='Actual source/restored rows. Same synthetic UUID/title as E07. Existing user databases were untouched.',content=lines(p,9,None))
p='docs/remediation-evidence/disaster-recovery.txt'
add('E35',9,'Failed backups leave no completed corrupt archive',p,'Deliberately fail pg_dump; reject unrelated namespace',version='PostgreSQL 16.10 / negative-control test',scope='Actual prior test output. Expected command failure is a passing negative-control assertion, not a real backup success.',content=read(p))
p='docs/architecture.md'
add('E36',10,'Architecture and engineering boundaries',p,'Review architecture.md and the official requirement checklist',kind='design',version='Platform architecture at 211199d',scope='Design diagram, not proof of a Hetzner deployment. Future cloud and manual production steps are labeled.',content='ARCHITECTURE')


p='docs/local-validation-evidence/kubernetes-live.log'
add('E37',4,'Historical ConfigMap, Ingress and rollout results',p,'kubectl apply local-dev.yaml; rollout status postgres/backend/frontend',observed='2026-10-22',version='k3d 5.9.0 / original first-pass images',scope='Actual first-pass resource creation and rollout output. New security/metrics manifests were not deployed.',content=block(p,'configmap/course-app-config created',20))
p='docs/local-validation-evidence/argocd-live.log'
add('E38',5,'Historical Argo components ready; sync still unproven',p,'kubectl -n argocd get pods,services; Argo health check',result='PARTIALLY_VALIDATED',observed='2026-10-22',version='Argo CD 3.5.5 / local k3d',scope='Actual running controllers/repository/server components. GitHub comparison failed afterward (E22); this is not Synced/Healthy application proof.',content=block(p,'NAME                                                   READY',15))

CSS = '''*{box-sizing:border-box}body{margin:0;background:#f0f3f7;color:#142338;font-family:Arial,sans-serif}main{max-width:1400px;margin:auto;padding:24px 32px}header{border-top:7px solid #176b8a;background:white;padding:18px 24px}h1{font-size:26px;line-height:1.15;margin:9px 0}h2{font-size:19px;margin:10px 0}.eyebrow{font-size:12px;font-weight:bold;letter-spacing:1.3px;color:#176b8a}.status{font-size:13px;font-weight:bold;color:#8a4200}.scope{font-size:15px;line-height:1.4;margin:10px 0}.command{font:13px monospace;overflow-wrap:anywhere}.panel{background:white;padding:18px 24px;margin-top:12px;border:1px solid #d4dee8}pre{font:15px/1.42 'DejaVu Sans Mono',monospace;white-space:pre-wrap;overflow-wrap:anywhere;margin:0;color:#142338}footer{font-size:11px;line-height:1.5;overflow-wrap:anywhere;padding:12px 4px;color:#47566a}.flow{display:flex;gap:12px;align-items:stretch;margin:15px 0}.box{background:#e9f2f7;border:1px solid #9dbbcb;flex:1;padding:15px;font-size:16px;line-height:1.45}.future{background:#fff4e0;border-color:#dcb568}a{color:#176b8a}img{max-width:100%;border:1px solid #d4dee8}.card{background:white;margin:18px 0;padding:20px}.metadata{font-size:14px;line-height:1.5}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:20px}@media print{.card{break-inside:avoid}}'''

(OUT/'views').mkdir(exist_ok=True)
for item in CATALOG:
    if '_content' not in item:
        continue
    content=item.pop('_content')
    mode={'archived-output':'ARCHIVED ACTUAL OUTPUT — NOT A LIVE TERMINAL', 'configuration':'CONFIGURATION EXCERPT — NOT DEPLOYMENT PROOF','design':'ARCHITECTURE DESIGN — NOT DEPLOYMENT PROOF'}[item['kind']]
    if content=='ARCHITECTURE':
        body='''<div class="flow"><div class="box">Original DataScientest app<br>React → FastAPI → PostgreSQL</div><div class="box">GitHub Actions<br>Tests → build → Trivy gates<br>Publish exact scanned images</div><div class="box">GitOps branches<br>deploy/dev automatic policy<br>Production manual sync</div></div><div class="flow"><div class="box future">Future Hetzner host<br>Terraform + Ansible + k3s<br>Cloud not provisioned</div><div class="box">Kubernetes design<br>Namespaces, PVC, Traefik<br>First-pass local dev tested</div><div class="box">Monitoring &amp; recovery<br>Prometheus / Grafana<br>SQL backup + fresh restore tested</div></div><p>Current release gate: 44 unfixed HIGH backend OS findings. New hardened cluster/Argo reconciliation and cloud recovery remain untested.</p>'''
    else:
        body='<pre>'+html.escape(content)+'</pre>'
    sources='<br>'.join(html.escape(a['path'])+'<br>SHA-256 '+a['sha256'] for a in item['sources'])
    title=f"{item['id']} · {item['title']}"
    req=REQUIREMENTS[item['requirement']-1]
    page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS}</style><main><header><div class="eyebrow">{mode}</div><h1>{html.escape(title)}</h1><div class="status">{item['result'].replace('_',' ')} · {html.escape(item['environment'])}</div><p class="scope">{html.escape(item['scope'])}</p><div class="command">{html.escape(item['command'])}</div></header><section class="panel">{body}</section><footer>Requirement {req['number']}. {html.escape(req['title'])}<br>Observed: {item['observed_date']} · Screenshot capture: {DATE} · Software: {html.escape(item['software'])}<br>{sources}</footer></main></html>'''
    (OUT/item['view']).write_text(page)

# Hashes are attached after capture; existing images remain unmodified.
for item in CATALOG:
    p=SHOTS/item['file']
    item['sha256']=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
manifest={'capture_date':DATE,'timezone':'Europe/Tirane','source_commit':'211199da8c52caf07199b155fb6baf28deb5b1f4','requirements':REQUIREMENTS,'status_legend':{'PASSED':'The narrow observed check passed, not the entire requirement.','FAILED':'The shown policy/integration failed; no success is implied.','PARTIALLY_VALIDATED':'Configuration/static evidence, with stated runtime gaps.','NOT_YET_TESTED':'No execution proof; use the missing-evidence register.'},'screenshots':CATALOG}
(SHOTS/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

index=['# Visual evidence index','',f'Capture date: {DATE} (Europe/Tirane). Original observation dates and software versions are recorded for every image.','', '**Actual UI** screenshots show real application, monitoring or GitHub pages. **Archived-output** screenshots show real saved command/API output in a labeled evidence viewer; they are not screenshots taken during the original run. **Configuration/design** views never prove deployment success. All full source artifacts and hashes are preserved.','', 'The exact ten official headings below are the primary organization. [Presentation plans](../presentation-evidence.md) · [Validation checklist](../requirements-validation-checklist.md) · [Machine-readable provenance](manifest.json) · [Offline gallery](../presentation-evidence/index.html) · [Capture protocol](capture-protocol.md)','']
gallery=[f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Liora graduation evidence</title><style>{CSS}</style><main><header><h1>Graduation presentation evidence</h1><p>Actual UI captures and clearly labeled archived-output/configuration views. Captured {DATE}. No cloud deployment or completed Argo sync is claimed.</p><p>Use the ten-minute plan in presentation-evidence.md. All image links work offline; no external scripts or assets are required.</p></header>']
for req in REQUIREMENTS:
    heading=f"{req['number']}. {req['title']}";index+=['## '+heading,''];cards=[];sub=['# '+heading,'']
    for s in CATALOG:
        if s['requirement']!=req['number']:continue
        details=f"**{s['id']} — {s['title']}** · **{s['result'].replace('_',' ')}** · `{s['kind']}`"
        image=f"[Screenshot]({s['file']})";source='; '.join(f"[{Path(a['path']).name}](../../{a['path']})" for a in s['sources'])
        index += [details,'',image+' · '+source,'',f"- Demonstrates: {s['scope']}",f"- Supports official requirement(s): {', '.join(map(str,s['supports']))}.",f"- Captured: {s['capture_date']}; original observation: {s['observed_date']}; environment: {s['environment']}.",f"- Software: {s['software']}.",f"- Command/page: `{s['command']}`"+(f" · [workflow]({s['workflow_url']})" if s['workflow_url'] else ''),'']
        sub += [f"- [{s['id']} — {s['title']}]({Path(s['file']).name}) — {s['result'].replace('_',' ')}; see [metadata](../README.md)."]
        cards.append(f'''<article class="card"><h2>{html.escape(s['id']+' · '+s['title'])}</h2><div class="metadata"><b>{s['result'].replace('_',' ')}</b> · {s['kind']}<br>Observed {s['observed_date']} · Captured {s['capture_date']}<br>{html.escape(s['scope'])}</div><a href="../screenshots/{s['file']}"><img loading="lazy" src="../screenshots/{s['file']}" alt="{html.escape(s['title'])}"></a></article>''')
    (SHOTS/req['directory']/'README.md').write_text('\n'.join(sub)+'\n')
    gallery.append('<section><h1>'+html.escape(heading)+'</h1><div class="gallery">'+''.join(cards)+'</div></section>')
index+=['## Missing execution or unavailable screenshots','', '[Detailed gaps and capture blockers](../presentation-evidence/missing-evidence.md). Every requirement has concrete evidence; several still lack successful end-to-end deployment proof.','']
(SHOTS/'README.md').write_text('\n'.join(index))
gallery.append('</main></html>');(OUT/'index.html').write_text(''.join(gallery))
print(f'Prepared {len(CATALOG)} evidence entries; {sum("view" in s for s in CATALOG)} archived/configuration/design views. Browser capture is a separate, explicit step.')
