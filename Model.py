class Model:
    def __init__(self):
        self.points = []
        self.polygons = []

    def getPoint(self, index):
        return self.points[index]

    def addPoint(self, point):
        self.points.append(point)

    def pointsLen(self):
        return len(self.points)

    def addPolygon(self, polygon):
        self.polygons.append(polygon)

    def polygonLen(self):
        return len(self.polygons)

    def getPolygons(self):
        return self.polygons

    def clear(self):
        self.points = []
        self.polygons = []

