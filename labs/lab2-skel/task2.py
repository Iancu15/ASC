"""
    Basic thread handling exercise:

    Use the Thread class to create and run more than 10 threads which print their name and a random
    number they receive as argument. The number of threads must be received from the command line.

    e.g. Hello, I'm Thread-96 and I received the number 42

"""

import random
from threading import Thread

def hello_world(id, nr):
    print("I'm Thread-" + str(id) + " and I received the number", nr)

threads = []
for t in range(0, 15):
    threads.append(Thread(target=hello_world, args=(t, random.randrange(1, 100))))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
