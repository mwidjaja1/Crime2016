"""
Data Source:
http://www.motherjones.com/politics/2012/12/mass-shootings-mother-jones-full-data

Amount of mass shootings (more than 4 down) since 1982
"""

import pandas as pd

# Loads Data
root = '/Users/Matthew/Github/Crime2016/Data_MassShooting/'
massst = pd.read_excel(root+'MassShooting.xlsx', index_col=0)
locations = massst.index

# Creates State Column
state = {'State':[]}
for location in massst.Location:
    state['State'].append(location.split(',')[-1].strip())
    

# Combines Data & State into DataFrame
massst = pd.concat([massst, pd.DataFrame(state, index=locations)], axis=1)
massst.to_pickle(root+'MainShooting.pkl')
states = massst.State

# Creates Dataframe with 'Binary' Data
binaryst = pd.DataFrame([massst.Year, massst.Location, massst.Fatalities, 
                         massst.Injured, massst.Total, massst.Venue, 
                         massst.Mental, massst.Legal, massst.Weapons,
                         massst.Race, massst.Gender]).T
binaryst.index = states
binaryst.to_pickle(root+'BinaryShooting.pkl')

# Group By Total Victims
peoplest = pd.DataFrame([massst.Year, massst.Fatalities, massst.Injured, 
                         massst.Total]).T
peoplest = peoplest.groupby(peoplest.index).sum()
peoplest.index = states
peoplest.to_pickle(root+'statsPerState.pkl')