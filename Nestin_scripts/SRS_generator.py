# This script generates a random sample of 4 combinations from a list of 6 combinations.
# This random sample is used to select the 4 combinations that will be used to pick the wells
# using the Systematic Random Sampling method.

# The seed is being recorded in my lab notebook so the values can be reproduced if needed.
# In this case, the sampling will be 1/6 (ssf)
import random

random.seed("KD63.7")  # Set the seed value

combinations = [(1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12)]

random_selection = random.sample(combinations, 2)
print(random_selection)
