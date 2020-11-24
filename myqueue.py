class queue:
    def __init__(self):
        self.content = []

    def add(self, item):
        self.content.append(item)

    def pop(self):
        return self.content.pop(0)

    def size(self):
        return len(self.content)

    def __str__(self):
        return str(self.content)


if __name__ == "__main__":
    q = queue()
    q.add('test')
    q.add('secondary')
    q.add('third')
    print(q)
    print(q.pop())
    print(q)
    print(q.pop())
    print(q)
    print(q.pop())
    print(q)
