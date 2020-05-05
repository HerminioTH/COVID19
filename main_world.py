from ReadCovidJSON import *
import matplotlib.pyplot as plt
import numpy as np
import random



fileName = "Data/WHO_29_04_2020.json"
co = CovidDataFromJson(fileName)

country_codes = ['BRA','ITA','FRA','CHN','USA','DEU','ESP','KOR','JPN']
country_codes = ['BRA','ITA','FRA','USA','ESP','ECU','SWE','DEU']
# country_codes = ['BRA','','JPN']
# country_codes = EUROPE

nCodes = len(country_codes)
nColors = len(COLORS)
indexes = np.linspace(0, nColors-1, nCodes).astype(np.int32)

# random.shuffle(COLORS)

# fig, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(2, 3, figsize=(25,12))
fig, axes = plt.subplots(2, 3, figsize=(21,12))
ax1 = axes[0][0]
ax2 = axes[0][1]
ax3 = axes[0][2]
ax4 = axes[1][0]
ax5 = axes[1][1]
ax6 = axes[1][2]
fig.subplots_adjust(left=0.05, right=0.975, top=0.965, bottom=0.1, hspace=0.2, wspace=0.3)


for i,code in zip(indexes, country_codes):
	co_COUNTRY = Country(co, code, COUNTRIES[code])
	co_COUNTRY.getDataPerCapita(1e5)

	color = COLORS[i]
	# plotDailyData(ax1, ax4, co_COUNTRY, color)
	# plotAccumulatedData(ax1, ax4, co_COUNTRY, color)

	plotNormalizedDailyData(ax1, ax4, co_COUNTRY, color)
	plotNormalizedAccumulatedData(ax2, ax5, co_COUNTRY, color)
	plotNormalizedAccumulatedDataPerCapita(ax3, ax6, co_COUNTRY, color)


ax1.legend(loc=0)
ax2.legend(loc=0)
ax3.legend(loc=0)
ax4.legend(loc=0)
ax5.legend(loc=0)
ax6.legend(loc=0)

print(type(co_COUNTRY.deaths))


plt.show()
