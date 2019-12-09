class IntSet(object):
    """IntSet是一个整数集合"""

    def __init__(self):
        """创建一个空的整数集合"""
        self.values = []

    def insert(self, e):
        """假设e是整数，插入到self中"""
        if e not in self.values:
            self.values.append(e)

    def member(self, e):
        """假设e是整数，如果在self中则返回true"""
        return e in self

    def remove(self, e):
        """假设e是整数，从self中删除e，如果失败则抛出异常"""
        try:
            self.values.remove(e)
        except ValueError:
            raise ValueError(str(e), 'not found')

    def getMembers(self):
        """返回self列表"""
        return self.values[:]

    def __str__(self):
        """返回一个表示self的字符串"""
        self.values.sort()
        result = ''
        for e in self.values:
            result = result + str(e) + ','
        return '{' + result[:-1] + '}'
