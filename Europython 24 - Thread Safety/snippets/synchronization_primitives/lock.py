import threading
import time

lock = threading.Lock()


def thread_func():
    print(f"Thread {threading.current_thread().ident} waiting to acquire lock")
    lock.acquire()
    try:
        # Critical section of code
        print(
            f"Lock acquired by {threading.current_thread().ident} at timestamp:{int(time.time())}, executing critical section")
        time.sleep(5)
    finally:
        print(f"Lock Releasing by {threading.current_thread().ident}")
        lock.release()


thread1 = threading.Thread(target=thread_func).start()
thread2 = threading.Thread(target=thread_func).start()

"""
Thread 11848 waiting to acquire lock
Lock acquired by 11848 at timestamp:1720777564, executing critical section
Thread 29480 waiting to acquire lock
Lock Releasing by 11848
Lock acquired by 29480 at timestamp:1720777569, executing critical section
Lock Releasing by 29480
"""
