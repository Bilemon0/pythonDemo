def findRoot(_k, _root, _epsilon):
    """_k是底数,_root是幂,_epsilon是精度"""
    guess = _k / float(_root)
    numGuesses = 0
    while abs(guess ** _root - _k) >= _epsilon:
        guess = guess - ((guess ** _root - _k) / (_root * (guess ** (_root - 1))))
        numGuesses += 1
        print('guess =', guess)
    print('numGuesses =', numGuesses)
    print('Square root of', _k, 'is about', guess)


k = int(input('Enter an integer: '))
root = int(input('Enter root: '))
epsilon = float(input('Enter epsilon: '))
findRoot(k, root, epsilon)

