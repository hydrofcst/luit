#!/glade/u/home/manab/anaconda3/bin/python

import sys
import xarray as xr
import numpy as np
import glob, os
import shutil

if __name__ == "__main__":
    # User supplied information
    outdir = '/glade/p/work/manab/fcast/PNW/output/7468_b3bdcbb'                   #Directory containing SUMMA output
    convertdir = 'convert'
    finalfile = 'final.nc'
    
    # Step 1: Convert all SUMMA output files into HRU-only
    convertdir = os.path.join(outdir, convertdir)
    os.makedirs(convertdir, exist_ok = True)
    outfilelist = glob.glob((outdir+'/*.nc')) #list of all files

    for x in range(0, len(outfilelist)):
        ncconvert = xr.open_dataset(outfilelist[x])                                  #Import netCDF file

        runoffdata = ncconvert['averageInstantRunoff'].values                     #Extract averageInstantRunoff values
        runoffarray = xr.DataArray(runoffdata, dims=['time','hru'])            #Create an array of averageInstantRunoff with 2 dimensions
        ncconvert = ncconvert.drop('averageInstantRunoff')                           #Drop the original averageInstantRunoff variable
        ncconvert['averageInstantRunoff'] = runoffarray                           #Add the new array to original netCDF
        ncconvert['averageInstantRunoff'].attrs['long_name'] = "instantaneous runoff (instant)"
        ncconvert['averageInstantRunoff'].attrs['units'] = 'm s-1'

        print('Step 1: Creating '+str(x+1)+ ' HRU-only SUMMA output file out of ' + str(len(outfilelist)))
        ncconvert_outfile = os.path.join(convertdir, os.path.basename(outfilelist[x]))#Create an output filename
        ncconvert.to_netcdf(ncconvert_outfile, 'w')                                  #Write out the final netCDF file


    # Step 2: Concatenate GRU set by time

    timefilelist = glob.glob(convertdir+'/*.nc') #list of all files
    ncconcat_time = xr.open_mfdataset(timefilelist, concat_dim='time')     #Concatenates by time
    ncconcat_time = ncconcat_time.sortby('time')                           #Sorts by time
    ncconcat_time['hruId'] = ncconcat_time['hruId'].isel(time=0, drop=True)  #Dropping extra time dimension from hruId

    print('Step 2: Concatenating GRUset')
    finalfilename = os.path.join(outdir, finalfile)
    ncconcat_time.to_netcdf(finalfilename, 'w')

    print('Deleting folder and contents of convert')
    shutil.rmtree(convertdir)

