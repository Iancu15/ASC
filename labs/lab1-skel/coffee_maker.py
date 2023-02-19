"""
A command-line controlled coffee maker.
"""

import sys
from load_recipes import load_recipes

"""
Implement the coffee maker's commands. Interact with the user via stdin and print to stdout.

Requirements:
    - use functions
    - use __main__ code block
    - access and modify dicts and/or lists
    - use at least once some string formatting (e.g. functions such as strip(), lower(),
    format()) and types of printing (e.g. "%s %s" % tuple(["a", "b"]) prints "a b"
    - BONUS: read the coffee recipes from a file, put the file-handling code in another module
    and import it (see the recipes/ folder)

There's a section in the lab with syntax and examples for each requirement.

Feel free to define more commands, other coffee types, more resources if you'd like and have time.
"""

"""
Tips:
*  Start by showing a message to the user to enter a command, remove our initial messages
*  Keep types of available coffees in a data structure such as a list or dict
e.g. a dict with coffee name as a key and another dict with resource mappings (resource:percent)
as value
"""

# Commands
EXIT = "exit"
LIST_COFFEES = "list"
MAKE_COFFEE = "make"  #!!! when making coffee you must first check that you have enough resources!
HELP = "help"
REFILL = "refill"
RESOURCE_STATUS = "status"
commands = [EXIT, LIST_COFFEES, MAKE_COFFEE, REFILL, RESOURCE_STATUS, HELP]

# Coffee examples
ESPRESSO = "espresso"
AMERICANO = "americano"
CAPPUCCINO = "cappuccino"

# Resources examples
WATER = "water"
COFFEE = "coffee"
MILK = "milk"

"""
Example result/interactions:

I'm a smart coffee maker
Enter command:
list
americano, cappuccino, espresso
Enter command:
status
water: 100%
coffee: 100%
milk: 100%
Enter command:
make
Which coffee?
espresso
Here's your espresso!
Enter command:
refill
Which resource? Type 'all' for refilling everything
water
water: 100%
coffee: 90%
milk: 100%
Enter command:
exit
"""


def make_coffee(resources, recipes):
    print("Which coffee?")
    coffee_type = sys.stdin.readline().strip()
    recipe = recipes[coffee_type]
    for key, value in recipe.items():
        if resources[key] < value:
            print("Not enough resources to make the coffee")
            return

    for key, value in recipe.items():
        resources[key] -= value

    print("Here's your", coffee_type, "!")

def refill(resources):
    print("Which resource? Type 'all' for refilling everything")
    line = sys.stdin.readline().strip()
    if line == "all":
        resources[WATER] = 100
        resources[COFFEE] = 100
        resources[MILK] = 100
    else:
        resources[line] = 100

    print_status(resources)

def print_status(resources):
    print("water:", resources[WATER], "%")
    print("coffee:", resources[COFFEE], "%")
    print("milk:", resources[MILK], "%")

def main():
    resources = {WATER: 100, COFFEE: 100, MILK: 100}
    recipes = load_recipes()
    print("I'm a simple coffee maker")
    while True:
        print("Enter command:")
        line = sys.stdin.readline().strip()
        if line == EXIT:
            exit(1)
        elif line == LIST_COFFEES:
            print(ESPRESSO, AMERICANO, CAPPUCCINO)
        elif line == MAKE_COFFEE:
            make_coffee(resources, recipes)
        elif line == HELP:
            print("exit -> exit")
            print("list -> list coffees")
            print("make -> make coffee")
            print("refill -> refill resources")
            print("status -> list status of resources")
        elif line == REFILL:
            refill(resources)
        elif line == RESOURCE_STATUS:
            print_status(resources)

if __name__ == "__main__":
    main()