import sys,json,subprocess,urllib.request,urllib.parse,urllib.error
from pathlib import Path
root=Path('/tmp/liora-env-20261024');env=sys.argv[1];other='dev'if env=='prod'else'prod';cmd=['kubectl','--kubeconfig',str(root/'kubeconfig')];out={}
# Read credentials only in memory. Persist only comparison booleans.
creds={e:dict(l.split('=',1)for l in (root/(e+'.env')).read_text().splitlines()) for e in ['dev','prod']}
assert all(creds['dev'][k]!=creds['prod'][k] for k in creds['dev'])
out['credential_values_are_distinct']=True
code='''import socket,json
r={}
for name,host in [('own','postgres'),('other','postgres.OTHER.svc.cluster.local')]:
 try:
  s=socket.create_connection((host,5432),timeout=3);s.close();r[name]='CONNECTED'
 except TimeoutError:r[name]='BLOCKED_TIMEOUT'
 except ConnectionRefusedError:r[name]='BLOCKED_REFUSED'
print(json.dumps(r))
assert r['own']=='CONNECTED' and r['other'].startswith('BLOCKED_'),r
'''.replace('OTHER','liora-'+other)
p=subprocess.run(cmd+['-n','liora-'+env,'exec','deployment/backend','--','python','-c',code],text=True,capture_output=True,check=True);out['database_tcp']=json.loads(p.stdout)
base='http://127.0.0.1:18081'
def call(path,data=None,token=None):
 headers={}
 if token:headers['Authorization']='Bearer '+token
 if data:headers['Content-Type']='application/x-www-form-urlencoded'
 try:
  with urllib.request.urlopen(urllib.request.Request(base+path,data=urllib.parse.urlencode(data).encode() if data else None,headers=headers),timeout=15)as r:return r.status,json.load(r)
 except urllib.error.HTTPError as e:return e.code,None
status,body=call('/api/v1/login/access-token',{'username':creds[env]['FIRST_SUPERUSER'],'password':creds[env]['FIRST_SUPERUSER_PASSWORD']});assert status==200
token=body['access_token'];other_id=json.loads(Path('docs/environment-evidence/'+other+'-http.json').read_text())['item']['id']
status,_=call('/api/v1/items/'+other_id,token=token);assert status==404;out['other_environment_item_http']=status
status,_=call('/api/v1/login/access-token',{'username':creds[other]['FIRST_SUPERUSER'],'password':creds[other]['FIRST_SUPERUSER_PASSWORD']});assert status==400;out['other_environment_credentials_http']=status
out['environment']=env;out['result']='PASSED';out['scope']='Same-namespace DB connection allowed; other namespace DB connection blocked; other environment credentials and record rejected. No shared-node failure isolation claim.'
Path('docs/environment-evidence/'+env+'-isolation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
