import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor

customer_available_condition = threading.Condition()

# Customers waiting to be served by the Travel agent
customer_queue = []


def serve_customers():
    while True:
        with customer_available_condition:
            # Wait for a customer to arrive
            while not customer_queue:
                print(f"{int(time.time())}: Travel agent is waiting for a customer.")
                customer_available_condition.wait()  # .wait() releases the lock, blocks

            # Serve the customer
            customer = customer_queue.pop(0)
            print(f"{int(time.time())}: Travel agent is serving {customer}.")

        # Simulate the time taken to serve the customer
        time.sleep(1)
        print(f"{int(time.time())}: Travel agent has finished serving {customer}.")


def add_customer_to_queue(name):
    with customer_available_condition:
        print(f"{int(time.time())}: {name} has arrived at the office.")
        customer_queue.append(name)

        customer_available_condition.notify()  # .notify() wakes up one of the waiting threads


customers = [
    ("Customer 1", 1),
    ("Customer 2", 1),
    ("Customer 3", 0),
    ("Customer 4", 1),
    ("Customer 5", 0)
]

if __name__ == "__main__":

    with ThreadPoolExecutor(max_workers=6) as executor:

        travel_agent_thread = executor.submit(serve_customers)

        for name, arrival_delay in customers:
            # Simulate customers arriving at random intervals
            time.sleep(arrival_delay)

            executor.submit(add_customer_to_queue, name)
