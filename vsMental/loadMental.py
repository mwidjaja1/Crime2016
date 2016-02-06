# -*- coding: utf-8 -*-
""" loadMental.py -------------------------------------------------------------
    Loads all mental data from NSDUH and saves it as a CSV & pickled file.

    Input:
    pwd: The directory where all NSDUH mental data should be saved in as
         pwd/<nameOfCategory>/<YYYY.csv>
         
    Output:
    CSV & Pickled File: Pandas DataFrame with the column names of YYYY as level
                        one & each type of stat as level two vs. each state.
--------------------------------------------------------------------------- """

import glob
import pandas as pd
import os

def setpwd():
    """ User should set this to the present working directory where the CSV
        data is and will be saved to. Inside of this directory should be a 
        directory named after each data type. Each data type should be saved
        as a YYYY.csv file
    """
    cwd = '/Users/Matthew/Github/Crime2016/vsMental/'
    return cwd

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

def removeKeys(df):
    """ Removes all keys which have 'CI', 'Order', or 'Unnamed' in its column
        names from the data frame. We then strip all blank lines, spaces, & 
        tab returns from the remaining column names.
    
        Input & Output:
        tempDf: The data frame to remove & strip keys from
    """
    dropKeys = [x for x in df.keys() if 'CI' in x or 'Order' in x \
                or 'Unnamed' in x]    
    for dropKey in dropKeys: df.drop(dropKey, 1, inplace=True)
    df.columns = [x.strip().replace('\n', ' ').replace('\r', ' ') \
                  for x in df.columns]
    return df
            
def createMultiIndex(levelOne, df):
    """ Creates a multiple index where all the column names in this tempDf 
        becomes the 'second' level where the 'first' level is added here.
    
        Input & Output:
        levelOne: The first level in which column names should be under
        tempDf: The data frame to add a multi index to
        
        Output:
        tempDf: The DF with a multiindex of levelOne >> <originalNames>
    """
    multiKeys = [(levelOne, key) for key in df.keys()]
    df.columns = pd.MultiIndex.from_tuples(multiKeys,
                                           names=['Year', 'Stats'])
    return df   

def deleteRows(data):
    """ Deletes regions and changes invalid state names to the official name
        
        Input & Output:
        data: Data Frame to replace its names for
    """
    # Drops Rows for Regions 
    regions = ['Midwest', 'Northeast', 'South', 'West', 'National', 
               'Total U.S.']
    for region in regions:
        if region in data.index: data.drop(region, inplace=True)
        
    # Renames States
    data.index.str.replace('District of Columbia','D.C.')
    return data

""" Main function loops through each folder in the pwd directory. We then loop
    in the dir to find all 2*.csv files. We load it up, remove invalid column 
    names, & prepare remaining column names to save it. We then make a new DF
    with the remaining column names & save it as a CSV and pickled file.
"""
# Finds directories where each directory is a data type
pwd = setpwd()
folders = [x for x in os.listdir(pwd) if os.path.isdir(x)]

# Opens up each CSV file and converts it to a data frame
for folder in folders:
    print('Analyzing: ' + folder)
    dataDict = {}
    cate = folder.split('/')[-1]
    for csv in glob.glob(os.path.join(pwd, folder, '2*.csv')):
        print('  ' + csv)
        year = os.path.split(csv)[-1].split('.csv')[0]
        for headRow in range(0,8):
            # Tries to load the CSV as a DF by filtering out empty header rows.
            #   Depending on when the file was made, there could be a varying
            #   amount of junk header rows we have to trim out.
            tempDf = openCsv(csv, headRow)
            
            # Checks to see how many of our keys are valid
            validKeys = [x for x in tempDf.keys() if 'Unnamed' not in x]
            
            # If we have enough valid keys, we then drop the unnecessary
            #   columns and save the CSV file as a multi index dataframe.
            if len(validKeys)>5:
                tempDf = removeKeys(tempDf)
                dataDict[year] = createMultiIndex(year, tempDf)
                break

    # Combines each year's data frame into one larger one & updates row labels
    dataDf = pd.concat([dataDict[year] for year in dataDict], axis=1)
    dataDf = deleteRows(dataDf)
    print(dataDf)
    
    # Converts DF values to floats by removing the percent sign
    dataDf.replace({'%':''}, regex=True, inplace=True)
    
    # Saves data frame to output files
    dataDf.to_csv(os.path.join(pwd, folder, cate+'.csv'))
    dataDf.to_pickle(os.path.join(pwd, folder, cate+'.pkl'))