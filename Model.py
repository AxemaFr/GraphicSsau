class Model:
    def __init__(self):
        self.points = []

    def getPoint(self, index):
        return self.points[index]

    def addPoint(self, point):
        self.points.append(point)

    def len(self):
        return len(self.points)
