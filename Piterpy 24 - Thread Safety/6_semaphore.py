import concurrent.futures
import threading
import time

max_concurrent_bookings = 3
semaphore = threading.Semaphore(max_concurrent_bookings)


def book_travel_package():

    print(f"{int(time.time())} : {threading.current_thread().name}: Waiting.")

    with semaphore:
        print(
            f"{int(time.time())} : {threading.current_thread().name}: Booking travel package."
        )
        time.sleep(1)
        print(
            f"{int(time.time())}: {threading.current_thread().name}: Travel package booked"
        )


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=10, thread_name_prefix="Worker"
    ) as executor:
        for _ in range(10):
            executor.submit(book_travel_package)
