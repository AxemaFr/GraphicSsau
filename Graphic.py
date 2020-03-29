from Model import Model
from graphics import *

f = open('file.obj', 'r')

model = Model()
for line in f:
    if line.startswith('v '):
        parts = line.split(' ')
        model.addPoint([parts[1], parts[2], parts[3].split('\n')[0]])

win = GraphWin("Картинка", 1000, 1000)

for i in range(1, model.len()):
    pt = model.getPoint(i)
    point = Point(float(pt[0])*4000 + 500, -float(pt[1])*4000 + 500)
    point.draw(win)

win.getMouse()
win.close()
