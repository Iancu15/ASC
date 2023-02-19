"""
	Bonus task: load all the available coffee recipes from the folder 'recipes/'
	File format:
		first line: coffee name
		next lines: resource=percentage

	info and examples for handling files:
		http://cs.curs.pub.ro/wiki/asc/asc:lab1:index#operatii_cu_fisiere
		https://docs.python.org/3/library/io.html
		https://docs.python.org/3/library/os.path.html
"""

RECIPES_FOLDER = "recipes"

def get_recipe(coffee_type):
    path = RECIPES_FOLDER + "/" + coffee_type + ".txt"
    file = open(path, "r")
    lines = file.readlines()
    recipe = {}
    for i in range(1,4):
        splitted_line = lines[i].strip().split("=")
        recipe[splitted_line[0]] = int(splitted_line[1])

    return recipe

def load_recipes():
    recipes = {}
    for coffee_type in ["americano", "cappuccino", "espresso"]:
        recipes[coffee_type] = get_recipe(coffee_type)

    return recipes