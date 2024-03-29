# map2_5.py
# starting Peter's 2015-07-18 MAP with 13 variables

# ***NB***
# REPLACED NODAL,+/- RESERVOIRS, +/- FUTURE AS VARIABLES 1,2,3,4
# AND +/- RESERVOIRS, +/- FUTURE ==0 IF <0
# ***NB***

# STARTING TO USE BETTER PLOT/COLORS FROM peace_11
# note: c(i,j) is effect of j on i



import math
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import random
import time
from circles_28 import *


def filein(fname):
    numlines = 0
    xin = []
    f = open(fname, 'r')
    for line in f:
        # print (line, end='')
        xin.append(line)
        numlines += 1
    f.close()
    return xin, numlines


def fileout(filename, filedata):
    f2 = open(filename, 'w')
    f2.write(filedata)
    f2.close()


def getxy(fname):
    data, numlines = filein(fname)
    #    dataline=['0' for i in range(numlines)]
    x = ['0' for i in range(numlines)]
    y = ['0' for i in range(numlines)]
    for i in range(numlines):
        xline = data[i]
        xline2 = xline.split('\t')
        xline2[-1] = xline2[-1].replace('\n', '')
        # print ('\nxline2',xline2)
        x[i] = eval(xline2[0])
        y[i] = eval(xline2[1])
    return x, y, numlines


def getx(fname):
    data, numlines = filein(fname)
    # print ('\ndata\n',data,'\nlines',numlines)
    x = ['0' for i in range(numlines)]
    for i in range(numlines):
        x[i] = data[i].replace('\n', '')
        x[i] = eval(x[i])
    return x, numlines


def getxn(fname):
    data, numlines = filein(fname)
    # print (numlines)
    # print (data)
    dataline = ['0' for i in range(numlines)]
    for i in range(numlines):
        x = data[i]
        y = x.split('\t')
        y[-1] = y[-1].replace('\n', '')
        dataline[i] = y
    # print ('\n\nascii-input',dataline)
    xdata = dataline[:]
    for i in range(numlines):
        inline = len(dataline[i])
        for j in range(inline):
            if xdata[i][j] != '':
                xdata[i][j] = eval(xdata[i][j])
            else:
                xdata[i][j] = None
    # print ('dataline',dataline)
    # print ('xdata',xdata)
    return xdata, numlines


# -------------------------------------------------------------------------
def lslin(invars, invar):
    print('\ncurrent value of ', invars, ' is= ', invar)
    outvars = input('\nchange to (def=no change)')
    if outvars == '':
        return invar
    else:
        outvar = eval(outvars)
    return outvar


# def lslina(invars,invar):
#     print('\ncurrent value of ',invars,' is= ',invar)
#     outvars=input('\nchange to (def=no change)')
#     if (outvars==''):
#         return invar
#     else:
#         outvar=eval(outvars)
#     return outvar

# -------------------------------------------------------------------------
# integration default parameters
# NOTE: dt=.001
dt = .001
tt = 0.
numdata = 30000
paramin = 'used data from files'

# input (old inputtest_II_1.py)
# input data from files

# give it just a number n, will find files cn.txt, bn.txt, mn.txt, icn.txt
fast = input('\n ONLY NUMBER n and I will find cn.txt, etc. (#/a, Def=a)')
if fast.isdigit():
    fnamec = 'c' + fast + '.txt'
    fnameb = 'b' + fast + '.txt'
    fnamem = 'm' + fast + '.txt'
    fnameic = 'ic' + fast + '.txt'
else:
    fname = input('\nfilename for array c [I will add .txt]=  ')
    fnamec = fname + '.txt'

    fname = input('\nfilename for array b [I will add .txt]=  ')
    fnameb = fname + '.txt'

    fname = input('\nfilename for array m [I will add .txt]=  ')
    fnamem = fname + '.txt'

    fname = input('\nfilename for array IC [I will add .txt]=  ')
    fnameic = fname + '.txt'

# get the files
c, numc = getxn(fnamec)
b, numb = getx(fnameb)
m, numm = getx(fnamem)
ic, numic = getx(fnameic)

# check for consistentcy
if numc ** 3 != numb * numm * numic:
    print("\nFATAL WARNING - input issue - numbers c,b,m,ic don't match")

# make arrays (NOT matrices) and print
ma = np.array(m)
ba = np.array(b)
ca = np.array(c)
ica = np.array(ic)
print('\nca= ', ca)
print('\nba= ', ba)
print('\nma= ', ma)
print('\nic= ', ica)

# xinit=[.0*i for i in range (p)]
# initial conditions
# for i in range (p):
#     xinit[i]=float(input('\ninitial value of x (e.g. .5 or -.5)  '))
# xold=xinit
# xolda=np.array(xold)

# You can change here, but program MUST finish before you get graph
change = input('\nWant to CHANGE parameters (y/n, def=n)')
if change.lower() == 'y':
    c = lslin('c', c)
    b = lslin('b', b)
    m = lslin('m', m)
    ic = lslin('ic', ic)
    ma = np.array(m)
    ba = np.array(b)
    ca = np.array(c)
    ica = np.array(ic)
    print('/n/nNEW PARAMETER VALUES ARE:')
    print('\nca= ', ca)
    print('\nba= ', ba)
    print('\nma= ', ma)
    print('\nic= ', ica)
    paramin = input('\nNOTE changes here!  ')
else:
    pass

# OK now start the integration
# fix +/- RESERVOIRS NEVER < 0
ica[1] = max(ica[1], 0.)
ica[2] = max(ica[2], 0.)
xolda = ica
tt = 0
t = [0. for i in range(numdata)]
z = np.array([ica for i in range(numdata)])  # NOTE: changed ic to ica HEREß

for i in range(1, numdata):
    mtanh = np.tanh(z[i - 1])
    cterm = np.dot(ca, mtanh)
    dx = dt * (ma * z[i - 1] + ba + cterm)
    #    print ('\nz[i-1]',z[i-1])
    #    print ('\nma*z[i-1],ba, ca * mtanh, dx','\n',ma*z[i-1],ba, ca * mtanh, dx,'\n\n')
    tt += dt
    t[i] = tt
    z[i] = z[i - 1] + dx
    z[i][1] = max(z[i][1], 0.0)  # the + reservoir is NEVER negative
    z[i][2] = max(z[i][2], 0.0)  # the - reservoir is NEVER negative
    z[i][3] = max(z[i][3], 0.0)  # the + future is NEVER negative
    z[i][4] = max(z[i][4], 0.0)  # the - future is NEVER negative
    # TODO call circle plot here to animate


# PLOT
print('\nYour plot is ready')
localtime = time.asctime(time.localtime(time.time()))
x_start = ica
x_final = z[-1]
plt.figure(1)
# plt.axes([.1,.1,.8,.7])  ORIGINAL
plt.axes([0.1, .075, .8, .7])
# new

plt.plot(t, z[:, 0], color='navy', linewidth=6)
plt.plot(t, z[:, 1], color='greenyellow', linewidth=4)
plt.plot(t, z[:, 2], color='hotpink', linewidth=4)
plt.plot(t, z[:, 3:numc])

# print labels on lines
xtext = 25
for i in range(numc):
    ytext = z[-1, i]
    varis = str(i + 1)
    plt.text(xtext, ytext, varis)
    xtext -= 1

# plt.text(5,0,'num')

# old
# #plt.axis([0, 3, -20, 20])
# lines=plt.plot(t,z)
# #lines=plt.plot (ta,x1a,'-b',ta,x2a,'-r')
# plt.setp(lines,linewidth=2.)
# #plt.show()
# #plt.setp(lines,linewidth=2.,mec='r')

programname = 'map2_4.py   ' + localtime
param1 = '\n   input files= ' + str(fnamec) + '    ' + str(fnameb) + \
         '    ' + str(fnamem) + '    ' + str(fnameic)
param2 = '\nx_start= ' + str(ica) + '    dt= ' + str(dt) + \
         '    var colors=ngp-bgrcmyk' + '\nx_final=' + str(x_final)
param4 = '\n' + paramin

# making it possible to print c matrix
# nh=int(numc/2)
# ca1=ca[0:nh,:]
# ca2=ca[nh:numc,:]
# ca1s=str(ca1)
# ca2s=str(ca2)
# ca1s2=ca1s.replace('\n','')
# ca2s2=ca2s.replace('\n','')
# param3='\nb= '+ str(b) +' m= '+str(m) + '\nc= '+ ca1s2 +'\n'+ ca2s2
titlelsl = programname + param1 + param4 + param2
plt.title(titlelsl, fontsize=10)
# plt.show()
# plt.axis([0, .1, -.2, .2])

# OK, now trying to print the second plot
zzin = x_final
ccin = ca
pprogamename = programname
clockplot(ccin, zzin, pprogamename)
