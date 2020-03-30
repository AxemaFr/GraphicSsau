from Model import Model
from graphics import *
import numpy as np
from sklearn.preprocessing import minmax_scale


def open_file():
    f = open('file.obj', 'r')
    print('Started reading file')
    for line in f:
        if line.startswith('v '):
            parts = line.split(' ')
            model.addPoint([int(float(parts[1]) * 4000 + 500),
                            int(-float(parts[2]) * 4000 + 500),
                            int(float(parts[3].split('\n')[0]) * 4000 + 500)])
        if line.startswith('f '):
            parts = line.split(' ')
            model.addPolygon(
                [int(parts[1].split('/')[0]) - 1, int(parts[2].split('/')[0]) - 1, int(parts[3].split('/')[0]) - 1])
    print('Finished reading file')


def draw_line(x1, y1, x2, y2):
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
            win.plot(y, x)
        else:
            win.plot(x, y)
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
        return True


def isPolygonVisible(pt1, pt2, pt3):
    n = [0, 0, 0]
    Vx = pt3[0] - pt1[0]
    Vy = pt3[1] - pt1[1]
    Vz = pt3[2] - pt1[2]
    Ux = pt2[0] - pt1[0]
    Uy = pt2[1] - pt1[1]
    Uz = pt2[2] - pt1[2]
    n[0] = Vy * Uz - Vz * Uy
    n[1] = Vz * Ux - Vx * Uz
    n[2] = Vx * Uy - Vy * Ux
    nNorm = np.linalg.norm(n)
    v = [1, 1, -1]
    vNorm = np.linalg.norm(v)
    cos = (n[0] * v[0] + n[1] * v[1] + n[2] * v[2]) / (nNorm * vNorm)
    if n[2] > 0:
        return False
    else:
        return n[2] * -1
    # if cos > 0:
    # return False
    # else:
    # return True


def draw_polygons():
    print('Started drawing polygons')
    for pg in model.getPolygons():
        pt1 = model.getPoint(pg[0])
        pt2 = model.getPoint(pg[1])
        pt3 = model.getPoint(pg[2])
        bright = isPolygonVisible(pt1, pt2, pt3)
        if bright:
            draw_line(pt1[0], pt1[1], pt2[0], pt2[1])
            draw_line(pt2[0], pt2[1], pt3[0], pt3[1])
            draw_line(pt1[0], pt1[1], pt3[0], pt3[1])
            fillPolygon(pt1, pt2, pt3, color_rgb(int(np.abs(bright)*255), int(np.abs(bright)*255), int(np.abs(bright)*255)))
    print('Finished drawing polygons')


model = Model()

win = GraphWin("Картинка", 1000, 1000)
win.autoflush = False

open_file()
draw_points()
draw_polygons()

win.flush()
win.getMouse()
