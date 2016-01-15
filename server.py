#  coding: utf-8 
import SocketServer
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.response_200 = "HTTP/1.1 200 OK\r\n"
        self.response_404 = "HTTP/1.1 404 Not Found\r\n"
        SocketServer.BaseRequestHandler.__init__(self, request,
                                                 client_address, server)

    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        formatted = self.data.split("\r\n")
        self.print_request(formatted)

        path = formatted[0].split(" ")[1]
            
        if (path == "/"):
            self.request.sendall(self.response_200)
            return

        root_path = os.getcwd() + "/www"

        if (not os.path.isfile(root_path+path)):
            self.request.sendall(self.response_404)
            return
        #os.direxists("path")
        elif (path == "/index.html"):
            self.add_file(path)
            self.request.sendall(self.response_200)
        else:
            self.request.sendall(self.response_200)
        
    def add_file(self, file_path):
        root_path = os.getcwd() + "/www"
        file0 = open(root_path+file_path, "r")

        self.response_200 += "\n"
        for line in file0:
            line = line.strip("\n")
            self.response_200 += line+"\r\n"
        file0.close()
        
        return

    def print_request(self, request_str):
        print "New request:"
        for line in request_str:
            print line

        return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
# a
