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
#from massgrid_wif_ecies import MassGridencrypt
user='wany'
pwd='19950815'
serverip='120.78.79.157'
serverport=10001
connectuser='zxx'
connectuserip=''
connectuserport=''
dictuser={}
dictaddr={}
def formatjson(method,id,params):
    if not method:
        data ={
        'jsonrpc':'2.0',
        'id'     :id,
        'result' : params 
        
    }
    else:
            
        data ={
            'jsonrpc':'2.0',
            'method' :method,
            'id'     :id,
            'params' : params 
        }
    return json.dumps(data)
def response(socket):
    data = ''  
    try:  
        new_data = sock.recv(1024)  
    except socket.error, e:  
        if e.args[0] == errno.EWOULDBLOCK:  
            print 'error'
    else:  
        if not new_data:
            print 'no new data'  
        else:  
            print 'new_data',new_data  
            data += new_data
    if not data:
        sock.close()  
    else:
        processResponse(data)
def processResponse(jsons):
    print 'json:',jsons
    data=json.loads(jsons)
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
            self.data=self.request.recv(1024)
            data=json.loads(self.data)
            print 'recv: ',self.data
            jsonstr=''
            if data['id']=='0':
                dictuser[data['params'][0]]=data['params'][1]
                dictaddr[data['params'][0]]=self.client_address
                jsonstr = formatjson(None,'0',True)
            if data['id']=='1':
                #if dictaddr
                if data['params'][0] not in dictaddr:
                    jsonstr = formatjson(None,'1',False)
                else:
                    jsonstr = formatjson(None,'1',dictaddr[data['params'][0]])
            print 'send: ',jsonstr
            if not self.data:
                print("connection lost")
            self.request.sendall(jsonstr)
        except Exception as e:
            print(self.client_address,"connect broke")
        finally:
            self.request.close()
    def setup(self):
        print("before handle,connected:",self.client_address)
        
    def finish(self):
        print("finish run  after handle")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', dest='mode', action='store_const', const='server', help='server')
    args = parser.parse_args()
    if args.mode == 'server':
        print 'use server :',serverip,serverport
        server=SocketServer.ForkingTCPServer(('',serverport),MyTCPHandler)
        server.serve_forever()
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(('',9999))
        #sock.setblocking(0)
        print 'connect server :',serverip,serverport
        sock.connect((serverip, serverport))
        print 'local address :',sock.getsockname()
        while True:
            cmd=raw_input('wait command\n')
            if cmd=='exit':
                sys.exit()
            elif cmd =='login':
                user=raw_input('input user\n')
                pwd=raw_input('input pwd\n')
                params=[user,pwd]
                jsonstr = formatjson('login','0',params)
                print 'send : {%s}'%jsonstr
                sock.sendall(jsonstr)
            elif cmd =='getuseraddress':
                connectuser=raw_input('input connectuser\n')
                params=[connectuser]
                jsonstr = formatjson('getuseraddress','1',params)
                print 'send : {%s}'%jsonstr
                sock.sendall(jsonstr)
            elif cmd == 'connect':
                connectuserip=raw_input('input connectuserip\n')
                connectuserport=raw_input('input connectuserport\n')
                if connectuserip =='' or connectuserport=='' :
                    continue

                try:
                    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock2.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                    sock2.bind(('',9999))
                    sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock3.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                    sock3.bind(('',9999))
                    #sock2.setblocking(0)
                    sock2.connect((connectuserip, connectuserport))
                except:
                    sock3.listen(5)
                    while True:
                        print ('server waiting...')
                        conn,addr = sock3.accept()
                        client_data = conn.recv(1024)
                        print 'reach: ',(str(client_data,'utf8'))
                        conn.sendall(bytes('wany','utf8'))
                else:
                        print 'connection success'
            response(sock)
        sock.close()
