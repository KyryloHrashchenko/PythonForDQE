import string # importing string module for generating random letter for key name
from random import randint, choice # importing random module for generating random numbers and choosing random letter

"""

1. create a list of random number of dicts (from 2 to 10)

dict's random numbers of keys should be letter,
dict's values should be a number (0-100),
example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]

"""

dict_list = [] # creating list of dictionaries

def create_dict(): # creating function for generating dictanaries with random number of keys and random values
    new_dict = {} # creating empty dictionary
    num_keys = randint(1, 10) # randomising number of keys from 1 to 10

    for i in range(num_keys): # Loop...
        random_key = choice(string.ascii_lowercase) # Creating key with random letter in its name
        random_value = randint(0, 100) # Creating random int value from 0 to 100
        new_dict[random_key] = random_value # Filling created results to new_dict variable

    return new_dict # Returning our created dictionary

num_dicts = randint(2, 10) # Variable for randomising number of dictionaries for list

for i in range(num_dicts): # Loop for filling our lists with random number of dictionaries
    dict_list.append(create_dict()) # Appending list with dictionaries, that are created using create_dict() function

# print(dict_list)
    
"""

2. get previously generated list of dicts and create one common dict:

if dicts have same key, we will take max value, and rename key with dict number with max value
if key is only in one dict - take it as is,
example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}

"""

unique_dict = {} # Creating dictionary for storing only unique keys from all of dictionaries
duplicated_dict  = {} # Creating dictionary for storing only duplicated keys from all of dictionaries
duplicated_keynames = []

all_keys = [key for my_dict in dict_list for key in my_dict] # Creating list of all keys from all dictionaries from dict_list

duplicated_keys = set([key for key in all_keys if all_keys.count(key) > 1]) # Finding only duplicated keys

for key in duplicated_keys: #Loop for findind max value for duplicated key and then filling it to duplicated_dict
    max_value = None # Creating empty variable for storing max value for duplicated keys
    source_dict = None # Creating empty variable to determine which dictionary contained max value from duplicated keys
    
    for i, my_dict in enumerate(dict_list, start=1): # Here we are indexing our dictionaries starting with number 1 (Giving each dictionary its own number)
        if key in my_dict: # If condition
            current_value = my_dict[key] # We are checking if key exists in my_dict 
            if max_value is None or current_value > max_value: # Condition, if max_value is empty or current_value greater than previous max_value
                max_value = current_value # Then rewrite max_value with current_value
                source_dict = i # Now source_dict stores index of dictionary, where max_value was located
    
    if max_value is not None: # If variable max_value is not empty...
        duplicated_dict[f"{key}_{source_dict}"] = max_value # then duplicated_dict dictionary filling with concatenation of key and '_' symbol and value from source_dict variable and value will be equal to max_value variable
        duplicated_keynames.append(key) # Append all duplicated keyd to seperate list duplicated_keynames


for my_dict in dict_list: # Unioning all dictionaries from dict_list
    unique_dict.update(my_dict) # And passing them to unique_dict dictionary
#print ("test:", unique_dict)

for key in duplicated_keynames: # for each key from duplicated_keynames
    unique_dict.pop(key, None) # delete all keys from unique_dict, which exists in duplicated_keynames (duplicates keys)

final_dict = {**duplicated_dict, **unique_dict} # Merging duplicated_dict and unique_dict to final_dict for final result

print("List with dictionaries->", dict_list) # Displaying list of dictionaries - dict_list
#print("Duplicated keynames->", duplicated_keynames)
print("Duplicated->", duplicated_dict) # Displaying dictionary with duplicated keys and their max values
print("Unique->", unique_dict) # Displaying dictionary with keys without duplicates
print("Final->", final_dict) # FInal merged dictionary