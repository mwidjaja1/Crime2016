# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 13:29:21 2016

@author: Matthew
"""

import glob
import pandas as pd
import os

def openCsv(csv, headerRows):
    """ Opens up a CSV file as a Pandas Data Frame. We skip 'X' amount of
        headerRows while opening up the file & trying to find column names
        
        Input:
        csv: The path to the CSV file
        headerRows: A quantity of rows to remove from the beginning
        
        Output:
        tempDf: The opened up CSV file as a Pandas Dataframe
    """
    try:
        tempDf = pd.read_csv(csv, skiprows=headerRows, index_col=1, header=0)
    except:
        tempDf = pd.read_csv(csv, skiprows=headerRows, index_col=1, header=0,
                             engine='python') 
    return tempDf

# Allocates Dictionary for Data
dataDict = {}
dataName = 'mentalData'

# Opens up each CSV file and converts it to a data frame
for csv in glob.glob('./*.csv'):
    year = os.path.split(csv)[-1].split('.csv')[0]
    for headRow in range(0,8):
        # Tries to load the CSV as a dataframe by filtering out empty header
        #   rows. Depending on when the file was created, there could be a
        #   varying amount of junk header rows we have to trim out.
        tempDf = openCsv(csv, headRow)
        
        # Checks to see how many of our keys are valid
        validKeys = [x for x in tempDf.keys() if 'Unnamed' not in x]
        
        # If we have enough valid keys, we proceed to drop the unnecessary
        #   columns and save the CSV file as a multi index dataframe.
        if len(validKeys)>5:
            dropKeys = [x for x in validKeys if 'CI' in x or 'Order' in x]
            for dropKey in dropKeys: tempDf.drop(dropKey, 1, inplace=True)
                
            multiKeys = [(year, key) for key in tempDf.keys()]
            tempDf.columns = pd.MultiIndex.from_tuples(multiKeys, 
                                                       names=['Year', 'Stat'])
            dataDict[year] = tempDf
            break

# Combines each year's data frame into one larger one
dataDf = pd.concat([dataDict[year] for year in dataDict], axis=1)
dataDf.to_csv(dataName+'.csv')
dataDf.to_pickle(dataName+'.pkl')