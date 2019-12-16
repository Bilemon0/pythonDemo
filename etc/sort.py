def setSort(L):
    """选择排序：假设L是可用>排序的列表,O(n^2)"""
    suffixStart = 0
    while suffixStart != len(L):
        # 检查后缀集合中的每个元素
        for i in range(suffixStart, len(L)):
            if L[i] < L[suffixStart]:
                L[suffixStart], L[i] = L[i], L[suffixStart]
        suffixStart += 1


def merge(left, right, compare):
    """归并排序：假设left和right是两个有序列表，compare定义了一种元素排序规则。
    返回一个新的有序列表（按照compare定义的顺序）其中包含left+right相同的元素"""
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if compare(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result


def mergeSort(L, compare=lambda x, y: x < y):
    """假设L是列表，compare定义了排序规则，返回一个新的有序列表,O(n*log(n))"""
    if len(L) < 2:
        return L[:]
    else:
        middle = len(L) // 2
        left = mergeSort(L[:middle], compare)
        right = mergeSort(L[middle:], compare)
        return merge(left, right, compare)


print(mergeSort([6, 7, 1, 5, 4, 8, 2]))

