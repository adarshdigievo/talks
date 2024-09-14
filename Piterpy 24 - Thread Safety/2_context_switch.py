import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def worker():
    for i in range(3):
        time.sleep(0.01)
        print(f"Thread {threading.current_thread().name}: iteration {i}")


if __name__ == "__main__":
    print(f"{sys.getswitchinterval()=}")

    with ThreadPoolExecutor(max_workers=4, thread_name_prefix="Worker") as executor:
        for i in range(4):
            executor.submit(worker)
