class Node(object):
    def __init__(self, name):
        """假设name是字符串"""
        self.name = name

    def getName(self):
        return self.name

    def __str__(self):
        return self.name


class Edge(object):
    def __init__(self, src, dest):
        """假设src和dest是节点"""
        self.src = src
        self.dest = dest

    def getSource(self):
        return self.src

    def getDestination(self):
        return self.dest

    def __str__(self):
        return self.src.getName() + '->' + self.dest.getName()


class WeightedEdge(Edge):
    def __init__(self, src, dest, weight=1.0):
        """假设src和dest是节点，weight是个权重数值"""
        super().__init__(src, dest)
        self.weight = weight

    def getWeight(self):
        return self.weight

    def __str__(self):
        return self.src.getName() + '->(' + str(self.weight) + ')'\
            + self.dest.getName()


class Digraph(object):
    """nodes是途中节点的列表;edges是一个字典，将每个节点映射到其子节点列表"""
    def __init__(self):
        self.nodes = []
        self.edges = {}

    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.append(node)
            self.edges[node] = []

    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)

    def childrenOf(self, node):
        return self.edges[node]

    def hasNode(self, node):
        return node in self.nodes

    def __str__(self):
        result = ''
        for src in self.nodes:
            for dest in self.edges[src]:
                result = result + src.getName() + '->'\
                    + dest.getName() + '\n'
        return result[:-1]


class Graph(Digraph):

    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)


def printPath(path):
    """假设path是节点列表"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result


def DFS(graph, start, end, path, shortTest, toPrint=False):
    """假设graph是无向图，start和end是节点，path和shortTest是节点列表
    返回graph中从start到end的最短路径
    深度优先搜索"""
    path = path + [start]
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path:
            if shortTest is None or len(path) < len(shortTest):
                newPath = DFS(graph, node, end, path, shortTest, toPrint)
                if newPath is not None:
                    shortTest = newPath
    return shortTest


def shortTestPath(graph, start, end, toPrint=False):
    return DFS(graph, start, end, [], None, toPrint)


def BFS(graph, start, end):
    """广度优先搜索"""
    initPath = [start]
    pathQueue = [initPath]
    while len(pathQueue) != 0:
        tmpPath = pathQueue.pop(0)
        print('Current BFS path:', printPath(tmpPath))
        lastNode = tmpPath[-1]
        if lastNode == end:
            return tmpPath
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath:
                nextPath = tmpPath + [nextNode]
                pathQueue.append(nextPath)
    return None


def testSP():
    nodes = []
    for name in range(6):
        nodes.append(Node(str(name)))
    g = Digraph()
    for n in nodes:
        g.addNode(n)
    g.addEdge(Edge(nodes[0], nodes[1]))
    g.addEdge(Edge(nodes[0], nodes[2]))
    g.addEdge(Edge(nodes[1], nodes[0]))
    g.addEdge(Edge(nodes[1], nodes[2]))
    g.addEdge(Edge(nodes[2], nodes[3]))
    g.addEdge(Edge(nodes[2], nodes[4]))
    g.addEdge(Edge(nodes[3], nodes[4]))
    g.addEdge(Edge(nodes[3], nodes[5]))
    g.addEdge(Edge(nodes[4], nodes[0]))
    sp = shortTestPath(g, nodes[0], nodes[5], toPrint=True)
    print('ShortTest path Fount By DFS:', printPath(sp))
    sp = BFS(g, nodes[0], nodes[5])
    print('ShortTest path found By BFS:', printPath(sp))


testSP()

