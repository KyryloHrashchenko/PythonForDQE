from random import randint  # importing module for randomizing numbers

# create list of 100 random numbers from 0 to 1000
a = []  # Creating empty list
for x in range(1, 101):  # Creating range for list from 1 to 100
    a.append(randint(0, 1000))  # Filling list with random numbers from 0 to 1000


# print (a)

# sort list from min to max(without using sort())
def bubble_sort(array):  # Creating function for bubble sorting
    n = len(array)  # Creating variable that is equal of array length
    for i in range(n):
        already_sorted = True  # Create a flag that will allow the function to terminate early (if there is no to sort)
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:  # If the item you are looking at is greater than its adjacent value, then swap
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False  # This flag is needed to not stop the code prematurely
        if already_sorted:  # If there were no swaps during the last iteration, the array is already sorted(stop it)
            break
    return array


bubble_sort(a)  # sorting list using bubble_sort function
# print (a)

# calculate average for even and odd numbers
even = []  # creating variable with datatype list for even numbers
odd = []  # creating variable with datatype list for odd numbers

for element in a:  # for each element of the list...
    if element % 2 == 0:  # if element in the list can be divided by 2...
        even.append(element)  # Then add this element to the even list
    else:  # If not, add it to the odd list
        odd.append(element)


# print(odd)

def calculate_average(arr):  # creating function calculate_average for finding average
    if not arr:
        return None  # if 0, return nothing
    return sum(arr) / len(arr)  # sum of all elements of array divide on number of elements of array


average_even = calculate_average(even)  # pass the average value to average_even variable
average_odd = calculate_average(odd)  # pass the average value to average_odd variable
print("Average of even numbers: ", average_even)  # printing average_even results
print("Average of odd numbers: ", average_odd)  # printing average_odd results
