from os import path
import os
import csv
"""
THIS FILE IS PURELY FOR TESTING PURPOSES
"""


# files = os.listdir(directory)

# for file in files:
#     file_path = os.path.join(directory, file)  # Create the full file path
#     print(file_path)
#     with open(file_path, 'r', newline='') as csv_file:
#         reader = csv.reader(csv_file)


def get_multipleData(directory):
    files = os.listdir(directory)

    iterations = 0 #This variable will be used to store how many days we have iterated through
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
        file_path = os.path.join(directory, file)  # Create the full file path
        """Creates a custom data frame of the charge pol data."""
        if not (path.exists(file_path) and file_path[-4:] == '.csv'):
            exit("Error: file must be a .csv file.")

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

    #test = chargepol["Date"]
    #print(test)
    return chargepol


directory = "chargepol_230505-230509" #Enter folder with CSV data
get_multipleData(directory)
