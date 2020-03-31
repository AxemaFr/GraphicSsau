from Model import Model
from graphics import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import *

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


def draw_textured_pix(point, coords, texture, bright):
    if type(coords) != bool:
        for item in coords:
            if np.isnan(item):
                coords = [1, 1]
    r = int(texture[int(coords[0] * 511), int(coords[1] * 511), 0] * 255 * bright)
    g = int(texture[int(coords[0] * 511), int(coords[1] * 511), 1] * 255 * bright)
    b = int(texture[int(coords[0] * 511), int(coords[1] * 511), 2] * 255 * bright)

    if r>255:
        r = 255
    if g>255:
        g = 255
    if b>255:
        b = 255

    color = color_rgb(r, g, b)
    win.plot(point[0], point[1], color)


def open_texture():
    texture = plt.imread('stanford_bunny/negz.png')
    return texture

def draw_line(x1, y1, x2, y2, bright, pt1, pt2, pt3, texture):
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
            coords = barycentric(pt1, pt2, pt3, y, x, False, True)
            if type(coords) != bool:
                draw_textured_pix([y, x], coords, texture, bright)
        else:
            coords = barycentric(pt1, pt2, pt3, x, y, False, True)
            if type(coords) != bool:
                draw_textured_pix([x, y], coords, texture, bright)
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


def fillPolygon(pt1, pt2, pt3, bright, texture):
    xs = [pt1[0], pt2[0], pt3[0]]
    xs.sort()
    ys = [pt1[1], pt2[1], pt3[1]]
    ys.sort()
    interes = rect(xs[0], xs[2], ys[0], ys[2])
    for point in interes:
        brightTemp = bright
        coords = barycentric(pt1, pt2, pt3, point[0], point[1], False, False)
        if np.isnan(bright):
            brightTemp = 1
        if type(coords) != bool:
            draw_textured_pix(point, coords, texture, np.abs(brightTemp))




def zb(x, y, z):
    if zbufer[x][y] < z:
        zbufer[x][y] = z
        return True
    else:
        return False


def barycentric(pt1, pt2, pt3, x, y, zbonly, coords):
    x0 = pt1[0]
    x1 = pt2[0]
    x2 = pt3[0]
    y0 = pt1[1]
    y1 = pt2[1]
    y2 = pt3[1]
    if ((y0 - y2) * (x1 - x2) - (x0 - x2) * (y1 - y2)) != 0:
        bar1 = ((y - y2) * (x1 - x2) - (x - x2) * (y1 - y2)) / ((y0 - y2) * (x1 - x2) - (x0 - x2) * (y1 - y2))
    else:
        bar1 = 10000

    if ((y1 - y0) * (x2 - x0) - (x1 - x0) * (y2 - y0)) != 0:
        bar2 = ((y - y0) * (x2 - x0) - (x - x0) * (y2 - y0)) / ((y1 - y0) * (x2 - x0) - (x1 - x0) * (y2 - y0))
    else:
        bar2 = 10000

    if ((y2 - y1) * (x0 - x1) - (x2 - x1) * (y0 - y1)) != 0:
        bar3 = ((y - y1) * (x0 - x1) - (x - x1) * (y0 - y1)) / ((y2 - y1) * (x0 - x1) - (x2 - x1) * (y0 - y1))
    else:
        bar3 = 10000

    if zbonly:
        if zb(x, y, bar1 * pt1[2] + bar2 * pt2[2] + bar3 * pt3[2]):
            return True
        else:
            return False

    if coords:
        if zb(x, y, bar1 * pt1[2] + bar2 * pt2[2] + bar3 * pt3[2]):
            #arr = [int(bar1 * pt1[0] + bar2 * pt2[0] + bar3 * pt3[0]), int(bar1 * pt1[1] + bar2 * pt2[1] + bar3 * pt3[1])]
            arr = [bar1, bar2]
            normArr = arr / np.linalg.norm(arr)
            return normArr
        else:
            return False

    if (bar1 <= 0) or (bar2 <= 0) or (bar3 <= 0):
        return False

    if zb(x, y, bar1 * pt1[2] + bar2 * pt2[2] + bar3 * pt3[2]):
        arr = [int(bar1 * pt1[0] + bar2 * pt2[0] + bar3 * pt3[0]), int(bar1 * pt1[1] + bar2 * pt2[1] + bar3 * pt3[1])]
        normArr = arr/np.linalg.norm(arr)
        return normArr
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

    if normal[2] <= 0:
        return False
    else:
        return normal[2] * -1

def draw_polygons():
    print('Started drawing polygons')
    texture = open_texture()
    lastgoodbright = 0
    for pg in model.getPolygons():
        pt1 = model.getPoint(pg[0])
        pt2 = model.getPoint(pg[1])
        pt3 = model.getPoint(pg[2])
        bright = np.abs(isPolygonVisible(pt1, pt2, pt3))
        if bright:
            if np.isnan(bright):
                bright = lastgoodbright
            else:
                lastgoodbright = bright

            draw_line(pt1[0], pt1[1], pt2[0], pt2[1], bright, pt1, pt2, pt3, texture)
            draw_line(pt2[0], pt2[1], pt3[0], pt3[1], bright, pt1, pt2, pt3, texture)
            draw_line(pt1[0], pt1[1], pt3[0], pt3[1], bright, pt1, pt2, pt3, texture)
            fillPolygon(pt1, pt2, pt3, bright, texture)
    print('Finished drawing polygons')


model = Model()

win = GraphWin("Картинка", 800, 800)
win.autoflush = False

open_file()
open_texture()
draw_points()
draw_polygons()
print('Started final render')
win.flush()
print('Finished final render')
win.getMouse()
