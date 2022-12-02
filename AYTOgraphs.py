import matplotlib.pyplot as plt
import numpy as np
import csv
import pathlib
import math

def readData():
    """reads and returns the data from the data.csv file and returns it in a list"""
    dir_path = pathlib.Path(__file__).parent.resolve()
    dir_path = dir_path.joinpath(r"data.csv")
    _L = []
    with open(dir_path,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row != []:
                _L.append([row[0],int(row[1]),float(row[2])])
            else:
                continue
    return _L

def create_graph_weeks(algorithm):
    """creates and displays histogram using data from the data.csv file"""
    data = readData()
    if len(data)<1:
        raise Exception("there is no data")
    filtered_data = [] #Contains all entries with only the specified algorithm type
    for i in data:
        if i[0] == algorithm:
            filtered_data.append(i[1])
    if len(filtered_data)<1:
        raise Exception("there is no data with this algorithm type")
    
    _bins = max(filtered_data)-min(filtered_data)+1
    if _bins > 40:
        _bins = 40


    plt.hist(filtered_data, range=(min(filtered_data),max(filtered_data)+1), bins=_bins, align='mid')
    plt.show()

if __name__ == "__main__":
    create_graph_weeks('ideal')
    