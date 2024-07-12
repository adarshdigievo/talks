from concurrent import futures
import threading

# Lock object
print_lock = threading.Lock()


def printer():
    message = f"Printing from thread: {threading.get_ident()}"
    end_separator = f" | Separator of {threading.get_ident()}\n"  # default end is '\n'

    # Acquire the lock before printing
    with print_lock:
        print(message, end=end_separator)


# Use ThreadPoolExecutor to run the printer function in multiple threads
with futures.ThreadPoolExecutor(max_workers=3) as executor:
    for _ in range(8):
        executor.submit(printer)

"""
Printing from thread: 13048 | Separator of 13048
Printing from thread: 13048 | Separator of 13048
Printing from thread: 13048 | Separator of 13048
Printing from thread: 13048 | Separator of 13048
Printing from thread: 3528 | Separator of 3528
Printing from thread: 13048 | Separator of 13048
Printing from thread: 3528 | Separator of 3528
Printing from thread: 3796 | Separator of 3796
"""
