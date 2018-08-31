#!/usr/bin/python
# -*- coding:utf-8 -*-
import socket
import argparse
import threading
import SocketServer
import json
import errno
import datetime
import sys
from massgrid_wif_ecies import MassGridencrypt
user='wany'
pwd='19950815'
serverip='47.92.28.155'
serverport=50001
connectuser='zxx'
connectuserip=''
connectuserport=''
def formatjson(method,id,params):
    data ={
        'jsonrpc':'2.0',
        'method' :method,
        'id'     :id,
        'params' : params 
    }
    return json.dumps(data)
def response(socket):
    data = ''  
    while True:  
        try:  
            new_data = sock.recv(1024)  
        except socket.error, e:  
            if e.args[0] == errno.EWOULDBLOCK:  
                break  
            raise  
        else:  
            if not new_data:  
                break  
            else:  
                print new_data  
                data += new_data
    if not data:
        sock.close()  
    else:
        processResponse(data)
def processResponse(json):
    data=json.loads(json)
    if not data:
        return False
    if data['id']=='0':
        if data['result']==True:
            print 'login success'
        else:
            print 'login fail'
    elif data['id']=='1':
        if data['result'] != False:
            connectuserip,connectuserport = data['result']
    else:
        return
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            while True:


                self.data=self.request.recv(1024)
                print("{} send:".format(self.client_address),self.data)
                if not self.data:
                    print("connection lost")
                    break
                self.request.sendall(self.data.upper())
        except Exception as e:
            print(self.client_address,"连接断开")
        finally:
            self.request.close()
    def setup(self):
        print("before handle,连接建立：",self.client_address)
        
    def finish(self):
        print("finish run  after handle")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', dest='mode', action='store_const', const='server', help='server')
    args = parser.parse_args()
    if args.mode == 'server':
        server=SocketServer.ForkingTCPServer((serverip,serverport),MyTCPHandler)
        server.serve_forever()
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(('127.0.0.1',9999))
        sock.setblocking(0)
        sock.connect((serverip, serverport))
        while True:
            cmd=raw_input('wait command')
            if cmd=='exit':
                sys.exit()
            elif cmd =='login':
                user=raw_input('input user')
                pwd=raw_input('input pwd')
                params=[user,pwd]
                jsonstr = formatjson('login','0',params)
                print 'send : {%s}'%jsonstr
                sock.sendall(jsonstr)
            elif cmd =='getuseraddress':
                connectuser=raw_input('input connectuser')
                params=[connectuser]
                jsonstr = formatjson('getuseraddress','1',params)
                print 'send : {%s}'%jsonstr
                sock.sendall(jsonstr)
            elif cmd == 'connect':
                if connectuserip =='' or connectuserport=='' :
                    continue

                try:
                    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock2.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                    sock2.bind(('127.0.0.1',9999))
                    sock2.setblocking(0)
                    sock2.connect((connectuserip, connectuserport))
                except:
                    sock2.listen(2)
                    while True:
                        print ('server waiting...')
                        conn,addr = sock2.accept()
                        client_data = conn.recv(1024)
                        print 'reach: ',(str(client_data,'utf8'))
                        conn.sendall(bytes('wany','utf8'))
            response(sock)
        sock.close()
