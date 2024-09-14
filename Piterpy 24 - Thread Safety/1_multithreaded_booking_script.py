import concurrent.futures
import time

available_seats = 10


def book_seat():
    global available_seats
    if available_seats > 0:
        time.sleep(0.1)
        available_seats -= 1
        print(f"Seat booked. Remaining seats: {available_seats}")
    else:
        print("Sorry, no seats available.")


if __name__ == "__main__":
    concurrent_threads = 10

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=concurrent_threads
    ) as executor:
        for i in range(15):
            executor.submit(book_seat)

    print(f"Final seat count: {available_seats}")
