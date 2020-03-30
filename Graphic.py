from Model import Model
from graphics import *
import numpy as np
from sklearn.preprocessing import minmax_scale

zbufer = np.zeros((1000, 1000))

def open_file():
    f = open('stanford_bunny/stanford-bunny.obj', 'r')
    print('Started reading file')
    for line in f:
        if line.startswith('v '):
            parts = line.split(' ')
            model.addPoint([int(float(parts[1]) * 6000 + 500),
                            int(-float(parts[2]) * 6000 + 800),
                            int(float(parts[3].split('\n')[0]) * 6000 + 500)])
        if line.startswith('f '):
            parts = line.split(' ')
            model.addPolygon(
                [int(parts[1].split('/')[0]) - 1, int(parts[2].split('/')[0]) - 1, int(parts[3].split('/')[0]) - 1])
    print('Finished reading file')


def draw_line(x1, y1, x2, y2, color):
    change = False
    if np.abs(x2 - x1) < np.abs(y2 - y1):
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        change = True
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    dx = x2 - x1
    y = y1
    if y2 > y1:
        step_y = 1
    else:
        step_y = -1
    derror = 2 * np.abs(y2 - y1)
    dsum = 0
    for x in range(x1, x2):
        if change:
            win.plot(y, x, color)
        else:
            win.plot(x, y, color)
        dsum += derror
        if dsum > dx:
            dsum -= 2 * dx
            y += step_y


def draw_points():
    print('Started drawing points')
    for i in range(0, model.pointsLen()):
        pt = model.getPoint(i)
        win.plot(pt[0], pt[1])
    print('Finished drawing points')


def rect(x1, x2, y1, y2):
    points = []
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            points.append([i, j])
    return points


def fillPolygon(pt1, pt2, pt3, color):
    xs = [pt1[0], pt2[0], pt3[0]]
    xs.sort()
    ys = [pt1[1], pt2[1], pt3[1]]
    ys.sort()
    interes = rect(xs[0], xs[2], ys[0], ys[2])
    for point in interes:
        if barycentric(pt1, pt2, pt3, point[0], point[1]):
            win.plot(point[0], point[1], color)


def zb(x, y, z):
    if zbufer[x][y] < z:
        zbufer[x][y] = z
        return True
    else:
        return False


def barycentric(pt1, pt2, pt3, x, y):
    x0 = pt1[0]
    x1 = pt2[0]
    x2 = pt3[0]
    y0 = pt1[1]
    y1 = pt2[1]
    y2 = pt3[1]
    if ((y0 - y2) * (x1 - x2) - (x0 - x2) * (y1 - y2)) != 0:
        bar1 = ((y - y2) * (x1 - x2) - (x - x2) * (y1 - y2)) / ((y0 - y2) * (x1 - x2) - (x0 - x2) * (y1 - y2))
    else:
        bar1 = -1

    if ((y1 - y0) * (x2 - x0) - (x1 - x0) * (y2 - y0)) != 0:
        bar2 = ((y - y0) * (x2 - x0) - (x - x0) * (y2 - y0)) / ((y1 - y0) * (x2 - x0) - (x1 - x0) * (y2 - y0))
    else:
        bar2 = -1

    if ((y2 - y1) * (x0 - x1) - (x2 - x1) * (y0 - y1)) != 0:
        bar3 = ((y - y1) * (x0 - x1) - (x - x1) * (y0 - y1)) / ((y2 - y1) * (x0 - x1) - (x2 - x1) * (y0 - y1))
    else:
        bar3 = -1

    if (bar1 <= 0) or (bar2 <= 0) or (bar3 <= 0):
        return False
    else:
        if zb(x, y, bar1 * pt1[2] + bar2 * pt2[2] + bar3 * pt3[2]):
            return True
        else:
            return False


def isPolygonVisible(p0, p1, p2):
    x02 = p0[0] - p2[0]
    x20 = -x02
    x10 = p1[0] - p0[0]

    y02 = p0[1] - p2[1]
    y20 = -y02
    y10 = p1[1] - p0[1]

    z02 = p0[2] - p2[2]
    z20 = -z02
    z10 = p1[2] - p0[2]

    length = np.sqrt(
        np.power(y20 * z10 - z20 * y10, 2) +
        np.power(z20 * x10 - x20 * z10, 2) +
        np.power(x20 * y10 - x10 * y20, 2)
    )

    normal = [
        (y20 * z10 - z20 * y10)/length,
        (z20 * x10 - x20 * z10)/length,
        (x20 * y10 - x10 * y20)/length
    ]

    if normal[2] < 0:
        return False
    else:
        return normal[2] * -1

def draw_polygons():
    print('Started drawing polygons')
    for pg in model.getPolygons():
        pt1 = model.getPoint(pg[0])
        pt2 = model.getPoint(pg[1])
        pt3 = model.getPoint(pg[2])
        bright = isPolygonVisible(pt1, pt2, pt3)
        if bright:
            if not np.isnan(bright):
                color = color_rgb(int(np.abs(bright)*255), int(np.abs(bright)*255), int(np.abs(bright)*255))
            else:
                color = color_rgb(255, 255, 255)
            draw_line(pt1[0], pt1[1], pt2[0], pt2[1], color)
            draw_line(pt2[0], pt2[1], pt3[0], pt3[1], color)
            draw_line(pt1[0], pt1[1], pt3[0], pt3[1], color)
            fillPolygon(pt1, pt2, pt3, color)
    print('Finished drawing polygons')


model = Model()

win = GraphWin("Картинка", 1000, 1000)
win.autoflush = False

open_file()
draw_points()
draw_polygons()

win.flush()
win.getMouse()
