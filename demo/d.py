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


global numFibCalls
test(5)
