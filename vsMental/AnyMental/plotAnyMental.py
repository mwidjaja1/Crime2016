# -*- coding: utf-8 -*-
""" plotAnyMental.py ----------------------------------------------------------
    Takes the pickled file and plots using it

    Input:
    data: The pickled dataframe
         
    Output:
    CSV & Pickled File: Pandas DataFrame with the column names of YYYY as level
                        one & each type of stat as level two vs. each state.
--------------------------------------------------------------------------- """

import glob
import matplotlib.pyplot as plt
import pandas as pd
import os

def openFile(inDir, inFile):
    """ User should set this to the present working directory where the pkl
        data is. This script will then find the .pkl file inside & return it.
        
        Input:
        inDir: The directory where the file is in. [Default = 'os.getcwd()']
        inFile: An additional string to search the file for before its
                extension. [Default = '']
        
        Output:
        data: The first .pkl file found in that dir opened up as a dataframe
    """
    files = glob.glob(os.path.join(inDir, '*' + inFile + '*.pkl'))
    if len(files)>1:
        print("WARNING: This dir has more than 1 pkl file. Using first one")
    data = pd.read_pickle(files[0])
    return data

def createFigure(xData, yData, colors, names, pTitle, xAxis, yAxis):
    """ Creates a Matplotlib Pyplot Figure
    
        Input:
        xData: List of xData to plot
        yData: List of yData to plot
        colors: List of colors to use
        names: List of line names to use
        pTitle: The title of the figure
        xAxis: The title of the xAxis
        yAxis: The title of the yAxis
        
        Output: 
        figure: The figure to plot on
    """
    plt.figure()
    data = list(zip(xData, yData, colors, names))
    for line in data:
        plt.scatter(line[0], line[1], color=line[2], label=line[3])
    
    # Sets plot information & present it
    plt.title(pTitle)
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.legend()
    plt.show()
    
    
    
""" Main function loads the pickled data frame & launches plot commands
"""
# Loads the Mental Data
mentData = openFile('/Users/Matthew/Github/Crime2016/vsMental/AnyMental/',
                    '')

# Loads the Shooting Data
murdData = openFile('/Users/Matthew/Github/Crime2016/Data_MassShooting/', 
                    'BinaryShooting')

# Plots
fig = createFigure(murdData['Fatalities'],
                   mentData['2012']['18 or Older Estimate'], 
                   ['k'], 
                   ['Fatalities vs 18 >'],
                   'Any Mental', 'X', 'Y')

