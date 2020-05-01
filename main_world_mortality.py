from ReadCovidJSON import *
import matplotlib.pyplot as plt
import numpy as np
import random

fileName = "Data/WHO_09_04_2020.json"
data = getJsonData(fileName)['records']
co_data = CovidDataFromJson(data)

country_codes = ['BRA','ITA','FRA','CHN','USA','DEU','ESP','KOR','JPN']
# country_codes = ['BRA','ITA','FRA','USA','ESP','ECU','SWE','DEU']
# country_codes = ['BRA']
# country_codes = ['BRA','ITA','ESP','CHN','USA']
# country_codes = SOUTH_AMERICA

nCodes = len(country_codes)
nColors = len(COLORS)
indexes = np.linspace(0, nColors-1, nCodes).astype(np.int32)

# random.shuffle(COLORS)

# fig, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(2, 3, figsize=(25,12))
fig, ax1 = plt.subplots(1, 1, figsize=(7,7))
fig.subplots_adjust(left=0.05, right=0.975, top=0.965, bottom=0.1, hspace=0.2, wspace=0.3)


for i,code in zip(indexes, country_codes):
	co_COUNTRY = Country(co_data, code, COUNTRIES[code])
	co_COUNTRY.getDataPerCapita(1e5)

	color = COLORS[i]
	plotMortalityRate(ax1, co_COUNTRY, color)

ax1.legend(loc=0)

print type(co_COUNTRY.deaths)


plt.show()
