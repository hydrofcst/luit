import matplotlib.pyplot as plt

def plotncvar(ncdat, ncvar, starttime, endtime, xlabel, ylabel):
    '''
    Plots netCDF variables temporally. Start and End time 
    set globally
    '''
    plt.figure(figsize=(15, 5))
    ncdat[ncvar].loc[starttime:endtime].plot()
    plt.ylabel(xlabel, fontsize = 16)
    plt.xlabel(ylabel, fontsize = 16)
    plt.show()
