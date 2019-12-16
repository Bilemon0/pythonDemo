def getBinaryRep(n, numDigits):
    """假设n和numDigits为非负数
    返回一个长度为numDigits的字符串，为n的二进制表示"""
    result = ''
    while n > 0:
        result = str(n % 2) + result
        n = n // 2
    if len(result) > numDigits:
        raise ValueError('not enough digits')
    for i in range(numDigits - len(result)):
        result = '0' + result
    return result


def genPowerSet(L):
    """假设L是列表
    返回一个列表，包含L中元素所有可能的集合
    e.g.L=[1, 2],则返回的列表包含[], [1], [2], [1, 2]"""
    powerSet = []
    for i in range(0, 2 ** len(L)):
        binStr = getBinaryRep(i, len(L))
        subset = []
        for j in range(len(L)):
            if binStr[j] == '1':
                subset.append(L[j])
        powerSet.append(subset)
    print('length of this result is ' + str(len(powerSet)))
    print(powerSet)
    return powerSet


genPowerSet(['a', 'b', 'c', 'd'])

# 生成所有n位的二进制数，也就是从0到2^n之间的所有二进制数；
# 对于这2^n +1个二进制数中的每一个数b，如果b中某一位为1，那么就从 L 中选择索引值对应
# 这一位的元素，由此生成一个列表。举例来说，如果 L 是 ['x', 'y'] 并且b是 01 ，那么就
# 生成列表 ['y'] 。
# O(2^len(L))

