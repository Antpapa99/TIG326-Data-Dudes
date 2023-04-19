nums = [1,2,1,5,3,4]
#nums[0] = 0
#if match
#index +1
def getConcatenation(nums):
    i = 0
    output = []
    for numbers in nums:
        print(numbers)
        print(nums[0])
        if numbers == nums[0]:
            output.append(numbers)
        return output

print(getConcatenation(nums))
