import json,subprocess,sys,hashlib
from pathlib import Path
ENV=sys.argv[1];ns='liora-'+ENV;cmd=['kubectl','--kubeconfig','/tmp/liora-env-20261024/kubeconfig','-n',ns]
def get(args):return json.loads(subprocess.check_output(cmd+args+['-o','json']))
pods=get(['get','pods'])['items'];out={'environment':ENV,'namespace':ns,'pods':[]}
for p in pods:
 statuses=p['status'].get('containerStatuses',[])
 out['pods'].append({'name':p['metadata']['name'],'phase':p['status']['phase'],'ready':all(c['ready'] for c in statuses),'restarts':sum(c['restartCount'] for c in statuses),'images':[{'name':c['name'],'requested_image':c['image'],'image_id':c['imageID']} for c in statuses],'init_containers':[{'name':c['name'],'image_id':c['imageID'],'exit_code':c.get('state',{}).get('terminated',{}).get('exitCode')} for c in p['status'].get('initContainerStatuses',[])]})
assert len(out['pods'])==3 and all(p['ready'] and p['phase']=='Running' for p in out['pods'])
out['configuration']=get(['get','configmap','course-app-config'])['data'];out['services']=[{'name':s['metadata']['name'],'cluster_ip':s['spec']['clusterIP']} for s in get(['get','services'])['items']]
out['storage']=[{'name':p['metadata']['name'],'phase':p['status']['phase'],'volume':p['spec']['volumeName']} for p in get(['get','pvc'])['items']]
secret=get(['get','secret','course-app-secrets']);out['secret_metadata']={'namespace':secret['metadata']['namespace'],'name':secret['metadata']['name'],'uid':secret['metadata']['uid'],'keys':sorted(secret['data'])}
release=json.loads(Path('docs/environment-evidence/registry-release.json').read_text())
for image in release['images']:
 actual=next(c['image_id'] for p in out['pods'] for c in p['images'] if c['name']==image['component']);assert actual.endswith(image['digest'])
out['published_digests_match_running_images']=True
Path('docs/environment-evidence/'+ENV+'-runtime.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASSED',ns,'all 3 pods Ready, release digests match, distinct namespace-scoped objects captured')
