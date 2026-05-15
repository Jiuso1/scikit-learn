import socket             
import pickle
import sklearn

s = socket.socket()         
port = 12345                
s.connect(('127.0.0.1', port)) 

reg = pickle.loads(s.recv(1024))

print('Model received from the coordinator. Listening and computing.')

while True:
    received = pickle.loads(s.recv(1024))
    if received == 'END':
        print('The coordinator has sent me an END message.')
        s.close()
        break       
    block = received
    infered_block = {'u': block.get('u'), 
                     'K': reg.predict(block.get('W'))}
    s.send(pickle.dumps(infered_block))