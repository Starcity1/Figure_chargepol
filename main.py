##
# Program allows user to combine various plots together.
# Author : David Rodriguez Sanchez
# Date   : Feb 06 2023
# Desc   : Using a converted .csv file from a .hdf5 chargepol file, the script will create a variety of figures.
#
# Dependencies : seaborn, numpy, matplotlib, Python 3.6+
# Usage :: python3 main.py <path_to_chargepol_csv_file>
##

# Other script dependencies.
from create_density_plot import plotDensity
from create_historgram import plotHistogram
from create_scatter_plot import plotScatterMap
from create_houston_map import mapHoustonData
import prepare_data as ch

import matplotlib.pyplot as plt
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

import cartopy.crs as ccrs

from sys import argv
import subprocess as sb
import os

figurePath = "figures/"
availableFigures = ["1", "2", "3", "4", "5", "6", "7", "8"]

# This function stores and outputs all terminal messages
def getMessage(messageCode):
    msg = ""
    if messageCode == 1:
        msg = "Enter the figures you want to plot.\n" \
              "Usage example :: write '1 2 3' if you want a density graph, histogram, and scatter plot\n" \
              "[1] Density graph\n" \
              "[2] Histogram\n" \
              "[3] Scatter Plot\n" \
              "[4] Scatter Plot with map (NOT STABLE)\n" \
              "--- Combinations ---\n" \
              "[5] Density graph and histogram\n" \
              "[6] Density Graph and scatter plot\n" \
              "[7] Density Graph and scatter plot with map (NOT STABLE)\n" \
              "[8] All plots (NOT STABLE)\n"
    elif messageCode == 2:
        msg = "Choose time interval :: \n" \
        "[1] 1-minute interval\n" \
        "[2] 5-minute interval\n" \
        "[3] 10-minute interval\n" \
        "[4] 1-hour interval\n" \
        "[5] 5-hour interval\n" \
        "[6] 10-hour interval\n" \
        "[7] Custom.\n\n"

    return msg

def ChooseTime(chargepol_time) -> (int, int):
    minTime = chargepol_time[0]
    maxTime = chargepol_time[-1]

    initTime = int(input(f"Choose time interval between [{int(minTime)}, {int(maxTime)}] :: "))
    interval = 0

    timeInterval = int(input(getMessage(2)))
    if timeInterval == 1:
        interval = 60
    elif timeInterval == 2:
        interval = 300
    elif timeInterval == 3:
        interval = 600
    elif timeInterval == 4:
        interval = 3600
    elif timeInterval == 5:
        interval = 18000
    elif timeInterval == 6:
        interval = 36000
    elif timeInterval == 7:
        cInterval = int(float(input("Enter custom interval (sec) :: ")))
        interval = cInterval
    else:
        exit("Invalid time interval")

    return (initTime, interval)

def plotFigs(figure, chargepol):
    if figure == "1":
        print("Scatter Plot :: ")
        init, interval = ChooseTime(chargepol["Timestamp"])
        plotDensity(chargepol["Timestamp"], chargepol["Charge"], init, interval, figurePath)

    elif figure == "2":
        print("Histogram :: ")
        init, interval = ChooseTime(chargepol["Timestamp"])
        plotHistogram(chargepol["Timestamp"], chargepol["Charge"], init, interval, figurePath)

    elif figure == "3":
        plotScatterMap(chargepol, figurePath)

    elif figure == "4":
        mapHoustonData(chargepol, figurePath)

    elif figure == "5":
        print("Density plot and histogram:: ")
        init, interval = ChooseTime(chargepol["Timestamp"])
        fig, (ax1, ax2) = plt.subplots(1, 2, sharey='row',
                                       figsize=(15,4))
        plotDensity(chargepol["Timestamp"], chargepol["Charge"], init,
                      interval, figurePath, returnFigure=True, ax=ax1)
        plotHistogram(chargepol["Timestamp"], chargepol["Charge"], init,
                      interval, figurePath, returnFigure=True, ax=ax2)

        ax1.grid()
        ax1.set_xlabel("Time after 0 UTC (sec)")
        ax2.grid()
        ax2.set_xlabel("Density")

        ax1.set_ylabel("Altitude")

        plt.savefig(figurePath + "/Density_histogram.pdf")

    elif figure == "6":
        print("Density plot and scatter plot ::")
        init, interval = ChooseTime(chargepol["Timestamp"])
        fig, (ax1, ax2) = plt.subplots(2, sharex="col")

        ax1.grid()
        plotDensity(chargepol["Timestamp"], chargepol["Charge"], init,
                       interval, figurePath, returnFigure=True, ax=ax1)

        ax2.grid()
        plotScatterMap(chargepol, figurePath, returnFigure=True, ax=ax2, timeInfo=[init, interval])

        ax1.grid()
        ax1.set_ylabel("Altitude")

        ax2.set_ylabel("Altitude")
        ax2.set_xlabel("Time after 0 UTC (sec)")

        plt.savefig(figurePath + "/Density_scatter.pdf")

    elif figure == "7":
        print("Density plot and Houston map")
        init, interval = ChooseTime(chargepol["Timestamp"])
        fig = plt.figure(figsize=(10,7))

        spec = plt.GridSpec(3, 3, wspace=0.5, hspace=0.5)

        ax1 = fig.add_subplot(spec[0, 0:])
        ax1.set(ylim=[0, 15])
        ax1.set(xlabel="Time after 0 UTC (sec)", ylabel="Altitude (km)")
        ax1.set_title("Flashes")
        plt.grid()
        plotDensity(chargepol["Timestamp"], chargepol["Charge"], init,
                       interval, figurePath, returnFigure=True, ax=ax1)

        ax2 = fig.add_subplot(spec[1:, 0:], projection=ccrs.PlateCarree())
        mapHoustonData(chargepol, returnFigure=True, ax=ax2)

        gl = ax2.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER

        plt.savefig(figurePath + "/Density_Hmap.pdf")
    elif figure == "8":
        pass
    else:
        print("Invalid figure ID.")

    print("Done.")

# Function will return a list of all the plots the user wants to create.

if __name__ == "__main__":
    sb.run("clear")

    if len(argv) < 2:
        exit(f"Usage: python CreateFigures.py <path_to_chargepol_csv_file>")

    chargepol = ch.get_data(argv[1])
    figures = set(input(getMessage(1)).split())

    # Small buffer that only allows valid figures.
    validFigures = sorted([figure for figure in figures if figure in availableFigures])

    # All figures will be stored in a directory called 'figures'
    if not os.path.exists(figurePath) and not os.path.isdir(figurePath):
        os.mkdir(figurePath)

    for figure in validFigures:
        plotFigs(figure, chargepol)




