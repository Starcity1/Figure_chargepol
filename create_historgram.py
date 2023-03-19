##
# Histogram plotter from chargepol data.
# Author : David Rodriguez Sanchez
# Date   : Feb 06 2023
# Desc   : Using a converted .csv file from a .hdf5 chargepol file, the script will create a histogram.
#
# Dependencies : seaborn, numpy, matplotlib, Python 3.6+
# Usage :: python3 create_density_plot.py <path_to_charepol_csv_file>
##

import csv

import matplotlib.pyplot as plt
from matplotlib import pyplot as py
from sys import argv
from os import path
from math import sqrt

def plotHistogram(timeList, eventList, initTime, interval = 0,
                  figurePath= False, returnFigure = False, ax=None):
    if(ax == None):
        ax = plt.gca()

    posEventIntAlt = list()
    negEventIntAlt = list()

    for index, timePoint in enumerate(timeList):
        if initTime < timeList[index]:
            if (initTime + interval) < timeList[index]: continue
            charge = eventList[index][0]
            if charge.strip() == "pos":
                posEventIntAlt.append(eventList[index][1])
            if charge.strip() == "neg":
                negEventIntAlt.append(eventList[index][1])

    ax.hist(posEventIntAlt, bins=int(sqrt(len(posEventIntAlt))), density=True, color=[1, 0.062, 0.019, 0.7]
            ,orientation="horizontal")
    ax.hist(negEventIntAlt, bins=int(sqrt(len(negEventIntAlt))), density=True, color=[0.062, 0.019, 1, 0.7]
            ,orientation="horizontal")

    if returnFigure:
        return ax

    ax.set(ylabel="Altitude (km)", xlabel="Density")
    plt.grid()

    plt.savefig(figurePath + "/Histogram.pdf")