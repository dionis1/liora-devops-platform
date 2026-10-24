import sys,json,urllib.request,urllib.parse
from pathlib import Path
ENV=sys.argv[1];root=Path('/tmp/liora-env-20261024');creds=dict(l.split('=',1) for l in (root/(ENV+'.env')).read_text().splitlines());base='http://127.0.0.1:18081'
def req(path,body=None,token=None,form=False):
 data=urllib.parse.urlencode(body).encode() if form else json.dumps(body).encode() if body is not None else None
 headers={'Content-Type':'application/x-www-form-urlencoded' if form else 'application/json'}
 if token:headers['Authorization']='Bearer '+token
 with urllib.request.urlopen(urllib.request.Request(base+path,data=data,headers=headers),timeout=20) as r:return r.status,r.read()
assert req('/')[0]==200
assert json.loads(req('/api/v1/utils/health-check/')[1]) is True
assert req('/readyz')[0]==200
_,body=req('/api/v1/login/access-token',{'username':creds['FIRST_SUPERUSER'],'password':creds['FIRST_SUPERUSER_PASSWORD']},form=True)
token=json.loads(body)['access_token']
_,body=req('/api/v1/items/',{'title':ENV.upper()+' environment isolation record','description':'Synthetic local acceptance test; no personal data'},token)
item=json.loads(body);assert req('/api/v1/items/'+item['id'],token=token)[0]==200
_,body=req('/api/v1/items/',token=token);items=json.loads(body)
assert item['id'] in [x['id'] for x in items['data']]
result={'environment':ENV,'result':'PASSED','access':'loopback port-forwards plus temporary same-origin HTTP proxy; not public ingress/TLS','frontend_http':200,'health_http':200,'health_body':True,'database_readiness_http':200,'login_and_jwt':'PASSED','create_and_read_item':'PASSED','item':{'id':item['id'],'title':item['title']},'visible_item_count':items['count']}
Path('docs/environment-evidence/'+ENV+'-http.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
