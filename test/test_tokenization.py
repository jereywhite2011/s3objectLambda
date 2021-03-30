########################################################
# test_tokenization.py - Tests the tokenization algo
# takes a value, tokens it and untokens it
########################################################
# Author: Jeremiah White
# License: MIT License
# Version: 1.0.1
## Email: jeremiah.white@gmail.com
########################################################


import sys

# Setup initial variables
rotation = 4
TOKENIZATION_INTEGER = "0123456789"
TOKENIZATION_STRING = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ."
input_string = sys.argv[1]
tokens = []
reconstructed = []

# Creates dictionaries for tokenizing/untokenizing
CHR_TOKENS = dict(zip(range(len(TOKENIZATION_STRING)),
                      list(TOKENIZATION_STRING)))
NUM_TOKENS = dict(zip(range(10), list(TOKENIZATION_INTEGER)))
CHR_TOKENS_REV = dict(zip(list(TOKENIZATION_STRING),
                          range(len(TOKENIZATION_STRING))))
NUM_TOKENS_REV = dict(zip(list(TOKENIZATION_INTEGER), range(10)))

# Print initial string
print(input_string)

# Tokenizes the string
for char in input_string:
    if char in TOKENIZATION_INTEGER:
        rotation = (NUM_TOKENS_REV[char] + rotation) % 10
        tokens.append(NUM_TOKENS[rotation])
    elif char in TOKENIZATION_STRING:
        rotation = (CHR_TOKENS_REV[char] + rotation) % 53
        tokens.append(CHR_TOKENS[rotation])
    else:
        tokens.append(char)

# Print the tokenized string
print("".join(tokens))

# Reset the rotation
rotation = 4

# Untokenize the tokenized string
for char in tokens:
    if char in TOKENIZATION_INTEGER:
        index = (NUM_TOKENS_REV[char] - rotation) % 10
        rotation = (index + rotation) % 10
        reconstructed.append(NUM_TOKENS[index])
    elif char in TOKENIZATION_STRING:
        index = (CHR_TOKENS_REV[char] - rotation) % 53
        rotation = (index + rotation) % 53
        reconstructed.append(CHR_TOKENS[index])
    else:
        reconstructed.append(char)

# Print the untokenized string
print("".join(reconstructed))
