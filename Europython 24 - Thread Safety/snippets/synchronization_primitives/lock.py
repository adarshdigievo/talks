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
Thread 2440 reached thread_func
Lock acquired at 1720595236, executing critical section
Thread 12976 reached thread_func
Lock Releasing by 2440
Lock acquired at 1720595241, executing critical section
Lock Releasing by 12976
"""
