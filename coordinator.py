from sklearn.datasets import load_iris
from sklearn import linear_model
import numpy as np
import socket
import pickle
from _thread import start_new_thread
import time

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
    sorted(BI, key=lambda x: x['u'])
    Z = np.array([])
    for i in range(int(m/b)):
        Z = np.concatenate((Z, BI[i].get('K')))
    return Z

# lock = threading.Lock()
iris = load_iris()
X = iris.data
Y = iris.target
reg = linear_model.LinearRegression()
reg.fit(X, Y)
X = np.random.rand(1200, 4)
m = len(X)
b = 10
B = generate_B(X, m, b)
BI = []
B_copy = B.copy()

def handle_client(c):
    c.send(pickle.dumps(reg))
    while True:
        if len(B_copy) == 0:
            c.send(pickle.dumps('END'))
            c.close()
            break
        c.send(pickle.dumps(B_copy[0]))
        infered_block = pickle.loads(c.recv(1024))
        B_copy[:] = [d for d in B_copy if d.get('u') != infered_block.get('u')]
        BI.append(infered_block)
    c.close()

def main():
    s = socket.socket()
    port = 12345
    s.bind(('', port))
    s.listen(5)

    while True:
        if len(BI) == len(B):
            break
        c, addr = s.accept()
        # lock.acquire()
        start_linkference = time.time()
        # print('Got connection from ', addr, '.')
        start_new_thread(handle_client, (c,))

    Z = generate_Z(BI, m, b)
    end_linkference = time.time()
    time_linkference = end_linkference - start_linkference
    print(time_linkference , ' seconds with Linkference')

    print('Z generated')

    start_not_linkference = time.time()
    if np.array_equal(reg.predict(X), Z):
        print('Z equals the prediction.')
    end_not_linkference = time.time()
    time_not_linkference = end_not_linkference - start_not_linkference
    print(time_not_linkference , ' seconds without Linkference')
    # print('time_linkference equals time_not_linkference ', (((time_not_linkference - time_linkference)/time_not_linkference)*-100) , '%')

if __name__ == '__main__':
    main()