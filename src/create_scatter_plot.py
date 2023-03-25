##
# Histogram plotter from chargepol data.
# Author : David Rodriguez Sanchez
# Date   : Mar 03 2023
# Desc   : Using a chargepol .csv file, I will be creating a map that plots the position of the event on a map of htx
#
# Dependencies : seaborn, numpy, matplotlib, Python 3.6+, plotly-geo, geopandas, pyshp, shapely
# Usage :: python3 scatterMap.py <path_to_charepol_csv_file>
##
import os.path

import matplotlib.pyplot as plt

def createAltitudelist(data, time=None):
    # if data.keys() not in ["Timestamp", "Charge", "Location"]:
    #     print("Invalid HLMA File, please contact David Rodriguez")
    #     exit(2)

    negAlt = [[],[]] # Index 0 are all longitudes, index 1 are all latitudes
    posAlt = [[],[]]

    if time == None:
        for index, event in enumerate(data['Charge']):
            if(event[0] == 'pos'):
                posAlt[0].append(data["Timestamp"][index])
                posAlt[1].append(event[1])
            else:
                negAlt[0].append(data["Timestamp"][index])
                negAlt[1].append(event[1])
    else:
        for index, event in enumerate(data['Charge']):
            if event[0] == 'pos' and withinInterval(time, data["Timestamp"][index]):
                posAlt[0].append(data["Timestamp"][index])
                posAlt[1].append(event[1])
            elif event[0] == 'neg' and withinInterval(time, data["Timestamp"][index]):
                negAlt[0].append(data["Timestamp"][index])
                negAlt[1].append(event[1])

    return (negAlt, posAlt)

def withinInterval(timeInfo, timePoint) -> bool:
    return (timePoint > timeInfo[0] and timePoint < (timeInfo[0] + timeInfo[1]))


def plotScatterMap(HLMAdata = None, figurePath = None, returnFigure = False, ax = None, timeInfo = None):
    if ax == None:
        ax = plt.gca()

    if timeInfo != None:
        neg, pos = createAltitudelist(HLMAdata, timeInfo)
    else:
        neg, pos = createAltitudelist(HLMAdata)

    ax.scatter(x=neg[0], y=neg[1], s=8, linewidth=.625, color=[0.062, 0.019, 1], marker="_")
    ax.scatter(x=pos[0], y=pos[1], s=8, linewidth=.625, color=[1, 0.062, 0.019], marker="+")


    plt.xlabel("Time after 0 UTC (sec)")
    plt.ylabel("Altitude (km)")

    return ax
