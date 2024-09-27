import concurrent.futures
import random
import threading
import time

num_travelers = 4
barrier = threading.Barrier(num_travelers + 1)  # +1 for the tour guide


def traveler():
    print(
        f"{int(time.time())}: Traveler {threading.current_thread().name} is getting ready"
    )
    time.sleep(random.randint(1, 4))
    print(
        f"{int(time.time())}: Traveler  {threading.current_thread().name} is ready and waiting"
    )

    barrier.wait()
    print(
        f"{int(time.time())}: Traveler  {threading.current_thread().name} started the tour"
    )


def tour_guide():
    print(f"{int(time.time())}: Tour guide is ready & waiting for travelers")
    barrier.wait()
    print(f"{int(time.time())}: Tour guide: Everyone is now ready!")


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=5, thread_name_prefix="Traveller"
    ) as executor:
        # create 4 threads for travelers and one for the tour guide
        traveler_futures = [executor.submit(traveler) for _ in range(num_travelers)]
        guide_future = executor.submit(tour_guide)
