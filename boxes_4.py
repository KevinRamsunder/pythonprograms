# boxes_3
# Making MAP2 like it is
# FOR 13 VARIABLES of map2_4.py

import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import random
import time


def generate_marker_size_array(z_2d_array):
    marker_size_matrix = [[0 for j in range(len(z_2d_array[i]))] for i in range(len(z_2d_array))]
    for i in range(len(z_2d_array)):
        for j in range(len(z_2d_array[i])):
            marker_size_matrix[i][j] = calculate_marker_size(j, z_2d_array[i])
    return marker_size_matrix


def calculate_marker_size(marker, zin):
    maxz = max(np.abs(zin))
    msz = abs(zin[marker]) * 40 / maxz
    msz = max(msz, 2.)
    return msz


def perp2(vxin, vyin):
    if vxin == 0:
        vxp = -np.sign(vyin) * abs(vyin) * 2
        vyp = 0.
    else:
        vyp = np.sign(vxin) * 1.0 / np.sqrt(1 + vyin ** 2 / vxin ** 2)
        vxp = -np.sign(vyin) * abs(vyin * vyp / vxin)
    return vxp, vyp


def animate(i, ax, z_2d_arr, msize_matrix, xp_arr, yp_arr, hold_value, variable_names, cin_nparray, step):
    if i < hold_value:
        return ax

    i -= hold_value
    i *= step

    # clear between frames
    ax.clear()

    # reset axes values
    ax.axis([-1.25, 1.25, -1.25, 1.25])
    ax.axis('off')
    ax.set_aspect('equal')
    ax.text(-1.25, 1.25, "Time: {} / {}".format(i, len(z_2d_arr)))

    for marker in range(len(z_2d_arr[i])):
        marker_size = msize_matrix[i][marker]

        symbol = 'o'
        if marker == 0:
            symbol = 's'
        marker_color = 'k'
        if z_2d_arr[i][marker] < 0:
            marker_color = 'r'
        elif z_2d_arr[i][marker] > 0:
            marker_color = 'g'

        ax.plot(xp_arr[marker], yp_arr[marker], symbol, ms=marker_size, c=marker_color, markeredgewidth=2.,
                markerfacecolor="none", markeredgecolor=marker_color)

        if xp_arr[marker] < 0:
            halign = 'right'
        elif xp_arr[marker] >= 0:
            halign = 'left'

        if marker != 0:
            ax.text(xp_arr[marker] + .1, yp_arr[marker] + 0.07, variable_names[marker], horizontalalignment=halign)
        else:
            ax.text(xp_arr[marker] + .2, yp_arr[marker] + 0.07, variable_names[marker])

    if i >= len(z_2d_arr) - 2:
        numc = len(cin_nparray)
        for i in range(numc):
            # plot the connections (arrows)
            for j in range(numc):
                if np.abs(cin_nparray[j][i]) > .1:
                    width = abs(cin_nparray[j][i]) / 2.
                    # print ('\nwidth= ',width)
                    dxp = (xp_arr[j] - xp_arr[i]) * 0.9
                    dyp = (yp_arr[j] - yp_arr[i]) * 0.9
                    dxshift, dyshift = perp2(dxp, dyp)
                    if cin_nparray[j][i] < 0:
                        arrow_color = 'r'
                    else:
                        arrow_color = 'g'
                    roff = 0.03
                    xoff = dxshift * roff
                    yoff = dyshift * roff
                    xpastart = xp_arr[i] + xoff
                    ypastart = yp_arr[i] + yoff
                    ax.arrow(xpastart, ypastart, dxp, dyp, head_width=0.05,
                             head_length=0.1, fc=arrow_color, ec=arrow_color, linewidth=width)

    # clear for next iteration
    return ax


def boxplot(cin, zin, programnamein):
    # set up only for THESE names
    vname = ['1-NODAL (+/-)',
             '2 +memory',
             '3 -memory',
             '4 +expect',
             '5 - expect',
             '6-Coop/Compete',
             '7-Conlf Manag',
             '8-Fairness',
             '9-Access',
             '10-Security',
             '11-Higher Authority',
             '12-Peace Vision',
             '13-Shared Ident']
    numc = len(cin)
    if numc > 13:
        print('\nSORRY, I cannot make a clockplot for more than 13 variables')
        return

    # plot the variables
    radius = 1.
    pi = np.pi
    #     for i in range(numc):
    #         angle=i*pi/(6.5)
    #         xp[i]=radius*np.sin(angle)
    #         yp[i]=radius*np.cos(angle)
    #     print (xp)
    xp = [0., -.5, -.5, .5, .5, -.1, .1, -1., -1., -.5, 0., .6, 1.]
    yp = [0., .25, -.25, .25, -.25, .5, -.5, .35, -.35, -.6, 1., .5, 0.]
    xpa = np.array(xp)
    ypa = np.array(yp)

    fig = plt.figure()
    fig.patch.set_facecolor('white')

    ax = fig.add_subplot(111)
    ax.axis([-1.25, 1.25, -1.25, 1.25])
    ax.axis('off')
    ax.set_aspect('equal')
    ax.set_axis_bgcolor('white')

    ax1 = fig.add_subplot(111)
    ax1.axis([-1.25, 1.25, -1.25, 1.25])
    ax1.axis('off')
    ax1.set_aspect('equal')
    ax1.set_axis_bgcolor('white')

    cina = np.array(cin)

    for i in range(numc):
        # plot the connections (arrows)
        for j in range(numc):
            if np.abs(cina[j][i]) > .1:
                width = abs(cina[j][i]) / 2.
                # print ('\nwidth= ',width)
                dxp = (xpa[j] - xpa[i]) * 0.9
                dyp = (ypa[j] - ypa[i]) * 0.9
                dxshift, dyshift = perp2(dxp, dyp)
                if cina[j][i] < 0:
                    arrow_color = 'r'
                else:
                    arrow_color = 'g'
                roff = 0.03
                xoff = dxshift * roff
                yoff = dyshift * roff
                xpastart = xpa[i] + xoff
                ypastart = ypa[i] + yoff
                # print ('\nijxy= ',i,j,xpastart, ypastart)

                ax.arrow(xpastart, ypastart, dxp, dyp, head_width=0.05,
                         head_length=0.1, fc=arrow_color, ec=arrow_color, linewidth=width)

                if xpa[i] < 0:
                    halign = 'right'
                else:
                    halign = 'left'
                if i != 0:
                    plt.text(xpa[i] + .1, ypa[i] + 0.07, vname[i], horizontalalignment=halign)
                else:
                    plt.text(xpa[i] + .2, ypa[i] + 0.07, vname[i])

    pname = programnamein
    plt.title(pname, fontsize=12)

    step = 50
    hold_value = 250
    marker_sizes = generate_marker_size_array(zin)
    anim = animation.FuncAnimation(fig, animate, frames=int((len(zin) + hold_value)/step),
                                   fargs=(ax, zin, marker_sizes, xpa, ypa, hold_value, vname, cina, step),
                                   interval=1, blit=False, repeat=False)

    plt.show()
    return

# THIS IS THE TEST RUN
# pprogamename='boxTEST'
# boxplot(ccin,zzin,pprogamename)
