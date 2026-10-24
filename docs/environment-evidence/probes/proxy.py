from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
import http.client
class Proxy(BaseHTTPRequestHandler):
 def do_GET(self):self.forward()
 def do_POST(self):self.forward()
 def do_PATCH(self):self.forward()
 def do_DELETE(self):self.forward()
 def do_OPTIONS(self):self.forward()
 def forward(self):
  port=18080 if self.path.startswith(('/api/','/readyz','/metrics')) else 18082
  body=self.rfile.read(int(self.headers.get('Content-Length',0)))
  headers={k:v for k,v in self.headers.items() if k.lower()not in ['host','connection','accept-encoding']}
  try:
   c=http.client.HTTPConnection('127.0.0.1',port,timeout=15);c.request(self.command,self.path,body,headers);r=c.getresponse();data=r.read()
   self.send_response(r.status)
   for k,v in r.getheaders():
    if k.lower()not in ['connection','transfer-encoding','content-length']:self.send_header(k,v)
   self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);c.close()
  except Exception:
   self.send_error(502,'Temporary validation port-forward unavailable')
 def log_message(self,*args):pass
ThreadingHTTPServer(('127.0.0.1',18081),Proxy).serve_forever()
