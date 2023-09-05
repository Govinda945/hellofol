# Example list
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Using a for loop with if-else
result_loop = []
for num in numbers:
    if num % 2 == 0:
        result_loop.append(num * 2)
    else:
        result_loop.append(num * 3)

print("Result using loop:", result_loop)

# Using a list comprehension with if-else
result_list_comp = [num * 2 if num % 2 == 0 else num * 3 for num in numbers]

print("Result using list comprehension:", result_list_comp)
