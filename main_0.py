from CovidBrasil import *
import matplotlib.pyplot as plt


data = getData("Data/COVID19_20200501.csv")
# data = getData("Data/COVID19_20200408.csv")
hash_state = createHashTable(data)

SUL = {'SUL' : ['SC', 'PR', 'RS']}
SUDESTE = {'SUDESTE' : ['SP','MG','RJ','ES']}
CENTRO_OESTE = {'CENTRO OESTE' : ['DF', 'GO', 'MT', 'MS']}
NORTE = {'NORTE' : ['AC', 'AP', 'PA', 'RO', 'RR', 'TO', 'AM']}
NORDESTE = {'NORDESTE' : ['AL', 'BA', 'CE', 'MA', 'PB', 'PI', 'PE', 'RN', 'SE']}
region = NORDESTE
regions = [SUL, SUDESTE, CENTRO_OESTE, NORTE, NORDESTE]

fig, axis = plt.subplots(2, 2, figsize=(10,7))
ax1 = axis[0][0]
ax2 = axis[0][1]
ax3 = axis[1][0]
ax4 = axis[1][1]
fig.subplots_adjust(left=0.05, right=0.975, top=0.965, bottom=-0.18, hspace=0.3)
prepareAxis(ax1)
prepareAxis(ax2)
prepareAxis(ax3)
prepareAxis(ax4)

plotStatesOfRegionData(data, hash_state, SUL, ax1, ax2, ax3, ax4)
# plotStatesOfRegionData(data, hash_state, NORDESTE, ax1, ax2, ax3, ax4)
# plotCountryData(data, hash_state, regions, ax1, ax2, ax3, ax4)
# plotRegionData(data, hash_state, NORTE, ax1, ax2, ax3, ax4)
# plotRegionData(data, hash_state, NORDESTE, ax1, ax2, ax3, ax4)
# plotRegionData(data, hash_state, CENTRO_OESTE, ax1, ax2, ax3, ax4)
# plotRegionData(data, hash_state, SUDESTE, ax1, ax2, ax3, ax4)
# plotRegionData(data, hash_state, SUL, ax1, ax2, ax3, ax4)

fig.autofmt_xdate()
plt.show()


