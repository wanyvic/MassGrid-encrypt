#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import SocketServer
import pyjsonrpc
from massgrid_wif_ecies import MassGridencrypt

# class MyTCPHandler(SocketServer.BaseRequestHandler):
#     def handle(self):
#         try:
#             while True:
#                 self.data=self.request.recv(1024)
#                 print("{} send:".format(self.client_address),self.data)
#                 if not self.data:
#                     print("connection lost")
#                     break
#                 self.request.sendall(self.data.upper())
#         except Exception as e:
#             print(self.client_address,"连接断开")
#         finally:
#             self.request.close()
#     def setup(self):
#         print("before handle,连接建立：",self.client_address)
        
#     def finish(self):
#         print("finish run  after handle")
class RequestHandler(pyjsonrpc.HttpRequestHandler):
    dictaddress={}
    dictpwd={}
    def IsSameUserAddress(self,username):
        if self.dictaddress.get(username)!=None :
            if self.dictaddress[username]==self.client_address :
                return True
        return False
    def IsSameUserPassWord(self,username,password):
        
        if self.dictpwd.get(username)!=None :
            if self.dictpwd[username]==password :
                print 'a'
                return True
            print 'b' 
            return False
        print 'c'
        return True
    @pyjsonrpc.rpcmethod
    def login(self,username,password):
        if self.IsSameUserPassWord(username ,password) == False:
            return False
        self.dictpwd[username]=password
        self.dictaddress[username]=self.client_address
        return True
    @pyjsonrpc.rpcmethod
    def ping(self,a):
        return a + 1
    @pyjsonrpc.rpcmethod
    def getuseraddress(self,username):
        if self.dictaddress.get(username)==None :
            return None
        else:
            return self.dictaddress[username]
    @pyjsonrpc.rpcmethod
    def logout(self,username):
        if ~self.IsSameUserAddress(username):
            return False
        self.dictaddress.pop(username)
        return True
    @pyjsonrpc.rpcmethod
    def add(self,a,b):
        print self.default_request_version
        print self.request_version
        return a+b
if __name__ == "__main__":
     HOST,PORT = "localhost",9999
    # print '1'
     server=SocketServer.ForkingTCPServer((HOST,PORT),MyTCPHandler)
    # print '2'
     server.serve_forever()

    # print '3'
    # Threading HTTP-Server
    http_server = pyjsonrpc.ThreadingHttpServer(
        server_address = ('127.0.0.1', 9999),
        RequestHandlerClass = RequestHandler
    )
    print "Starting HTTP server ..."
    print "URL: http://localhost:9999"
    http_server.serve_forever()