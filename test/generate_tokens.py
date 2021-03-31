########################################################
# generate_tokens.py - Generates sample tokenization
# strings
########################################################
# Author: Jeremiah White
# License: MIT License
# Version: 1.0.1
## Email: jeremiah.white@gmail.com
########################################################


import random
import math

# Start with a list of all possible values
starting_string = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.')
starting_integer = list('0123456789')

def generate_string(txt):
    # Generate the key by pulling out one value at a time and print the result
    # Void return
    final = ''
    while len(txt) > 0:
        tmp = math.floor(random.random() * len(txt))
        final += txt.pop(tmp)
    print(final)

generate_string(starting_string)
generate_string(starting_integer)
