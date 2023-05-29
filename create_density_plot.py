##
# Density graph plotter from chargepol data.
# Author : David Rodriguez Sanchez
# Date   : Feb 06 2023
# Desc   : Using a converted .csv file from a .hdf5 chargepol file. We create a density plot.
#
# Dependencies : seaborn, numpy, matplotlib, Python 3.6+
# Usage :: python3 create_density_plot.py <path_to_charepol_csv_file>
##

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import matplotlib.dates as mdates

# PARAMETERS (rn it is empty)
def plotDensity(timeList = 0, eventList = 0, initTime = 0, interval = 0, dateList = 0,
                   store_path = None, returnFigure = False, ax = None):
    if(ax == None):
        ax = plt.gca()

    # xAxisList = np.array([])
    # for time in timeList:
    #     xAxisList.append(time)

    timePoints = list()
    if interval < 1000: linewidth = 1
    elif interval < 10000: linewidth = .6
    elif interval < 20000: linewidth = .3
    else: linewidth = .1
    #print(list(enumerate(timeList)))
    for index, time in enumerate(timeList):
        if initTime < time:
            if (initTime + interval) < timeList[index]: continue
            charge = eventList[index][0]
            # Plotting positive events.
            if charge.strip() == "pos":
                ax.plot([timeList[index], timeList[index] + .001],
                        [eventList[index][1], eventList[index][1] + eventList[index][2]],
                        color=[1, 0.062, 0.019, 0.7], linewidth=linewidth)
            # Plotting negative events.
            if charge.strip() == "neg":
                ax.plot([timeList[index], timeList[index] + .001],
                        [eventList[index][1], eventList[index][1] + eventList[index][2]],
                        color=[0.062, 0.019, 1, 0.7], linewidth=linewidth)
            timePoints.append(time)

    #Error handling here check if timePoints is empty if so then throw error
    if not timePoints:
        raise Exception("No lightning activity at the time chosen")

    # Plotting density
    ax1 = ax.twinx()
    density = gaussian_kde(timePoints)
    density.covariance_factor = lambda: .25
    density._compute_covariance()
    xs = np.linspace(timePoints[0], timePoints[-1], len(timePoints))
    ax1.plot(xs, density(xs), color=[0,0,0], marker=',')
    # Hiding y-axis values
    ax1.set_yticks([])

    # Creating second x-axis for dates
    # # ax2 = ax1.twiny()
    # # new_xticks = list()
    # #
    # # #print(timePoints)
    # # for i in range(int(timePoints[0]), int(timePoints[-1])):
    # #     if i % 86400 == 0:
    # #         xticklocation = (float((i-(int(timePoints[0])))/interval))
    # #         new_xticks.append(xticklocation)
    # # ax2.set_xticks(new_xticks)
    # # #print(new_xticks)
    if int(timePoints[-1]) - int(timePoints[0]) >= 172800:  # if our interval is greater or equal to 2 days
        ticks = []
        for i in range(int(timePoints[0]), int(timePoints[-1])):
            if i % 86400 == 0:
                ticks.append(i)
        plt.xticks(ticks)
        ax.figure.canvas.draw()
        labels = [item.get_text() for item in ax.get_xticklabels()]
        startingDateChargePol = int(initTime / 86400)
        endingDateChargePol = startingDateChargePol + len(ticks)
        dateList = dateList[startingDateChargePol:endingDateChargePol]
        print(dateList)
        for i, n in enumerate(dateList):
            labels[i] = str(dateList[i])
        ax.set_xticklabels(labels)

    ax.set(ylim=[0,15])
    ax.set(xlabel="Time after 0 UTC (sec)", ylabel="Altitude (km)")
    plt.suptitle("Flashes")
    plt.grid()


    return (ax, timePoints)