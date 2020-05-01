import datetime as dt
import matplotlib.dates as mdates
import numpy as np
import json

def getJsonData(fileName):
	with open(fileName, 'r') as json_file:
		data = json.load(json_file)
	return data

##data = pd.read_csv("Data/COVID19_20200403.csv")

class CovidDataFromJson(object):
	def __init__(self, fileName):
		self.data = getJsonData(fileName).get('records')

		self.createJsonHash()

	def createJsonHash(self):
		self.country_hash = {}
		n = len(self.data)
		for i in range(n):
			country = self.data[i]['countryterritoryCode']
			if country in self.country_hash:
				self.country_hash[country][1] = i+1
			else:
				self.country_hash[country] = [i, 0]

	def __getColumnFromCountry(self, country_code, column_name):
		column_values = []
		begin = self.country_hash[country_code][0]
		end = self.country_hash[country_code][1]
		for i in range(begin, end):
			column_values.append(self.data[i][column_name])
		return column_values

	def getTimeFromCountry(self, country_code):
		return self.__getColumnFromCountry(country_code, 'dateRep')

	def getCasesFromCountry(self, country_code):
		return self.__getColumnFromCountry(country_code, 'cases')



class Country(object):
	def __init__(self, covid_data, country_code, country_population=1.):
		self.covid_data = covid_data
		self.country_code = country_code
		self.country_population = country_population
		self.__initialize()

	def __initialize(self):
		self.getTime()

		self.getCases()
		self.getDeaths()
		self.sortData()

		self.getAccumCases()
		self.getNormCases()
		self.getNormAccumCases()

		self.getAccumDeaths()
		self.getNormDeaths()
		self.getNormAccumDeaths()

		self.getDataPerCapita(1.)

	def __getColumn(self, column_name):
		column_values = []
		begin = self.covid_data.country_hash[self.country_code][0]
		end = self.covid_data.country_hash[self.country_code][1]
		for i in range(begin, end):
			column_values.append(self.covid_data.data[i][column_name])
		return column_values

	def __getAccumulatedColumn(self, column_data):
		n = self.cases.size
		aux_list = np.zeros(n,dtype=np.int32)
		aux_list[0] = column_data[0]
		for i in range(1,n):
			aux_list[i] = aux_list[i-1] + column_data[i]
		return aux_list

	def __findCase100(self):
		for i,v in enumerate(self.accumulatedCases):
			if v >= 100:
				break
		self.day100 = i

	def __normalize(self, column_data):
		norm_values = column_data[self.day100:]
		norm_times = np.array(range(len(norm_values)))
		return np.array(norm_times), np.array(norm_values)

		# norm_values = []
		# for i, v in enumerate(column_data):
		# 	if v >= 100:
		# 		norm_values.append(v)
		# norm_times = np.array(range(len(norm_values)))
		# return np.array(norm_times), np.array(norm_values)

	def getDataPerCapita(self, group):
		self.getCasesPerGroup(group)
		self.getDeathsPerGroup(group)

	def sortData(self):
		self.cases = np.array([x for _,x in sorted(zip(self.time,self.cases))])
		self.deaths = np.array([x for _,x in sorted(zip(self.time,self.deaths))])
		self.time.sort()

	def getTime(self):
		self.time = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in self.__getColumn('dateRep')]


	def getCases(self):
		self.cases = abs(np.array(self.__getColumn('cases')).astype(np.int16))

	def getAccumCases(self):
		self.accumulatedCases = self.__getAccumulatedColumn(self.cases)
		self.__findCase100()

	def getNormCases(self):
		self.norm_time_cases, self.normalizedCases = self.__normalize(self.cases)

	def getNormAccumCases(self):
		self.norm_time_cases, self.normalizedAccumulatedCases = self.__normalize(self.accumulatedCases)

	def getCasesPerGroup(self, group):
		self.casesPerCapita = group*self.cases/self.country_population
		self.accumCasesPerCapita = group*self.accumulatedCases/self.country_population
		self.normalizedCasesPerCapita = group*self.normalizedCases/self.country_population
		self.normalizedAccumulatedCasesPerCapita = group*self.normalizedAccumulatedCases/self.country_population


	def getDeaths(self):
		self.deaths = abs(np.array(self.__getColumn('deaths')).astype(np.int16))

	def getAccumDeaths(self):
		self.accumulatedDeaths = self.__getAccumulatedColumn(self.deaths)

	def getNormDeaths(self):
		self.norm_time_deaths, self.normalizedDeaths = self.__normalize(self.deaths)

	def getNormAccumDeaths(self):
		self.norm_time_deaths, self.normalizedAccumulatedDeaths = self.__normalize(self.accumulatedDeaths)

	def getDeathsPerGroup(self, group):
		self.deathsPerCapita = group*self.deaths/self.country_population
		self.accumDeathsPerCapita = group*self.accumulatedDeaths/self.country_population
		self.normalizedDeathsPerCapita = group*self.normalizedDeaths/self.country_population
		self.normalizedAccumulatedDeathsPerCapita = group*self.normalizedAccumulatedDeaths/self.country_population

FONTS = {'fontname': 'serif'}
FONT_SIZE = 14

def prepareAxis(ax):
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
    ax.grid(True)

def setLabelsToAxis(ax, x_label, y_label):
	ax.grid(True)
	ax.set_xlabel(x_label, fontsize=FONT_SIZE, **FONTS)
	ax.set_ylabel(y_label, fontsize=FONT_SIZE, **FONTS)

def plotDailyData(ax1, ax2, co_country, color=None):
	prepareAxis(ax1)
	prepareAxis(ax2)
	if color == None:
		ax1.plot(co_country.time, co_country.cases, '.-', linewidth=2.0, label=co_country.country_code)
		ax2.plot(co_country.time, co_country.deaths, '.-', linewidth=2.0, label=co_country.country_code)
	else:
		ax1.plot(co_country.time, co_country.cases, '.-', color=color, linewidth=2.0, label=co_country.country_code)
		ax2.plot(co_country.time, co_country.deaths, '.-', color=color, linewidth=2.0, label=co_country.country_code)
	setLabelsToAxis(ax1, 'Data', 'Casos diarios')
	setLabelsToAxis(ax2, 'Data', 'Obitos diarios')

def plotNormalizedDailyData(ax1, ax2, co_country, color=None):
	N1 = co_country.norm_time_cases.size
	N2 = co_country.cases.size
	N = N2 - N1
	if color == None:
		ax1.plot(co_country.norm_time_cases, co_country.cases[N:], '.-', linewidth=2.0, label=co_country.country_code)
		ax2.plot(co_country.norm_time_cases, co_country.deaths[N:], '.-', linewidth=2.0, label=co_country.country_code)
	else:
		ax1.plot(co_country.norm_time_cases, co_country.cases[N:], '.-', color=color, linewidth=2.0, label=co_country.country_code)
		ax2.plot(co_country.norm_time_cases, co_country.deaths[N:], '.-', color=color, linewidth=2.0, label=co_country.country_code)
	setLabelsToAxis(ax1, 'Dias a partir do contagio 100', 'Casos diarios')
	setLabelsToAxis(ax2, 'Dias a partir do contagio 100', 'Obitos diarios')

def plotAccumulatedData(ax1, ax2, co_country, color=None):
	if color == None:
		ax1.plot(co_country.time, co_country.accumulatedCases, '.-', linewidth=2.0, label=co_country.country_code)
		ax2.plot(co_country.time, co_country.accumulatedDeaths, '.-', linewidth=2.0, label=co_country.country_code)
	else:
		ax1.plot(co_country.time, co_country.accumulatedCases, '.-', color=color, linewidth=2.0, label=co_country.country_code)
		ax2.plot(co_country.time, co_country.accumulatedDeaths, '.-', color=color, linewidth=2.0, label=co_country.country_code)
	setLabelsToAxis(ax1, 'Data', 'Casos acumulados')
	setLabelsToAxis(ax2, 'Data', 'Obitos acumulados')

def plotNormalizedAccumulatedData(ax1, ax2, co_country, color=None):
	if color == None:
		ax1.plot(co_country.norm_time_cases, co_country.normalizedAccumulatedCases, '.-', linewidth=2.0, label=co_country.country_code)
		ax2.plot(co_country.norm_time_deaths, co_country.normalizedAccumulatedDeaths, '.-', linewidth=2.0, label=co_country.country_code)
	else:
		ax1.plot(co_country.norm_time_cases, co_country.normalizedAccumulatedCases, '.-', color=color, linewidth=2.0, label=co_country.country_code)
		ax2.plot(co_country.norm_time_deaths, co_country.normalizedAccumulatedDeaths, '.-', color=color, linewidth=2.0, label=co_country.country_code)
	setLabelsToAxis(ax1, 'Dias a partir do contagio 100', 'Casos acumulados')
	setLabelsToAxis(ax2, 'Dias a partir do contagio 100', 'Obitos acumulados')

def plotNormalizedAccumulatedDataPerCapita(ax1, ax2, co_country, color=None):
	if color == None:
		ax1.plot(co_country.norm_time_cases, co_country.normalizedAccumulatedCasesPerCapita, '.-', linewidth=2.0, label=co_country.country_code)
		ax2.plot(co_country.norm_time_deaths, co_country.normalizedAccumulatedDeathsPerCapita, '.-', linewidth=2.0, label=co_country.country_code)
	else:
		ax1.plot(co_country.norm_time_cases, co_country.normalizedAccumulatedCasesPerCapita, '.-', color=color, linewidth=2.0, label=co_country.country_code)
		ax2.plot(co_country.norm_time_deaths, co_country.normalizedAccumulatedDeathsPerCapita, '.-', color=color, linewidth=2.0, label=co_country.country_code)
	setLabelsToAxis(ax1, 'Dias a partir do contagio 100', 'Casos acumulados / 100.000 hab.')
	setLabelsToAxis(ax2, 'Dias a partir do contagio 100', 'Obitos acumulados / 100.000 hab.')

def divide(a, b):
	n = a.size
	c = np.zeros(n)
	for i in range(n):
		if b[i] != 0:
			c[i] = float(a[i])/float(b[i])
		else:
			c[i] = 0.0
	return c

def plotMortalityRate(ax, co_country, color=None):
	# print float(co_country.deaths)
	# print float(co_country.cases)
	# print float(co_country.deaths)/float(co_country.cases)
	if color == None:
		ax.plot(co_country.time, 100*divide(co_country.accumulatedDeaths,co_country.accumulatedCases), '.-', linewidth=2.0, label=co_country.country_code)
	else:
		ax.plot(co_country.time, 100*divide(co_country.accumulatedDeaths,co_country.accumulatedCases), '.-', color=color, linewidth=2.0, label=co_country.country_code)
	setLabelsToAxis(ax, 'Data', 'Taxa de mortalidade')




SOUTH_AMERICA = ['ARG','BOL','BRA','CHL','COL','ECU','PRY','PER','URY','VEN']
CENTRAL_AMERICA = ['CUB','GTM','HND','NIC','HTI','CRI','SLV','JAM','PAN','DOM']
NORTH_AMERICA = ['CAN','MEX','USA']
EUROPE = ['DEU','AUT','BEL','KAZ','HRV','DNK','ESP','FIN','FRA','GRC','HUN','IRL','ITA','NLD','POL','PRT','GBR','CZE','ROU','RUS','SWE','CHE','TUR','UKR','VAT']
ASIA = ['CHN','IND','IDN','PAK','BGD','RUS','JPN','IRN','KOR','SAU']
OCEANIA = ['AUS','PNG','NZL']
AFRICA = ['NER','ETH','EGY','ZAF','KEN','AGO','MOZ','LBR','GIN','SEN','SOM','RWA']
COUNTRIES = {
				# AMERICA LATINA
				'ARG' : 40677348,
				'BOL' : 9247816,
				'BRA' : 210147125,
				'CHL' : 16454143,
				'COL' : 45013674,
				'ECU' : 13927650,
				'PRY' : 6831306,
				'PER' : 29180899,
				'URY' : 3477778,
				'VEN' : 26414815,

				# AMERICA CENTRAL
				'CUB' : 11167325,
				'GTM' : 15472156,
				'HND' : 8098263,
				'NIC' : 6082447,
				'HTI' : 9996731,
				'CRI' : 4133884,
				'SLV' : 6948073,
				'JAM' : 2950210,
				'PAN' : 3694190,
				'DOM' : 9378818,

				# AMERICA DO NORTE
				'CAN' : 37373000,
				'MEX' : 126577691,
				'USA' : 328700000,

				# EUROPA
				'DEU' : 83251851,
				'AUT' : 8169929,
				'BEL' : 10274595,
				'KAZ' : 15217711,
				'HRV' : 4437460,
				'DNK' : 5368854,
				'ESP' : 45061274,
				'FIN' : 5157537,
				'FRA' : 59765983,
				'GRC' : 10645343,
				'HUN' : 10075034,
				'IRL' : 4234925,
				'ITA' : 58751711,
				'NLD' : 16318199,
				'POL' : 38625478,
				'PRT' : 10409995,
				'GBR' : 61100835,
				'CZE' : 10256760,
				'ROU' : 21698181,
				'RUS' : 142200000,
				'SWE' : 9090113,
				'CHE' : 7507000,
				'TUR' : 71517100,
				'UKR' : 48396470,
				'VAT' : 900,

				# ASIA
				'CHN' : 1384689024,
				'IND' : 1296834048,
				'IDN' : 262787408,
				'PAK' : 207862512,
				'BGD' : 159453008,
				'RUS' : 142122784,
				'JPN' : 126168160,
				'IRN' : 83024744,
				'KOR' : 51446201,
				'SAU' : 33091112,

				# OCEANIA
				'AUS' : 25318081,
				'PNG' : 8558800,
				'NZL' : 4795886,

				# AFRICA
				'NER' : 190886311,
				'ETH' : 104957439,
				'EGY' : 97553151,
				'ZAF' : 56717151,
				'KEN' : 49699862,
				'AGO' : 29784194,
				'MOZ' : 29668834,
				'LBR' : 4731906,
				'GIN' : 12717176,
				'SEN' : 15850567,
				'SOM' : 14742523,
				'RWA' : 12208407
			}

COLORS = [
			'black',
			'silver',
			'rosybrown',
			'firebrick',
			'red',
			'darksalmon',
			'sienna',
			'sandybrown',
			'bisque',
			'gold',
			'olivedrab',
			'chartreuse',
			'palegreen',
			'darkgreen',
			'seagreen',
			'mediumspringgreen',
			'darkcyan',
			'deepskyblue',
			'royalblue',
			'navy',
			'blue',
			'mediumpurple',
			'plum',
			'm',
			'mediumvioletred',
			'palevioletred'
			]




if __name__ == '__main__':
	from ReadCovidData import prepareAxis
	import matplotlib.pyplot as plt

	fileName = "Data/download.json"
	data = getJsonData(fileName)['records']

	co = CovidDataFromJson(data)
	print(co.country_hash)
	co_BRA = Country(co, 'BRA')
	co_ITA = Country(co, 'ITA')
	co_FRA = Country(co, 'FRA')
	co_CHN = Country(co, 'CHN')
	co_USA = Country(co, 'USA')


	# time_ITA = co.getTimeFromCountry('ITA')
	# cases_ITA = co.getCasesFromCountry('ITA')

	fig, ax1 = plt.subplots(1, 1, figsize=(22,7))
	fig.subplots_adjust(left=0.03, right=0.975, top=0.965, bottom=0.1, hspace=0.3)

	ax1.plot(co_BRA.time, co_BRA.cases, '.-', linewidth=2.0, label=co_BRA.country_code)
	ax1.plot(co_ITA.time, co_ITA.cases, '.-', linewidth=2.0, label=co_ITA.country_code)
	ax1.plot(co_FRA.time, co_FRA.cases, '.-', linewidth=2.0, label=co_FRA.country_code)
	ax1.plot(co_CHN.time, co_CHN.cases, '.-', linewidth=2.0, label=co_CHN.country_code)
	ax1.plot(co_USA.time, co_USA.cases, '.-', linewidth=2.0, label=co_USA.country_code)
	ax1.grid(True)
	plt.legend(loc=2)


	plt.show()



