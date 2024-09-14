import concurrent.futures
import threading
import time

available_seats = 10
lock = threading.Lock()


def book_seat():
    global available_seats

    # the critical section is protected by the lock
    with lock:
        if available_seats > 0:
            time.sleep(0.01)
            available_seats -= 1
            print(f"Seat booked. Remaining seats: {available_seats}")
        else:
            print("Sorry, no seats available.")


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(15):
            executor.submit(book_seat)

    print(f"Final seat count: {available_seats}")
