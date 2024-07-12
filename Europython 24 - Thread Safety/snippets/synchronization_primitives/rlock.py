import threading
import time


class BankAccount:
    def __init__(self):
        self.balance = 0
        self.lock = threading.RLock()

    def deposit(self, amount):
        print(f"Thread {threading.current_thread().ident} waiting to acquire lock for deposit()")
        with self.lock:
            print(f"Thread {threading.current_thread().ident} acquired lock for deposit()")
            time.sleep(0.1)
            self._update_balance(amount)

    def _update_balance(self, amount):
        print(f"Thread {threading.current_thread().ident} waiting to acquire lock for _update_balance()")
        with self.lock:  # Deadlock won't occur because of RLock usage
            print(f"Thread {threading.current_thread().ident} acquired lock for _update_balance()")
            self.balance += amount


account = BankAccount()


def make_deposits():
    account.deposit(100)


# Threads to perform deposits
threads = [threading.Thread(target=make_deposits) for _ in range(3)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"Final balance: {account.balance}")

"""
Thread 23128 waiting to acquire lock for deposit()
Thread 23128 acquired lock for deposit()
Thread 11944 waiting to acquire lock for deposit()
Thread 27752 waiting to acquire lock for deposit()
Thread 23128 waiting to acquire lock for _update_balance()
Thread 23128 acquired lock for _update_balance()
Thread 11944 acquired lock for deposit()
Thread 11944 waiting to acquire lock for _update_balance()
Thread 11944 acquired lock for _update_balance()
Thread 27752 acquired lock for deposit()
Thread 27752 waiting to acquire lock for _update_balance()
Thread 27752 acquired lock for _update_balance()
Final balance: 300
"""