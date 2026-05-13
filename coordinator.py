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

def generate_Z(BI, m, b):
    Z = []
    bi = sorted(BI, key=lambda d: d['u'])
    for i in range(int(m/b)):
        Z.append(BI[i].get('K'))
    Z = np.(Z)
    return Z

iris = load_iris()
X = iris.data
Y = iris.target
reg = linear_model.LinearRegression()
reg.fit(X, Y)
m = len(X)
b = 10

B = generate_B(X, m, b)
BI = []
B_copy = B.copy()

s = socket.socket()
port = 12345
s.bind(('', port))
s.listen(5)
c, addr = s.accept()
print('Got connection from ', addr)
c.send(pickle.dumps(reg))

while True:
    if len(BI) == len(B):
        c.send(pickle.dumps('END'))
        c.close()
        break
    c.send(pickle.dumps(B_copy[0]))
    infered_block = pickle.loads(c.recv(1024))
    B_copy[:] = [d for d in B_copy if d.get('u') != infered_block.get('u')]
    BI.append(infered_block)

Z = generate_Z(BI, m, b)
print(Z)