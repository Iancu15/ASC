from concurrent.futures import ThreadPoolExecutor
from random import choice, seed

seed(42)

sequence = "AGTCTCTCTCT"

samples = []
for i in range(0, 100):
    adn = ""
    for j in range(0, 10000):
        adn += choice(['A', 'G', 'T', 'C'])

    samples.append(adn)


def search_sample(sample_index):
    if samples[sample_index].find(sequence) != 1:
        return "DNA sequence found in ", sample_index


with ThreadPoolExecutor(max_workers=30) as executor:
    result = []
    for i in range(0, 100):
        result.append(executor.submit(search_sample, i))

    for result_elem in result:
        print(result_elem.result())
