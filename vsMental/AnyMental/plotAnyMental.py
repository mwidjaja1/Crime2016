#! /Users/Matthew/anaconda/envs/Python35/bin/python3

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

def prepareData(xData, yData, yKeys, year):
    allData = []
    
    # Finds year in xData & sums all values up per state
    xData = xData[xData.Year == year]
    xData = xData.groupby(xData.index).sum()
    
    # Finds alternative year if this year is not in yData
    if year not in yData and str(int(year)+1) in yData:
        year = str(int(year)+1)
    elif year not in yData and str(int(year)-1) in yData:
        year = str(int(year)-1)
    else:
        year = None
    
    # Creates unified data frame for data if xData and yData is found
    if year:
        for idx, yKey in enumerate(yKeys):
            allData.append(pd.concat([xData, yData[str(year)][yKey]], axis=1))
            allData[idx] = allData[idx].fillna(0)
    
    return allData
    

""" Main function loads the pickled data frame & launches plot commands
"""
# Loads the Mental Data
mentData = openFile('/Users/Matthew/Github/Crime2016/vsMental/AnyMental/',
                    '')

# Loads the Shooting Data
murdData = openFile('/Users/Matthew/Github/Crime2016/Data_MassShooting/',
                    'statsPerState')
                    
# Sets lists for each key on the yAxis, the colors to use, and the labels
years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
yKeys = ['18 or Older Estimate', '26 or Older Estimate']

# Plots each year
plt.figure()
for year in [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]:
    allData = prepareData(murdData, mentData, yKeys, year)
    for idx, data in enumerate(allData):
        plt.scatter(data.Fatalities, data[yKeys[idx]], color='k', label='>18 Yrs')
    
# Adds universal plot elements
plt.title('Fatalities vs. Mental Health')
plt.xlabel('Fatalities')
plt.ylabel('Mental Health Data')
plt.legend()
plt.show()

"""
    xData = murdData[murdData.Year == year].Fatalities
    xData = xData.groupby(xData.index).sum()
    yData = [allData[(str("'"+year+"'"), '18 or Older Estimate')],
            [allData[(str("'"+year+"'"), '26 or Older Estimate')]]]
    allData = pd.concat([xData, yData], axis=1).fillna(0)
    """