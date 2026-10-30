def average(numbers):
    total = 0
    for i in range(len(numbers) - 1):
        total += numbers[i]
    return total / len(numbers)


print(average([2, 4, 6]))  # should print 4.0
