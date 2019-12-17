def fib(x):
    """假设x是正整数，返回第x个斐波那契数"""
    global numFibCalls
    numFibCalls += 1
    if x == 0 or x == 1:
        return 1
    else:
        return fib(x - 1) + fib(x - 2)


def test(n):
    for i in range(n + 1):
        global numFibCalls
        numFibCalls = 0
        print("fib of", i, '=', fib(i))
        print("for", numFibCalls, "times")


def fastFib(n, memo={}):
    """假设n是非负数，返回第n个斐波那契数
    动态规划"""
    if n == 0 or n == 1:
        return 1
    try:
        return memo[n]
    except KeyError:
        result = fastFib(n - 1, memo) + fastFib(n - 2, memo)
        memo[n] = result
        print("fib of", n, '=', result)
        return result


global numFibCalls
test(20)
fastFib(120, {})
