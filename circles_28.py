# circles_28 - NEXT
# FOR 13 VARIABLES of map2_4.py

import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import random
import time

outer_index = -2  # Must be -2 since 'i' is not incremented at first run of animate


def perp(vxin, vyin):
    if vxin == 0:
        vxp = -np.sign(vyin) * vyin
        vyp = 0.
    else:
        vyp = np.sign(vxin) * 1.0 / np.sqrt(1 + vyin ** 2 / vxin ** 2)
        vxp = -np.sign(vyin) * abs(vyin * vyp / vxin)
    return vxp, vyp


# -------------------------------------------------------------------------

# NEED TO CHANGE THIS LATER
# numc = 8
# cin = [[0, 3, -6, 3, 3, 3, 0, 0], [3, 0, 0, 0, 0, 0, 0, 3], [-3, 0, 0, 0, 0, 0, 0, -3], [3, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 3, -6, 0, 0, 0, 0, 0]]
# zin = [13.31636449,   6.65819304,   0.,   3.33333333, 3.33333333, 6.65819304, 3.33332235, 3.33332235]


def clockplot(cin, zin, programnamein):
    # set up only for THESE names
    vname = ['1-NODAL (+/-)',
             '2-POSITIVE memory',
             '3-NEGATIVE memory',
             '4-POSITIVE expect',
             '5-NEGATIVE expect',
             '6-Coop/Compete',
             '7-Conlf Manag',
             '8-Fairness',
             '9-Access',
             '10-Security',
             '11-Higher Authority',
             '12-Peace Vision',
             '13-Shared Ident'
             ]
    numc = len(cin)
    if numc > 13:
        print('\nSORRY, I cannot make a clockplot for more than 13 variables')
        return

    # plot the variables
    radius = 1.
    pi = np.pi
    xp = []
    yp = []
    for i in range(numc):
        angle = i * pi / 6.5
        xp.append(radius * np.sin(angle))
        yp.append(radius * np.cos(angle))
    xp_array = np.array(xp)
    yp_array = np.array(yp)
    fig = plt.figure()
    # plt.axes([.1,.1,.7,.7])
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    fig.patch.set_facecolor('white')
    ax.set_axis_bgcolor('white')

    for i in range(numc):
        # Creates circles (or square)
        maxz = max(np.abs(zin))
        msz = abs(zin[i]) * 40 / maxz
        if msz < 2:
            msz = 2.
        symbol = 'o'
        if i == 0:
            symbol = 's'
        varc = 'k'
        if zin[i] < 0:
            varc = 'r'
        elif zin[i] > 0:
            varc = 'g'
        # else:
        #             varc='g'
        ax.plot(xp_array[i], yp_array[i], symbol, ms=msz, c=varc, markeredgewidth=2.0,
                markerfacecolor='none', markeredgecolor=varc)
        if i != 0:
            ax.text(xp_array[i] + .1, yp_array[i] - 0.07, vname[i])
        else:
            ax.text(xp_array[i] + .2, yp_array[i] + 0.07, vname[i])
    ax.axis([-1.25, 1.25, -1.25, 1.25])
    ax.axis('off')

    # plot the connections
    cina = np.array(cin)
    counter = 0
    for i in range(2):
        for j in range(2):
            pass
            # if np.abs(cina[j][i]) > .1:
            #     width = abs(cina[j][i]) / 2.
            #     # print ('\nwidth= ',width)
            #     dxp = (xp_array[j] - xp_array[i]) * 0.9
            #     dyp = (yp_array[j] - yp_array[i]) * 0.9
            #     dxshift, dyshift = perp(dxp, dyp)
            #     if cina[j][i] < 0:
            #         arrow_color = 'r'
            #     else:
            #         arrow_color = 'g'
            #     roff = 0.03
            #     xoff = dxshift * roff
            #     yoff = dyshift * roff
            #     xpastart = xp_array[i] + xoff
            #     ypastart = yp_array[i] + yoff
            #     # print ('\nijxy= ',i,j,xpastart, ypastart)
            #     ax.arrow(xpastart, ypastart, dxp, dyp, head_width=0.05,
            #              head_length=0.1, fc=arrow_color, ec=arrow_color, linewidth=width)
            #     localtime = time.asctime( time.localtime(time.time()) )
            #     programname='peace_20.py   '+localtime
    pname = programnamein
    plt.title(pname, fontsize=12)
    anim = animation.FuncAnimation(fig, animate, frames=numc ** 2, fargs=(ax, cin, xp_array, yp_array), interval=1,
                                   blit=False, repeat=False)
    plt.show()


counter = 0


def animate(i, ax, cin, xp_array, yp_array):
    global outer_index, counter
    inner_index = i % len(cin)

    if i % 13 == 0:
        outer_index += 1
        print("i: {}".format(i))
    print("Outer index: {}, inner index: {}, i: {}".format(outer_index, inner_index, i))
    cina = np.array(cin)
    if np.abs(cina[outer_index][inner_index]) > .1:
        width = abs(cina[outer_index][inner_index]) / 2.
        # print ('\nwidth= ',width)
        dxp = (xp_array[outer_index] - xp_array[inner_index]) * 0.9
        dyp = (yp_array[outer_index] - yp_array[inner_index]) * 0.9
        dxshift, dyshift = perp(dxp, dyp)
        if cina[outer_index][inner_index] < 0:
            arrow_color = 'r'
        else:
            arrow_color = 'g'
        roff = 0.03
        xoff = dxshift * roff
        yoff = dyshift * roff
        xpastart = xp_array[inner_index] + xoff
        ypastart = yp_array[inner_index] + yoff
        # print ('\nijxy= ',i,j,xpastart, ypastart)
        ax.arrow(xpastart, ypastart, dxp, dyp, head_width=0.05,
                 head_length=0.1, fc=arrow_color, ec=arrow_color, linewidth=width)
        print("{}".format(counter))
        counter += 1
