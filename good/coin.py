import pylab
import random


def variance(X):
    """假设X是一个数值型列表。返回X的方差"""
    mean = sum(X)/len(X)
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return tot/len(X)


def stdDev(X):
    """假设X是一个数值型列表。返回X的标准差"""
    return variance(X)**0.5


def flip(numFlips):
    heads = 0
    for i in range(numFlips):
        if random.choice(('H', 'T')) == 'H':
            heads += 1
    return heads / float(numFlips)


def flipSim(numFlipsPerTrial, numTrials):
    fracHeads = []
    for i in range(numTrials):
        fracHeads.append(flip(numFlipsPerTrial))
    mean = sum(fracHeads) / len(fracHeads)
    sd = stdDev(fracHeads)
    return fracHeads, mean, sd


def labelPlot(numFlips, numTrials, mean, sd):
    pylab.title(str(numTrials) + ' trials of ' + str(numFlips) + ' flips each')
    pylab.xlabel('Fraction of Heads')
    pylab.ylabel('Number of Trials')
    pylab.annotate('Mean = ' + str(round(mean, 4)) + '\nSD = ' + str(round(sd, 4)),
                   size='x-large', xycoords='axes fraction', xy=(0.67, 0.5))


def makePlots(numFlips1, numFlips2, numTrials):
    val1, mean1, sd1 = flipSim(numFlips1, numTrials)
    pylab.hist(val1, bins=20)
    xMin, xMax = pylab.xlim()
    labelPlot(numFlips1, numTrials, mean1, sd1)
    pylab.show()
    pylab.figure()
    val2, mean2, sd2 = flipSim(numFlips2, numTrials)
    pylab.hist(val2, bins=20)
    pylab.xlim(xMin, xMax)
    labelPlot(numFlips2, numTrials, mean2, sd2)
    pylab.show()


# 模拟10万次抛硬币，第一个每次试验抛硬币100次，第二个每次试验抛1000次
makePlots(100, 1000, 10000)

