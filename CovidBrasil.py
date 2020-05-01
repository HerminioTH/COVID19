import numpy as np
import csv
import matplotlib as plt
import datetime as dt
import matplotlib.dates as mdates

def getDataFromState(data, hash_state, state):
    return data[hash_state[state][0]:hash_state[state][1],:]

def createHashTable(data):
    hash_state = {}
    regioes = {}
    nData = data.shape[0]
    for i in range(1,nData):
        if data[i][1] in hash_state:
            hash_state[data[i][1]][1] = i+1
        else:
            hash_state[data[i][1]] = [i, 0]
    return hash_state

def getData(fileName):
    with open(fileName, "r") as f:
        data = np.array(list(csv.reader(f, delimiter=";")))
    f.close()
    return data

def prepareAxis(ax):
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.grid(True)

def plotStatesOfRegionData(data, hash_state, region, ax1, ax2, ax3, ax4):
    ax1.set_title(data[0][3])
    ax2.set_title(data[0][4])
    ax3.set_title(data[0][5])
    ax4.set_title(data[0][6])
    for state in region[list(region)[0]]:
        state_data = getDataFromState(data, hash_state, state)
        time_axis = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in state_data[:,2]]
        ax1.plot(time_axis, state_data[:,3].astype(np.float), '.-', linewidth=2.0, label=state)
        ax2.plot(time_axis, state_data[:,4].astype(np.float), '.-', linewidth=2.0, label=state)
        ax3.plot(time_axis, state_data[:,5].astype(np.float), '.-', linewidth=2.0, label=state)
        ax4.plot(time_axis, state_data[:,6].astype(np.float), '.-', linewidth=2.0, label=state)
    ax1.legend(loc=2)
    ax2.legend(loc=2)
    ax3.legend(loc=2)
    ax4.legend(loc=2)

def plotRegionData(data, hash_state, region, ax1, ax2, ax3, ax4):
    ax1.set_title(data[0][3])
    ax2.set_title(data[0][4])
    ax3.set_title(data[0][5])
    ax4.set_title(data[0][6])
    n = len(getDataFromState(data, hash_state, region[list(region)[0]][0]))
    new_cases = np.zeros(n)
    cumulative_cases = np.zeros(n)
    new_deaths = np.zeros(n)
    cumulative_deaths = np.zeros(n)
    for state in region[list(region)[0]]:
        state_data = getDataFromState(data, hash_state, state)
        new_cases += state_data[:,3].astype(np.float)
        cumulative_cases += state_data[:,4].astype(np.float)
        new_deaths += state_data[:,5].astype(np.float)
        cumulative_deaths += state_data[:,6].astype(np.float)
    time_axis = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in state_data[:,2]]
    ax1.plot(time_axis, new_cases, '.-', linewidth=2.0, label=list(region)[0])
    ax2.plot(time_axis, cumulative_cases, '.-', linewidth=2.0, label=list(region)[0])
    ax3.plot(time_axis, new_deaths, '.-', linewidth=2.0, label=list(region)[0])
    ax4.plot(time_axis, cumulative_deaths, '.-', linewidth=2.0, label=list(region)[0])
    ax1.legend(loc=2)
    ax2.legend(loc=2)
    ax3.legend(loc=2)
    ax4.legend(loc=2)

def plotCountryData(data, hash_state, regions, ax1, ax2, ax3, ax4):
    ax1.set_title(data[0][3])
    ax2.set_title(data[0][4])
    ax3.set_title(data[0][5])
    ax4.set_title(data[0][6])
    a = getDataFromState(data, hash_state, regions[0][list(regions[0])[0]][0])
    n = len(a)
    new_cases = np.zeros(n)
    cumulative_cases = np.zeros(n)
    new_deaths = np.zeros(n)
    cumulative_deaths = np.zeros(n)
    for region in regions:
        for state in region[list(region)[0]]:
            state_data = getDataFromState(data, hash_state, state)
            new_cases += state_data[:,3].astype(np.float)
            cumulative_cases += state_data[:,4].astype(np.float)
            new_deaths += state_data[:,5].astype(np.float)
            cumulative_deaths += state_data[:,6].astype(np.float)
    time_axis = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in state_data[:,2]]
    # time_axis = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in state_data[:,2]]
    ax1.plot(time_axis, new_cases, '.-', linewidth=2.0)
    ax2.plot(time_axis, cumulative_cases, '.-', linewidth=2.0)
    ax3.plot(time_axis, new_deaths, '.-', linewidth=2.0)
    ax4.plot(time_axis, cumulative_deaths, '.-', linewidth=2.0)
    ax1.legend(loc=2)
    ax2.legend(loc=2)
    ax3.legend(loc=2)
    ax4.legend(loc=2)


