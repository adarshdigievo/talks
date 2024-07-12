import sys
import threading
import time


def worker(id_):
    for i in range(3):
        time.sleep(0.05)
        print(f"Worker thread id {id_}; iteration {i}")


if __name__ == "__main__":
    print(f"{sys.getswitchinterval()=}")

    for i in range(3):
        threading.Thread(target=worker, args=(i,)).start()

"""
sys.getswitchinterval()=0.005
Worker thread id 2; iteration 0
Worker thread id 1; iteration 0
Worker thread id 0; iteration 0
Worker thread id 0; iteration 1
Worker thread id 1; iteration 1
Worker thread id 2; iteration 1
Worker thread id 2; iteration 2
Worker thread id 1; iteration 2
Worker thread id 0; iteration 2
"""
