"""
Data Source:
http://www.americashealthrankings.org/ALL/Graduation/

Percent of HS Graduates per State
"""

import matplotlib.pyplot as plt
import pandas as pd

# Loads Data
root = '/Users/Matthew/Github/Crime2016/vsEducation/'
hsgrad = pd.read_csv(root+'HSGraduation.csv', index_col=3)
hsgrad.to_pickle(root+'HSGraduation.pkl')

# Simplify hsgrad
hsgradsimp = pd.DataFrame(hsgrad.Value)
print(hsgradsimp)

# Loads MassShooting Data from 2013 & beyond
shoots = pd.read_pickle(root+'../Data_MassShooting/statsPerState.pkl')
shootsnew = shoots[shoots.Year>2012]
shootsnew = shootsnew.groupby(shootsnew.index).sum()

# Combines the shooting & hsgrad data
data = pd.concat([hsgradsimp, shoots], axis=0)
data = data.groupby(data.index).sum()

# Plots MassShooting Data for all time
plt.figure()
plt.scatter(data.Value, data.Total, color='k', label='Total')
plt.scatter(data.Value, data.Injured, color='b', label='Injured')
plt.scatter(data.Value, data.Fatalities, color='r', label='Fatalities')
plt.ylabel('People')
plt.xlabel('Graduation Rate')
plt.title('Graduation Rates vs. Mass Shootings')
plt.legend()
plt.show()
