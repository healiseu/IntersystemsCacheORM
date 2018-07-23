
#%% **************************************************
#%% First terminal (receiver)

from socket import SocketReceiver

socket_receiver = SocketReceiver(host='localhost', port=5005)

print(socket_receiver)

socket_receiver.listen(1024)

#%%
# How to set an Intersystems CACHE listener 
# at a console enter the following commands
# set tcp="|TCP|5005|"
# open tcp:(:5005):1 write $s($t:"OK", 1:"failed"),!
# for line=1:1 use tcp read text use 0 write line, ?5, text, !

#%% **************************************************
#%% Second terminal (client)

from socket import SocketSender

socket_sender = SocketSender(host='localhost', port=4200)

print(socket_sender)

socket_sender.connect()

#%% Start sending string messages

socket_sender.send('Hello world')
socket_sender.send('Do you copy ???')


#%% Test with Intersystems Cache Python Binding
import intersys.pythonbind3

conn = intersys.pythonbind3.connection( )
conn.connect_now('localhost[1972]:SAMPLES', '_SYSTEM', '123', None)
samplesDB = intersys.pythonbind3.database(conn)
samplesDB.run_class_method("Sample.Person", "SendMessage", ["Hello world", 5005])
