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
from pylab import *
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

def prepareXData(xInData, years):
    """ Takes xData, which is most likely the # of Fatalities, Injuries, &
        Totals from the shootings of each state, and parses it year-by-year.
        
        Input:
        xInData: DF of xValues which will be filtered & organized by each
                 'year' in years. Each 'year' in years must be used here.
        years:   The list of years where xInData will be split up by initially
                 to organize and concat the data.
        
        Output:
        xData:   A dictionary where each key is a year & each value is the DF
                 data for that given year.
    """
    xData = {}

    # Finds year in xData & sums all values up per year for each state
    for year in years:
        # Finds all shooting victims in each year (Fatalities, Injured, Total).
        #   We then add a column for # of shootings. We then sum it all up.
        xTemp = xInData[xInData.Year == year]
        xTemp.loc[:,'Shooting'] = 1
        xTemp = xTemp.groupby(xTemp.index).sum()
        del xTemp['Year']
        
        """
        # Fixes multiple years summation issue if there was more than one
        #   shooting in a state in a given year.
        fixYear = xTemp[xTemp.Shooting>1]
        for state in fixYear.index:
            xTemp.loc[state, 'Year'] = xTemp.loc[state, 'Year'] / \
                                       fixYear.loc[state, 'Shooting']
                                       """
                                       
        # Create Multiindex so it's Year >> [Fatalities, Injured, etc.]
        yearCols = [year]*len(xTemp.columns)
        cols = list(zip(*[yearCols, list(xTemp.columns)]))
        colsIdx = pd.MultiIndex.from_tuples(cols, names=['Year', 'Stat'])
        xTemp.columns = colsIdx

        # Saves the year's current data to the DataFrame
        xData[year] = xTemp
    
    """    
    # Groups the statistics by stat type and sums it up across all years   
    summary = xData.groupby(level=['Stat'], axis=1).sum()
    
    # Create Multiindex so it's 'Summary' >> [Fatalities, Injured, etc.]
    yearCols = ['All']*len(summary.columns)
    cols = list(zip(*[yearCols, list(summary.columns)]))
    colsIdx = pd.MultiIndex.from_tuples(cols, names=['Year', 'Stat'])
    summary.columns = colsIdx
    
    # Saves the summarized data to the DataFrame
    xData['All'] = summary"""
    return xData

def prepareYData(yInData, yKey, years):
    """ Takes yData, which is probably the mental heatlh data for each year &
        age group vs. each state, and parses it year-by-year
        
        Input:
        yInData: Data frame of yValues which will be filtered & organized by
                 each 'year' in years. If a 'year' is not here, we'll use +/-
                 1 year before giving up.
        yKey:    The key of data being extracted from yInData for plotting.
        years:   The list of years where xInData & yInData will be split up by
                 initially to organized and concat the data.
        
        Output:
        yData:   A dictionary where each key is a year & each value is the DF
                 data for that given year.
    """
    yData = {}
    
    # Gets columns/years from existing yInData
    yYears = [int(x) for x in list(yInData.columns.get_level_values(0))]
    
    for year in years:
        # Finds alternative year if this year is not in yData
        if year in yYears:
            yTemp = yInData[str(year)][yKey]
        elif year+1 in yYears:
            yTemp = yInData[str(year+1)][yKey]
        else:
            yTemp = yInData[str(year-1)][yKey]
        
        # Create Multiindex so it's Year >> [Fatalities, Injured, etc.]
        if year:
            yearCols = [year]*len(yTemp.columns)
            cols = list(zip(*[yearCols, list(yTemp.columns)]))
            colsIdx = pd.MultiIndex.from_tuples(cols, names=['Year', 'Stat'])
            yTemp.columns = colsIdx
        
            # Saves the year's current data to the DataFrame
            yData[year] = yTemp
    
    return yData 
    """
    # Groups the statistics by stat type and sums it up across all years   
    summary = yData.groupby(level=['Stat'], axis=1).mean()
    
    # Create Multiindex so it's 'Summary' >> [Fatalities, Injured, etc.]
    yearCols = ['All']*len(summary.columns)
    cols = list(zip(*[yearCols, list(summary.columns)]))
    colsIdx = pd.MultiIndex.from_tuples(cols, names=['Year', 'Stat'])
    summary.columns = colsIdx
    
    # Saves the summarized data to the DataFrame
    yData['All'] = summary"""
    
    #return yData
        
def combineData(xData, yData, years):
    """ Takes the xData and yData from the two prepare functions above and
        we combine those two data sets with respect to the years & states.
    """
    data = pd.DataFrame()
    for year in years:
        data = pd.concat([data, pd.concat([xData[year], yData[year]], axis=1)],
                         axis=1)
    
    return data

def ratios(data, years):
    """ Calculates the ratios between the 'people' statistics & mental helth
        data.
    """
    for year in years:
        temp = data[year]

def prepareData(xInData, yInData, yKey, years):
    """ DEPRICIATED
        Takes xData which should be the sum across all of its time periods &
        yData which shold be the average across all of its time periods, and
        concats it to a data frame so both are indexed by their states, where
        states with no data are populated with 0 values.
        
        Input:
        xInData: Data frame of xValues which will be filtered & organized by
                 each 'year' in years. Each 'year' in years must be used here.
        yInData: Data frame of yValues which will be filtered & organized by
                 each 'year' in years. If a 'year' is not here, we'll use +/-
                 1 year before giving up.
        yKey:    The key of data being extracted from yInData for plotting.
        years:   The list of years where xInData & yInData will be split up by
                 initially to organized and concat the data.
                 
        Output:
        allData: The concated data set between xInData & yInData, indexed by
                 all of the possible row labels from xInData & yInData.
    """
    xData = pd.DataFrame()
    yData = pd.DataFrame()
    
    # Finds year in xData & sums all values up per state
    for year in years:
        # Finds all shooting victims in each year (Fatalities, Injured, Total).
        #   We then add a column for # of shootings. We then sum it all up.
        xYrData = xInData[xInData.Year == year]
        xYrData.loc[:,'Shooting'] = 1
        xYrData = xYrData.groupby(xYrData.index).sum()
        
        # Fixes multiple years summation issue if there was more than one
        #   shooting in a state in a given year.
        fixYear = xYrData[xYrData.Shooting>1]
        for state in fixYear.index:
            xYrData.loc[state, 'Year'] = xYrData.loc[state, 'Year'] / \
                                         fixYear.loc[state, 'Shooting']
    
        # Finds alternative year if this year is not in yData
        if year in yInData:
            yYrData = yInData[str(year)][yKey]
        elif year not in yInData and str(int(year)+1) in yInData:
            year = str(int(year)+1)
            yYrData = yInData[str(year)][yKey]
        elif year not in yInData and str(int(year)-1) in yInData:
            year = str(int(year)-1)
            yYrData = yInData[str(year)][yKey]
        else:
            year = None
    
        # Creates unified data frame for data if xData and yData is found
        if year is not None:
            xData = pd.concat([xData, xYrData], axis=0)
            yData = pd.concat([yData, yYrData], axis=1)

    # Sums up xData which should be total fatalities
    xData = xData.groupby(xData.index).sum()
    yData = yData.groupby(yData.index).mean()
    yData.columns = [yKey]
    
    # Removes na values & sums everything up from the unified data set      
    allData = pd.concat([xData, yData], axis=1)
    allData = allData.fillna(0)

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
yLabels =['Age 18>', 'Age 26>']
clrs = ['k', 'g']

# Prepares Data
xData = prepareXData(murdData, years)
yData = prepareYData(mentData, yKeys, years)
data = combineData(xData, yData, years)
#data = prepareData(murdData, mentData, yKeys, years)
#test = pd.concat([xData, mentData], levels=['Year'], axis=1)

# Prepare quantity of shootings per year
#for year in years:
    

# Prepares Figure for People Data
plt.figure()
f, (ax1, ax2, ax3) = plt.subplots(1,3, sharey=True)
f.tight_layout()
ax1.set_ylabel('All Mental Illness Cases')

# Plots each year vs. Fatalities
ax1.set_xlabel('Fatalities')
for idx, yKey in enumerate(yKeys):
    ax1.scatter(data.Fatalities, data[yKeys[idx]], color=clrs[idx], 
                label=yLabels[idx])
    m,b = polyfit(data.Fatalities, data[yKeys[idx]], 1) 
    ax1.plot(data.Fatalities, m*data[yKeys[idx]]+b, color=clrs[idx])

# Plots each year vs. Injuries
ax2.set_xlabel('Injured')
for idx, yKey in enumerate(yKeys):
    ax2.scatter(data.Injured, data[yKeys[idx]], color=clrs[idx], 
                label=yLabels[idx])
    m,b = polyfit(data.Injured, data[yKeys[idx]], 1) 
    ax2.plot(data.Injured, m*data[yKeys[idx]]+b, color=clrs[idx])               

# Plots each year vs. Total
ax3.set_xlabel('Total')
for idx, yKey in enumerate(yKeys):
    ax3.scatter(data.Total, data[yKeys[idx]], color=clrs[idx], 
                label=yLabels[idx])
    m,b = polyfit(data.Total, data[yKeys[idx]], 1) 
    ax3.plot(data.Total, m*data[yKeys[idx]]+b, color=clrs[idx])   
plt.show()

# Prepares Figure for Shooting Data
plt.figure()
plt.ylabel('All Mental Illness Cases')

# Plots each year vs. Injuries
plt.set_xlabel('Total Attacks')
for idx, yKey in enumerate(yKeys):
    plt.scatter(data.Total, data[yKeys[idx]], color=clrs[idx], 
                label=yLabels[idx])
    m,b = polyfit(data.Total, data[yKeys[idx]], 1) 
    plt.plot(data.Total, m*data[yKeys[idx]]+b, color=clrs[idx])   

plt.show()

"""
    xData = murdData[murdData.Year == year].Fatalities
    xData = xData.groupby(xData.index).sum()
    yData = [allData[(str("'"+year+"'"), '18 or Older Estimate')],
            [allData[(str("'"+year+"'"), '26 or Older Estimate')]]]
    allData = pd.concat([xData, yData], axis=1).fillna(0)
    """