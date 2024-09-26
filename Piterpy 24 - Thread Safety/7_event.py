import threading
import time

flight_landed = threading.Event()


def wait_for_passengers():
    print(
        f"{int(time.time())} : {threading.current_thread().name}: Waiting for flight to land"
    )
    flight_landed.wait()
    print(
        f"{int(time.time())} : {threading.current_thread().name}:Flight landed, collecting passengers"
    )


def flight_status_update():
    time.sleep(3)
    print(f"{int(time.time())} : {threading.current_thread().name}: Flight has landed")
    flight_landed.set()


if __name__ == "__main__":
    t1 = threading.Thread(target=wait_for_passengers, name="Passengers thread")
    t2 = threading.Thread(target=flight_status_update, name="Flight status thread")

    t1.start()
    t2.start()

    t1.join()
    t2.join()
