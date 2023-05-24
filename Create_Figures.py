##
# Program allows user to combine various plots together.
# Author : David Rodriguez Sanchez
# Date   : Feb 06 2023
# Version: 0.0.1
# Desc   : Using a converted .csv file from a .hdf5 chargepol file, the script will create a variety of figures.
#
# Dependencies : seaborn, numpy, matplotlib, Python 3.6+
# Usage :: python3 Create_Figures.py <path_to_chargepol_csv_file>
##

# First section of script checks if all modules necessary are installed.
# DO NOT CHANGE.
# Built-in modules.
import importlib.util
import sys
import subprocess as sb
import os


MODULE_REQ = ["matplotlib", "numpy", "os", "math", "csv", "scipy"]
if sys.version_info.major != 3 and sys.version_info.minor < 8:
    exit("Please make sure to install Python 3.8+")

if importlib.util.find_spec("cartopy") is None:
    sb.check_call(['conda', 'install', '-c', 'conda-forge', 'cartopy'])

for module in MODULE_REQ:
    if importlib.util.find_spec(module) is None:
        sb.check_call([sys.executable, '-m', 'pip', 'install', module])

# Other script dependencies.
# from create_historgram import plotHistogram
# from create_scatter_plot import plotScatterMap
# from create_houston_map import mapHoustonData
# import prepare_data as ch

from src.create_density_plot import plotDensity
from src.create_historgram import plotHistogram
from src.create_scatter_plot import plotScatterMap
from src.create_houston_map import mapHoustonData

import src.prepare_data as ch

import matplotlib.pyplot as plt
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

import cartopy.crs as ccrs

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
              "[4] Event Layer on Houston\n" \
              "--- Combinations ---\n" \
              "[5] Density graph and histogram\n" \
              "[6] Density Graph and scatter plot\n" \
              "[7] Density Graph and scatter plot with map\n" \
              "[8] All plots \n" \
              "[q] Quit program.\n"
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


def plotFigs(figure, chargepol, params):
    if figure == "1":
        print("Density Graph :: ")
        init, interval = ChooseTime(chargepol["Timestamp"])
        ax = plotDensity(chargepol["Timestamp"], chargepol["Charge"],
                         init, interval, figurePath)
        ax.set(title=(params["Title"] + " " + params["Date"]))
        plt.savefig(figurePath + "/Density_plot.pdf")

    elif figure == "2":
        print("Histogram :: ")
        init, interval = ChooseTime(chargepol["Timestamp"])
        ax = plotHistogram(chargepol["Timestamp"], chargepol["Charge"],
                           init, interval, figurePath)
        ax.set(title=(params["Title"] + " " + params["Date"]))
        plt.savefig(figurePath + "/Histogram.pdf")

    elif figure == "3":
        print("Scatter Plot")
        ax = plotScatterMap(chargepol, figurePath)
        ax.set(title=(params["Title"] + " " + params["Date"]))
        plt.savefig(figurePath + "/Scatter.pdf")

    elif figure == "4":
        print("Houston Map")
        ax = mapHoustonData(chargepol, figurePath)
        ax.set(title=(params["Title"] + " " + params["Date"]))
        plt.savefig(figurePath + "/Houston_map.pdf")

    elif figure == "5":
        print("Density plot and histogram:: ")
        init, interval = ChooseTime(chargepol["Timestamp"])
        fig, (ax1, ax2) = plt.subplots(1, 2, sharey='row',
                                       figsize=(15, 4))
        plotDensity(chargepol["Timestamp"], chargepol["Charge"], init,
                    interval, figurePath, returnFigure=True, ax=ax1)
        plotHistogram(chargepol["Timestamp"], chargepol["Charge"], init,
                      interval, figurePath, returnFigure=True, ax=ax2)

        ax1.grid()
        ax1.set_xlabel("Time after 0 UTC (sec)")
        ax2.grid()
        ax2.set_xlabel("Density")

        ax1.set_ylabel("Altitude")

        plt.title(params["Title"] + " " + params["Date"])
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

        plt.title(params["Title"] + " " + params["Date"])
        plt.savefig(figurePath + "/Density_scatter.pdf")

    elif figure == "7":
        print("Density plot and Houston map")
        init, interval = ChooseTime(chargepol["Timestamp"])
        fig = plt.figure(figsize=(10, 7))

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
        gl.top_labels = False
        gl.right_labels = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER

        plt.title(params["Title"] + " " + params["Date"])
        plt.savefig(figurePath + "/Density_Hmap.pdf")
    elif figure == "8":
        print("XLMA-Formatted figure")
        init, interval = ChooseTime(chargepol["Timestamp"])
        fig = plt.figure(figsize=(8.3, 11.7)) # Common dimensions for poster.

        spec = plt.GridSpec(8, 6, hspace=.35)

        # Density plot
        ax1 = fig.add_subplot(spec[0:1, 0:])
        ax1.set(ylim=[0, 15])
        ax1.set(ylabel="Altitude (km)")
        ax1.tick_params(axis='both', which='major', labelsize=10)
        plotDensity(chargepol["Timestamp"], chargepol["Charge"], init,
                    interval, figurePath, returnFigure=True, ax=ax1)

        # First Scatter Plot
        ax2 = fig.add_subplot(spec[1:2, :5])
        ax2.tick_params(axis='both', which='major', labelsize=10)
        plotScatterMap(chargepol, figurePath, returnFigure=True, ax=ax2, timeInfo=[init, interval])

        # Houston Map

        ax3 = fig.add_subplot(spec[2:6, :5], projection=ccrs.PlateCarree())
        mapHoustonData(chargepol, returnFigure=True, ax=ax3)

        gl = ax3.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
        gl.top_labels = False
        gl.right_labels = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER

        ax3.set(xlabel="Longitude", ylabel="Latitude")

        # Histogram
        ax4 = fig.add_subplot(spec[1:2, 5])
        ax4.set_yticks([0, 5.0, 10.0, 15.0])
        ax4.yaxis.tick_right()
        ax4.yaxis.set_label_position("right")
        plotHistogram(chargepol["Timestamp"], chargepol["Charge"],
                           init, interval, ax=ax4)

        # Second (vertical) scatter plot.
        ax5 = fig.add_subplot(spec[2:6 , 5])
        ax5.yaxis.tick_right()
        ax5.yaxis.set_label_position("right")
        ax5.tick_params(axis='both', which='major', labelsize=10)
        plotScatterMap(chargepol, figurePath, returnFigure=True, ax=ax5, timeInfo=[init, interval], makeVertical=True)
        plt.ylabel("Time UTC (sec)")
        plt.xlabel("Altitude (km)")

        fig.suptitle(params["Date"] + " " + params["Title"] + " ")
        plt.savefig(figurePath + "/XLMA-format.pdf")

    elif figure == "q" or figure == "Q":
        exit(0)
    else:
        print("Invalid figure ID.")

    plt.close()
    print("Done.")


# Function will return a list of all the plots the user wants to create.:W

if __name__ == "__main__":
    # Clears terminal screen
    os.system("cls")

    if len(sys.argv) < 2:
        exit(f"Usage: python CreateFigures.py <path_to_chargepol_csv_file>")

    chargepol = ch.get_data(sys.argv[1])
    figures = set(input(getMessage(1)).split())

    # Small buffer that only allows valid figures.
    validFigures = sorted([figure for figure in figures if figure in availableFigures])

    # All figures will be stored in a directory called 'figures'
    if not os.path.exists(figurePath) and not os.path.isdir(figurePath):
        os.mkdir(figurePath)

    # This bracket allows you to change the name and xAxis.
    params = {
        "Title": "Source Density, threshold=3",
        "Date": "221105"
    }

    for figure in validFigures:
        plotFigs(figure, chargepol, params)