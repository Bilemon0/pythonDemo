import random
import pylab


class Location(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def move(self, deltaX, deltaY):
        """deltaX和Y为数值型"""
        return Location(self.x + deltaX, self.y + deltaY)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distFrom(self, other):
        ox, oy = other.x, other.y
        xDist, yDist = self.x - ox, self.y - oy
        return (xDist ** 2 + yDist ** 2) ** 0.5

    def __str__(self):
        return '<' + str(self.x) + ',' + str(self.y) + '>'


class Field(object):
    def __init__(self):
        self.drunks = {}

    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc

    def moveDrunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        # 使用Location的move方法获得一个新位置
        self.drunks[drunk] = currentLocation.move(xDist, yDist)

    def getLoc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]


class Drunk(object):
    def __init__(self, name=None):
        self.name = name

    def __str__(self):
        if self is not None:
            return self.name
        return 'Anonymous'


class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return random.choice(stepChoices)


class ColdDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0, 1), (0, -2), (1, 0), (-1, 0)]
        return random.choice(stepChoices)


class EWDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(1, 0), (-1, 0)]
        return random.choice(stepChoices)


class styleIterator(object):
    """迭代器，可以在一个样式序列间滚动轮换"""

    def __init__(self, styles):
        self.index = 0
        self.styles = styles

    def nextStyle(self):
        result = self.styles[self.index]
        if self.index == len(self.styles) - 1:
            self.index = 0
        else:
            self.index += 1
        return result


def walk(f, d, numSteps):
    """假设f是一个Field对象，d是f中的一个Drunk对象，numSteps是正整数。
    将d移动numSteps次，返回这次游走最终位置与开始位置之间的距离"""
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return start.distFrom(f.getLoc(d))


def simWalks(numSteps, numTrials, dClass):
    """假设numSteps是非负数，numTrials是正整数，dClass是Drunk的一个子类
    模拟numTrials次游走，每次游走numSteps步，返回一个列表，表示每次模拟的距离"""
    Homer = dClass()
    origin = Location(0, 0)
    distances = []
    for t in range(numTrials):
        f = Field()
        f.addDrunk(Homer, origin)
        distances.append(round(walk(f, Homer, numSteps), 1))
    return distances


def drunkTest(walkLengths, numTrials, dClass):
    """假设walkLengths是非负整数序列，numTrials是正整数，dClass是Drunk的一个子类
    对于walkLengths中的每个步数，运行numTrials次simWalks函数，并输出结果"""
    for numSteps in walkLengths:
        distances = simWalks(numSteps, numTrials, dClass)
        print(dClass.__name__, 'random walk of', numSteps, 'steps')
        print(' Mean =', round(sum(distances) / len(distances), 4))
        print(' Max =', max(distances), 'Min =', min(distances))


def simAll(drunkKinds, walkLengths, numTrials):
    for dClass in drunkKinds:
        drunkTest(walkLengths, numTrials, dClass)


def simDrunk(numTrials, dClass, walkLengths):
    meanDistances = []
    for numSteps in walkLengths:
        print('Starting simulation of', numSteps, 'steps')
        trials = simWalks(numSteps, numTrials, dClass)
        mean = sum(trials) / len(trials)
        meanDistances.append(mean)
    return meanDistances


def simAll1(drunkKinds, walkLengths, numTrials):
    """步数增加时距离发生的变化"""
    styleChoice = styleIterator(('m-', 'r:', 'k-.'))
    for dClass in drunkKinds:
        curStyle = styleChoice.nextStyle()
        print('Starting simulation of', dClass.__name__)
        means = simDrunk(numTrials, dClass, walkLengths)
        pylab.plot(walkLengths, means, curStyle, label=dClass.__name__)
    pylab.title('Mean Distance from Origin (' + str(numTrials) + 'trials)')
    pylab.xlabel('Number of Steps')
    pylab.ylabel('Distance from Origin')
    pylab.legend(loc='best')
    pylab.semilogx()
    pylab.semilogy()
    pylab.show()


def getFinalLocs(numSteps, numTrials, dClass):
    locs = []
    d = dClass()
    for r in range(numTrials):
        f = Field()
        f.addDrunk(d, Location(0, 0))
        for s in range(numSteps):
            f.moveDrunk(d)
        locs.append(f.getLoc(d))
    return locs


def plotLocs(drunkKinds, numSteps, numTrials):
    """对于某个特定的步数，各个最终位置分布"""
    styleChoice = styleIterator(('k+', 'r^', 'mo'))
    for dClass in drunkKinds:
        locs = getFinalLocs(numSteps, numTrials, dClass)
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        meanX = sum(xVals) / len(xVals)
        meanY = sum(yVals) / len(yVals)
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle, label=dClass.__name__ + 'mean loc. = <' + str(meanX) +
                                                 ', ' + str(meanY) + '>')
    pylab.title('Location at End of Walks (' + str(numSteps) + ' Steps)')
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc='lower left')
    pylab.axhline(0)
    pylab.axvline(0)
    pylab.show()


def traceWalk(drunkKinds, numSteps):
    """单次游走经过的路径"""
    styleChoice = styleIterator(('k+', 'r^', 'mo'))
    f = Field()
    for dClass in drunkKinds:
        d = dClass()
        f.addDrunk(d, Location(0, 0))
        locs = []
        for s in range(numSteps):
            f.moveDrunk(d)
            locs.append(f.getLoc(d))
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle, label=dClass.__name__)
    pylab.title('Spots Visited on Walk (' + str(numSteps) + 'steps)')
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc='best')
    pylab.show()


# drunkTest([10, 100, 1000, 10000, 100000], 100, UsualDrunk)
# simAll1((UsualDrunk, ColdDrunk, EWDrunk), (100, 1000, 10000, 100000), 100)
plotLocs((UsualDrunk, ColdDrunk, EWDrunk), 100, 400)
# traceWalk((UsualDrunk, ColdDrunk, EWDrunk), 200)
