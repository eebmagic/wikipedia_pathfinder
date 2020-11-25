class queue:
    def __init__(self):
        self.content = []

    def add(self, item, score):
        if len(self.content) == 0:
            self.content.append((item, score))
            return

        for ind, point in enumerate(self.content):
            existingItem, existingScore = point
            if existingScore < score:
                self.content.insert(ind, (item, score))
                break

        # if len(self.content) % 10 == 0:
        #     print(self)

    def pop(self):
        item, score = self.content.pop(0)
        return item

    def size(self):
        return len(self.content)

    def __str__(self):
        if type(self.content[0][0]) == str:
            return str(self.content)
        else:
            out = []
            for item, score in self.content:
                out.append((item.getData().split('/')[-1], score))
            return str(out)


if __name__ == "__main__":
    q = queue()
    q.add('test', 0)
    q.add('secondary', 2)
    q.add('third', 1)
    print(q)
    print(q.pop())
    print(q)
    print(q.pop())
    print(q)
    print(q.pop())
    print(q)
