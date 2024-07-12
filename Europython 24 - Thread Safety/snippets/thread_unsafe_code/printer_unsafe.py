from concurrent import futures
import threading


def printer():
    message = f"Printing from thread: {threading.get_ident()}"
    end_separator = f" | Separator of {threading.get_ident()}\n"  # default end is '\n'
    print(message, end=end_separator)


with futures.ThreadPoolExecutor(max_workers=3) as executor:
    for _ in range(8):
        executor.submit(printer)

"""
Printing from thread: 79484 | Separator of 79484
Printing from thread: 79484 | Separator of 79484
Printing from thread: 79484Printing from thread: 72360 | Separator of 72360
 | Separator of 79484
Printing from thread: 79484 | Separator of 79484
Printing from thread: 72360Printing from thread: 79484 | Separator of 79484
Printing from thread: 79484 | Separator of 79484
 | Separator of 72360
"""
