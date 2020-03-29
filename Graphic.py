from Model import Model
from graphics import *
import numpy as np


def open_file():
    f = open('file.obj', 'r')
    for line in f:
        if line.startswith('v '):
            parts = line.split(' ')
            model.addPoint([int(float(parts[1]) * 8000 + 500),
                            int(-float(parts[2]) * 8000 + 700),
                            int(float(parts[3].split('\n')[0]) * 10000) + 1000])
        if line.startswith('f '):
            parts = line.split(' ')
            model.addPolygon(
                [int(parts[1].split('/')[0]) - 1, int(parts[2].split('/')[0]) - 1, int(parts[3].split('/')[0]) - 1])


def draw_line(x1, y1, x2, y2, wind):
    points = []
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
            points.append([y, x])
        else:
            points.append([x, y])
        dsum += derror
        if dsum > dx:
            dsum -= 2 * dx
            y += step_y

    for item in points:
        pnt = Point(item[0], item[1])
        pnt.draw(wind)
    return points


def draw_points():
    for i in range(0, model.pointsLen()):
        pt = model.getPoint(i)
        point = Point(pt[0], pt[1])
        point.draw(win)


def barycentric(pt1, pt2, pt3, x, y):
    x0 = pt1[0]
    x1 = pt2[0]
    x2 = pt3[0]
    y0 = pt1[1]
    y1 = pt2[1]
    y2 = pt3[1]
    bar1 = ((y - y2)(x1 - x2) - (x - x2)(y1 - y2)) / ((y0 - y2)(x1 - x2) - (x0 - x2)(y1 - y2))
    bar2 = ((y - y0)(x2 - x0) - (x - x0)(y2 - y0)) / ((y1 - y0)(x2 - x0) - (x1 - x0)(y2 - y0))
    bar3 = ((y - y1)(x0 - x1) - (x - x1)(y0 - y1)) / ((y2 - y1)(x0 - x1) - (x2 - x1)(y0 - y1))

    if (bar1 < 0) or (bar2 < 0) or (bar3 < 0):
        return False
    else:
        return True



def draw_polygons():
    for pg in model.getPolygons():
        pt1 = model.getPoint(pg[0])
        pt2 = model.getPoint(pg[1])
        pt3 = model.getPoint(pg[2])
        draw_line(pt1[0], pt1[1], pt2[0], pt2[1], win)
        draw_line(pt2[0], pt2[1], pt3[0], pt3[1], win)
        draw_line(pt1[0], pt1[1], pt3[0], pt3[1], win)


model = Model()

win = GraphWin("Картинка", 1000, 1000)

open_file()
draw_points()
draw_polygons()

win.getMouse()
