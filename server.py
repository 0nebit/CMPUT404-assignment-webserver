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
        self.response_404 = "HTTP/1.1 404 Not Found\r\n\r\n404: Page " + \
                            "Not Found"
        SocketServer.BaseRequestHandler.__init__(self, request,
                                                 client_address, server)

    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        # process request text
        formatted = self.data.split("\r\n")
        self.print_request(formatted)

        path = formatted[0].split(" ")[1]
        root_path = os.getcwd() + "/www"

        print ("PATH: %s" % path)
        print ("REAL PATH: %s" % os.path.realpath(root_path+path))
        real_path = os.path.realpath(root_path+path)

        if (real_path == root_path):
            path = "/"
        elif (real_path.startswith(root_path+"/")):
            # get relative path to /www/ from given path
            path = real_path.split(root_path)[1]
        else: # invalid path
            return self.request.sendall(self.response_404)
        
        # check root dir
        if (path == "/"):
            if (os.path.isfile(root_path+"/index.html")):
                self.add_file("/index.html")
                self.request.sendall(self.response_200)
            # if root index.html does not exist
            else:
                self.request.sendall(self.response_404)
        elif (path[-1] == "/"): # directory
            # check if directory exists
            if (os.path.isdir(root_path+path)):
                # if index.html exists
                if (os.path.isfile(root_path+path+"index.html")):
                    self.add_file(path+"index.html")
                    self.request.sendall(self.response_200)
                else:
                    self.request.sendall(self.response_200)
            else:
                self.request.sendall(self.response_404)
        # a directory but does not end in '/'
        elif (os.path.isdir(root_path+path)):
            """ What to do with this? """
            self.request.sendall(self.response_404)
        else: # regular file
            if (os.path.isfile(root_path+path)):
                # path is not within /www/
                if (not os.path.realpath(root_path+path).startswith(
                        root_path)):
                    self.request.sendall(self.response_404)
                else:
                    self.add_file(path)
                    self.request.sendall(self.response_200)
            else:
                self.request.sendall(self.response_404)

        return
    
    def add_file(self, file_path):
        # handle css and html files
        # HERE
        if (file_path.endswith(".css")):
            self.response_200 += "Content-Type: text/css\r\n"
        elif (file_path.endswith(".html")):
            self.response_200 += "Content-Type: text/html\r\n"
            
        root_path = os.getcwd() + "/www"
        file0 = open(root_path+file_path, "r")

        self.response_200 += "\r\n" # add a '\r'?
        for line in file0:
            line = line.strip("\n")
            self.response_200 += line+"\r\n"
        file0.close()
        
        return

    def print_request(self, request_str):
        print "New request:"
        for line in request_str:
            print line
        print "\n"
        
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
