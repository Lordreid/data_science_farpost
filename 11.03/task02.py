"""
Given a cell with "it's a fib sequence" from slideshow,
    please write function "check_fib", which accepts a Sequence of integers, and
    returns if the given sequence is a Fibonacci sequence

We guarantee, that the given sequence contain >= 0 integers inside.

"""




from collections.abc import Sequence

def check_fibonacci(data: Sequence[int]) -> bool:
    if not data:
        return False
    if len(data) >= 1 and data[0] != 0:
        return False
    if len(data) >= 2 and data[1] != 1:
        return False
    for i in range(2, len(data)):
        if data[i] != data[i-1] + data[i-2]:
            return False
    return True


#проверка

testdata = [4,6,43,43,6,4,6]
testdata_check = check_fibonacci(testdata)
print(testdata_check) #false


testdata = [0, 1, 1, 2, 3, 5, 8, 13, 21]
testdata_check = check_fibonacci(testdata)
print(testdata_check) #true