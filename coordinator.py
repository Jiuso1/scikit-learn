from sklearn.datasets import load_iris
from sklearn import linear_model
import numpy as np
import socket
import pickle

def generate_B(X, m, b):
    B = []
    block = []
    u = 0

    for i in range(m):
        if len(block) == b:
            B.append({
                'u': u,
                'W': np.array(block)
            })
            u += 1
            block = []

        block.append(X[i])

    if len(block) > 0:
        B.append({
            'u': u,
            'W': np.array(block)
        })

    return B

iris = load_iris()
X = iris.data
Y = iris.target
reg = linear_model.LinearRegression()
reg.fit(X, Y)
m = len(X)
b = 10

B = generate_B(X, m, b)
BI = []

#for i in range(int(m/b)):
#    print(B[i].get('u'))
#    print(B[i].get('W'))

s = socket.socket()
port = 12345
s.bind(('', port))
s.listen(5)
c, addr = s.accept()
print('Got connection from ', addr)
c.send(pickle.dumps(reg))

while True:
    print(B[0])
    c.send(pickle.dumps(B[0]))
    infered_block = pickle.loads(c.recv(1024))
    B.pop(infered_block.get('u'))
    BI.append(infered_block)
    #print(BI)
    c.close()
    break