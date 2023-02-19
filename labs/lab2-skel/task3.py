"""
Coffee Factory: A multiple producer - multiple consumer approach

Generate a base class Coffee which knows only the coffee name
Create the Espresso, Americano and Cappuccino classes which inherit the base class knowing that
each coffee type has a predetermined size.
Each of these classes have a get message method

Create 3 additional classes as following:
    * Distributor - A shared space where the producers puts coffees and the consumers takes them
    * CoffeeFactory - An infinite loop, which always sends coffees to the distributor
    * User - Another infinite loop, which always takes coffees from the distributor

The scope of this exercise is to correctly use threads, classes and synchronization objects.
The size of the coffee (ex. small, medium, large) is chosen randomly everytime.
The coffee type is chosen randomly everytime.

Example of output:

Consumer 65 consumed espresso
Factory 7 produced a nice small espresso
Consumer 87 consumed cappuccino
Factory 9 produced an italian medium cappuccino
Consumer 90 consumed americano
Consumer 84 consumed espresso
Factory 8 produced a strong medium americano
Consumer 135 consumed cappuccino
Consumer 94 consumed americano
"""

from threading import Lock, Thread, Semaphore
import random


class Coffee:
    """ Base class """

    def __init__(self, name, size):
        self.name = name
        self.size = size
        pass

    def get_name(self):
        """ Returns the coffee name """
        return self.name

    def get_size(self):
        """ Returns the coffee size """
        return self.size

    def get_message(self):
        return str(self.name) + " " + str(self.size)


class Espresso(Coffee):
    """ Espresso implementation """

    def __init__(self, size):
        super().__init__("espresso", size)
        pass


class Americano(Coffee):
    """ Americano implementation """

    def __init__(self, size):
        super().__init__("americano", size)
        pass


class Cappuccino(Coffee):
    """ Cappuccino implementation """

    def __init__(self, size):
        super().__init__("cappuccino", size)
        pass


class CoffeeFactory(Thread):
    def __init__(self, buf, coffee):
        Thread.__init__(self)
        self.buffer = buf
        self.coffee = coffee

    def run(self):
        self.buffer.produce(self.coffee)


class User(Thread):
    def __init__(self, buf):
        Thread.__init__(self)
        self.buffer = buf

    def run(self):
        self.buffer.consume()


class Distributor:
    def __init__(self, size):
        self.buffer = []
        self.semaphore = Semaphore(value=size)

    def produce(self, stuff):
        self.semaphore.acquire()
        self.buffer.append(stuff)

    def consume(self):
        self.semaphore.release()
        return self.buffer.pop()


if __name__ == '__main__':
    pass

buffer = Distributor(5)
factory_threads = []
for i in range(1, 15):
    factory_threads.append(CoffeeFactory(buffer, Cappuccino("medium")))

for i in range(1, 15):
    factory_threads.append(CoffeeFactory(buffer, Americano("small")))

for i in range(1, 15):
    factory_threads.append(CoffeeFactory(buffer, Espresso("large")))

consumer_threads = []
for i in range(1, 45):
    consumer_threads.append(User(buffer))

for thread in consumer_threads:
    thread.start()

for thread in factory_threads:
    thread.start()

for thread in factory_threads:
    thread.join()

for thread in consumer_threads:
    thread.join()
