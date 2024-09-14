import threading
import time

booking_lock = threading.RLock()


def book_flight_and_hotel():
    print(f" Thread {threading.current_thread().ident}: Attempting to book flight")
    with booking_lock:
        time.sleep(1)
        print(
            f" Thread {threading.current_thread().ident}: Flight booked, now trying to book hotel"
        )
        book_hotel()  # Now this will work without deadlock


def book_hotel():
    print(f" Thread {threading.current_thread().ident}: Attempting to book hotel")
    with booking_lock:
        time.sleep(1)
        print(f" Thread {threading.current_thread().ident}: Hotel booked")


if __name__ == "__main__":
    thread1 = threading.Thread(target=book_flight_and_hotel)
    thread1.start()
    thread1.join()
