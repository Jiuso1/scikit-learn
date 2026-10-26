from sklearn.datasets import load_iris
from sklearn import linear_model
import numpy as np
import socket
import pickle
from _thread import start_new_thread
import threading
import time


def generate_B(X, m, b):
    B = []
    block = []
    u = 0

    for i in range(m):
        if len(block) == b:
            B.append({"u": u, "W": np.array(block)})
            u += 1
            block = []

        block.append(X[i])

    if len(block) > 0:
        B.append({"u": u, "W": np.array(block)})

    return B


def generate_Z(BI, m, b):
    sorted(BI, key=lambda x: x["u"])
    Z = np.array([])
    for i in range(int(m / b)):
        Z = np.concatenate((Z, BI[i].get("K")))
    return Z


iris = load_iris()
X = iris.data
Y = iris.target
reg = linear_model.LinearRegression()
reg.fit(X, Y)
X = np.random.rand(100000, 4)  # 100000
m = len(X)
b = 10
B = generate_B(X, m, b)
BI = []
B_copy = B.copy()
print(B_copy[-1])


def handle_client(c, lock):
    c.send(pickle.dumps(reg))
    while True:
        lock.acquire()
        if len(B_copy) == 0:
            c.send(pickle.dumps("END"))
            lock.release()
            c.close()
            break
        c.send(pickle.dumps(B_copy[0]))  # Key line
        infered_block = pickle.loads(c.recv(1024))
        B_copy[:] = [d for d in B_copy if d.get("u") != infered_block.get("u")]
        BI.append(infered_block)
        lock.release()
    c.close()


def main():
    s = socket.socket()
    port = 12345
    s.bind(("", port))
    s.listen(5)
    s.settimeout(0.001)
    lock = threading.Lock()

    while True:
        if len(BI) == len(B):
            # print("break with len(BI) =", len(BI), " and len(B) =", len(B))
            break
        try:
            c, addr = s.accept()
        except socket.timeout:
            # print("continue with len(BI) =", len(BI), " and len(B) =", len(B))
            continue
        print("Got connection from ", addr, ".")
        start_new_thread(handle_client, (c, lock))

    Z = generate_Z(BI, m, b)

    print("Z generated")

    if np.array_equal(reg.predict(X), Z):
        print("Z equals the prediction.")


if __name__ == "__main__":
    main()
