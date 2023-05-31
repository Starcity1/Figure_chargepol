##
# Script to create a list containing all Chargepol.csv data.
# Author : David Rodriguez Sanchez
# Date   : Feb 06 2023
# Desc   : Using a converted .csv file from a .hdf5 chargepol file, the script will create a histogram.
#
# Dependencies : seaborn, numpy, matplotlib, Python 3.6+
# Usage :: python3 prepare_data.py <path_to_charepol_csv_file>
##
import os
from os import path
import csv


def verify_data(filepath) -> bool:
    with open(filepath, 'r') as chargepol_file:
        chargepol_file.readline()
        header = chargepol_file.readline()
        if "longitude" not in header:
            return False
    return True


def get_data(filepath):
    """Creates a custom data frame of the charge pol data."""
    if not (path.exists(filepath) and filepath[-4:] == '.csv'):
        exit("Error: file must be a .csv file.")

    if not verify_data(filepath):
        exit("Error: please used the forked version of chargepol")

    time = list()
    chargeEvent = list()
    longLat = list()

    with open(filepath, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if(row[0] != "pos") and (row[0] != "neg") : continue
            time.append(float(row[1]))
            chargeEvent.append([row[0], float(row[2]), float(row[3])])
            longLat.append([row[-1], row[-2]])

    chargepol = { "Timestamp" : time,    # Time of event
                  "Charge": chargeEvent, # Type of charge, length and starting altitude
                  "Location": longLat    # Longitude and altitude of charge
                }
    #print(chargepol["Timestamp"])
    return chargepol


def get_multipleData(directory, specifiedDateInterval = "none"): #For multiple days
    files = os.listdir(directory)
    start_index = 0 #By default we will start from the first file when getting chargepol data

    if specifiedDateInterval != "none":
        firstMonth = specifiedDateInterval[0:2]
        firstDay = specifiedDateInterval[3:5]
        firstYear = specifiedDateInterval[8:10]

        secondMonth = specifiedDateInterval[13:15]
        secondDay = specifiedDateInterval[16:18]
        secondYear = specifiedDateInterval[21:23]

        firstFile = "chargepol_" + firstYear + firstMonth + firstDay + ".csv"
        secondFile = "chargepol_" + secondYear + secondMonth + secondDay + ".csv"

        start_index = files.index(firstFile)
        end_index = files.index(secondFile)
        files = files[start_index:(end_index+1)]

    iterations = start_index #"Iterations" will be used to store how many days we have iterated through
    time = list()
    chargeEvent = list()
    longLat = list()
    date = list()

    chargepol = {"Timestamp": time,  # Time of event
                 "Charge": chargeEvent,  # Type of charge, length and starting altitude
                 "Location": longLat,  # Longitude and altitude of charge
                 "Date": date  # MM/DD. ex. 05/05
                 }

    for file in files:
        #print(file)
        file_path = os.path.join(directory, file)  # Create the full file path
        """Creates a custom data frame of the charge pol data."""
        if not (path.exists(file_path) and file_path[-4:] == '.csv'):
            exit("Error: file must be a .csv file.")

        if not verify_data(file_path):
            exit("Error: please used the forked version of chargepol")

        month = file[-8:-6]
        day = file[-6:-4]
        monthAndDay = month + "/" + day
        date.append(monthAndDay)

        with open(file_path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if(row[0] != "pos") and (row[0] != "neg") : continue
                time.append((float(row[1]))+(iterations*86400))
                chargeEvent.append([row[0], float(row[2]), float(row[3])])
                longLat.append([row[-1], row[-2]])
        iterations += 1

    return chargepol

# def get_initialDate(directory, specifiedDateInterval = "All"):
#     files = os.listdir(directory)
#
#     if specifiedDateInterval != "All":
#         firstMonth = specifiedDateInterval[0:2]
#         firstDay = specifiedDateInterval[3:5]
#         firstYear = specifiedDateInterval[6:10]
#     elif specifiedDateInterval == "All": #ex. chargepol_230505.csv
#         firstMonth = files[0][-8:-6]
#         firstDay = files[0][-6:-4]
#         firstYear = "20" + files[0][-10:-8]

    # return(firstYear, firstMonth, firstDay)
