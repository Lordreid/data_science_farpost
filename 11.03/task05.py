"""
Given a list of integers numbers "nums".

You need to find a sub-array with length less equal to "k", with maximal sum.

The written function should return the sum of this sub-array.

Examples:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    result = 16
"""
from typing import List

nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3

def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    max_sum = float(-1) #ставим чтобы любое число было больше чем это
    n = len(nums)
    
    for i in range(n):
        current_sum = 0
        
        for j in range(i, min(i + k, n)):
            current_sum += nums[j]
            
            if current_sum > max_sum:
                max_sum = current_sum
    return max_sum


test = find_maximal_subarray_sum(nums, k)
print(test)