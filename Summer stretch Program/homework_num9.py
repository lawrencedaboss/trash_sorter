def find_max(a, b, c, d, e):
    largest = a
    for num in [b, c, d, e]:
        if num > largest:
            largest = num
    return largest
