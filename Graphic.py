from Model import Model
from graphics import *

f = open('file.obj', 'r')

model = Model()
for line in f:
    if line.startswith('v '):
        parts = line.split(' ')
        model.addPoint([parts[1], parts[2], parts[3].split('\n')[0]])

print(model.getPoint(15))
#OUTPUT: ['-0.044835', '0.047895', '0.000493']
# win = GraphWin("Картинка", 400, 400)
# win.getMouse()
# win.close()
