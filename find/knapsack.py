class Item(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.weight = w

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def getWeight(self):
        return self.weight

    def __str__(self):
        result = '<' + self.name + ',' + str(self.value)\
            + ',' + str(self.weight) + '>'
        return result


def value(item):
    return item.getValue()


def weightInverse(item):
    return 1.0 / item.getWeight()


def density(item):
    return item.getValue() / item.getWeight()


def greedy(items, maxWeight, keyFunction):
    """假设Items是列表，maxWeight >= 0
    keyFunctions将物品元素映射为数值
    O(n*log(n)))(内置排序复杂度)"""
    itemsCopy = sorted(items, key=keyFunction, reverse=True)
    result = []
    totalValue, totalWeight = 0.0, 0.0
    for i in range(len(itemsCopy)):
        if totalWeight + itemsCopy[i].getWeight() <= maxWeight:
            result.append(itemsCopy[i])
            totalWeight += itemsCopy[i].getWeight()
            totalValue += itemsCopy[i].getValue()
    return result, totalValue


#
def buildItems():
    names = ['clock', 'painting', 'radio', 'vase', 'book', 'computer']
    values = [175, 90, 20, 50, 10, 200]
    weights = [10, 9, 4, 2, 1, 20]
    Items = []
    for i in range(len(values)):
        Items.append(Item(names[i], values[i], weights[i]))
    return Items


def testGreedy(items, maxWeight, keyFunction):
    taken, val = greedy(items, maxWeight, keyFunction)
    print('Total value of items taken is', val)
    for item in taken:
        print(' ', item)


def testGreedy01(maxWeight=20):
    items = buildItems()
    print('\nUse greedy by value to fill knapsack of size', maxWeight)
    testGreedy(items, maxWeight, value)
    print('\nUse greedy by weight to fill knapsack of size', maxWeight)
    testGreedy(items, maxWeight, weightInverse)
    print('\nUse greedy by density to fill knapsack of size', maxWeight)
    testGreedy(items, maxWeight, density)


testGreedy01()


# 下面枚举所有可能，然后选择最优，复杂度为（n*2^n）
def chooseBest(pSet, maxWeight, getVal, getWeight):
    bestVal = 0.0
    bestSet = None
    for items in pSet:
        itemsVal = 0.0
        itemsWeight = 0.0
        for item in items:
            itemsVal += getVal(item)
            itemsWeight += getWeight(item)
        if itemsWeight <= maxWeight and itemsVal > bestVal:
            bestVal = itemsVal
            bestSet = items
    return bestSet, bestVal


def getBinaryRep(n, numDigits):
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
    powerSet = []
    for i in range(0, 2 ** len(L)):
        binStr = getBinaryRep(i, len(L))
        subset = []
        for j in range(len(L)):
            if binStr[j] == '1':
                subset.append(L[j])
        powerSet.append(subset)
    return powerSet


def testBest(maxWeight=20):
    items = buildItems()
    pSet = genPowerSet(items)
    taken, val = chooseBest(pSet, maxWeight, Item.getValue, Item.getWeight)
    print('\nTotal value of items taken is', val)
    for item in taken:
        print(' ', item)


testBest()


def maxVal(toConsider, avail):
    """假设toConsider是一个物品列表（还没有考虑的物品），avail表示重量（可用的空间数量）
    返回一个元组表示0/1背包问题的解，包括物品总价值和物品列表"""
    if toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getWeight() > avail:
        # 探索右侧分支
        result = maxVal(toConsider[1:], avail)
    else:
        nextItem = toConsider[0]
        # 探索左侧分支
        withVal, withToTake = maxVal(toConsider[1:], avail - nextItem.getWeight())
        withVal += nextItem.getValue()
        # 探索右侧分支
        withoutVal, withoutToTake = maxVal(toConsider[1:], avail)
        # 选择更好的分支
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    return result
