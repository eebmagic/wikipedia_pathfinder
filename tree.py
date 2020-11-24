from myqueue import queue

class node:
    def __init__(self, data):
        self.data = data
        self.children = set()
        self.parent = None

    def setParent(self, parentNode):
        self.parent = parentNode

    def getParent(self):
        return self.parent

    def addChildren(self, newChildren):
        if type(newChildren) in [set, list, tuple]:
            for x in newChildren:
                self.children.add(x)
        else:
            self.children.add(newChildren)

    def removeChild(self, target, verbose=True):
        if target in self.children:
            self.children.remove(target)
        elif verbose:
            print(f"{target=} was not in the node's children")

    def getChildren(self):
        return self.children

    def getData(self):
        return self.data

    def setData(self, newData):
        self.data = newData

    def __str__(self):
        return f"data: {self.data} - children: {self.children}"


class tree:
    def __init__(self, headNode):
        self.head = headNode

    def bfs(self, target):
        q = queue()
        q.add(self.head)

        while q.size() != 0:
            curr = q.pop()
            if curr.getData() == target or curr == target:
                return curr
            else:
                for child in curr.getChildren():
                    q.add(child)

        return False

    def add(self, newNode, targetParent):
        if type(targetParent) == node:
            targetParent.addChildren(newNode)
            newNode.setParent(targetParent)
        else:
            parent = self.bfs(targetParent)
            if parent:
                parent.addChildren(newNode)
                newNode.setParent(parent)
            else:
                print("the given target parent was not found in the tree")

    def getPath(self, startNode):
        path = [startNode.getData()]
        curr = startNode
        while curr != None:
            if curr.getParent():
                path.append(curr.getParent().getData())
            curr = curr.getParent()

        path = path[::-1]
        return path

    def getHead(self):
        return self.head


if __name__ == "__main__":
    # n = node("Contents")
    # n.addChildren("FIRST")
    # print(n)

    # others = ['these', 'are', 'more', 'contents']
    # s = set()
    # for x in others:
    #     s.add(x)

    # n.addChildren(s)
    # print(n)
    
    a = node("A")
    b = node("B")
    c = node("C")
    t = tree(a)

    t.add(b, a)
    t.add(c, a)
    t.add(c, 'A')

    print(f"head: {t.getHead()}")
    for child in t.getHead().getChildren():
        print(f"child: {child}")