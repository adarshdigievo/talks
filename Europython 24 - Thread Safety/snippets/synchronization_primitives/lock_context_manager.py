# The code here produces same results as that of lock.py

import threading
import time

lock = threading.Lock()


def thread_func():
    print(f"Thread {threading.current_thread().ident} reached thread_func")
    with lock:
        # Critical section of code
        print(f"Lock acquired at {int(time.time())}, executing critical section")
        time.sleep(5)
        print(f"Lock Releasing by {threading.current_thread().ident}")


thread1 = threading.Thread(target=thread_func).start()
thread2 = threading.Thread(target=thread_func).start()
