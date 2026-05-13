import socket             
import pickle
import sklearn

s = socket.socket()         
port = 12345                
s.connect(('127.0.0.1', port)) 

reg = pickle.loads(s.recv(1024))

while True:
    received = pickle.loads(s.recv(1024))
    if received == 'END':
        s.close()
        break       
    block = received
    infered_block = {'u': block.get('u'), 
                     'K': reg.predict(block.get('W'))}
    s.send(pickle.dumps(infered_block))