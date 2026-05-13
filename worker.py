import socket             
import pickle
import sklearn

s = socket.socket()         
port = 12345                
s.connect(('127.0.0.1', port)) 

reg = pickle.loads(s.recv(1024))

while True:
    block = pickle.loads(s.recv(1024))
    print(block)
    infered_block = {'u': block.get('u'), 
                     'K': reg.predict(block.get('W'))}
    print(infered_block)
    s.send(pickle.dumps(infered_block))
    s.close()
    break