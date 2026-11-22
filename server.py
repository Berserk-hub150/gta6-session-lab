import argparse,json,math,secrets,threading,time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
class Lobby:
    def __init__(self):
        self.players={};self.lock=threading.Lock()
    def update(self,action,body):
        with self.lock:
            now=time.monotonic()
            self.players={k:v for k,v in self.players.items() if now-v['seen']<120}
            if action=='join':
                name=body.get('name')
                if not isinstance(name,str) or not 1<=len(name.strip())<=32: raise ValueError('Use 1–32 characters')
                key=secrets.token_urlsafe(18);self.players[key]=dict(name=name.strip(),x=50,y=50,seen=now)
                return {'token':key}
            if action=='move':
                p=self.players.get(body.get('token'))
                if not p: raise ValueError('Session expired. Join again.')
                x,y=body.get('x'),body.get('y')
                if not all(type(v) in (int,float) and math.isfinite(v) and 0<=v<=100 for v in (x,y)): raise ValueError('Coordinates outside arena')
                p.update(x=x,y=y,seen=now)
            return [{k:p[k] for k in ('name','x','y')} for p in self.players.values()]
lobby=Lobby()
class Handler(BaseHTTPRequestHandler):
    def reply(self,body,status=200,kind='application/json'):
        raw=body if isinstance(body,bytes) else json.dumps(body).encode()
        self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        path=urlsplit(self.path).path
        if path=='/state': self.reply(lobby.update('state',{}));return
        assets={'/':('index.html','text/html; charset=utf-8'),'/app.js':('app.js','text/javascript'),'/style.css':('style.css','text/css')}
        if path not in assets: self.send_error(404);return
        name,kind=assets[path];self.reply((Path(__file__).parent/name).read_bytes(),kind=kind)
    def do_POST(self):
        if self.path not in ['/join','/move']: self.send_error(404);return
        try:
            if self.headers.get_content_type()!='application/json': raise ValueError('Use application/json')
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=2048: raise ValueError('Invalid message size')
            data=json.loads(self.rfile.read(length))
            if not isinstance(data,dict): raise ValueError('Expected an object')
            self.reply(lobby.update(self.path[1:],data))
        except (ValueError,TypeError) as e: self.reply({'error':str(e)},400)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8765);a=p.parse_args()
    ThreadingHTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
