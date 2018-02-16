''' Utility functions for working with SUMMA'''

import glob, os
import xarray as xr
import shutil

def concatHRUspatially(outdir, outfile):
    '''
    Concatenates discrete HRUs spatially contained in outdir
    and produces a single outfile, e.g. final.nc
    '''
    outfilelist = glob.glob(outdir + '/*.nc')     #List of all files
    convertdir = os.path.join(outdir, 'convert')  
    os.makedirs(convertdir, exist_ok =True)      #Create a convert directory
    
    for count,value in enumerate(outfilelist):
        ncconvert = xr.open_dataset(outfilelist[count])                                  #Import each netCDF file

        runoffdata = ncconvert['averageInstantRunoff'].values                     #Extract averageInstantRunoff values
        runoffarray = xr.DataArray(runoffdata, dims=['time','hru'])            #Create an array of averageInstantRunoff with 2 dimensions
        ncconvert = ncconvert.drop('averageInstantRunoff')                           #Drop the original averageInstantRunoff variable
        ncconvert['averageInstantRunoff'] = runoffarray                           #Add the new array to original netCDF
        ncconvert['averageInstantRunoff'].attrs['long_name'] = "instantaneous runoff (instant)"
        ncconvert['averageInstantRunoff'].attrs['units'] = 'm s-1'

        print('Step 1: Creating '+str(count+1)+ ' HRU-only SUMMA output file out of ' + str(len(outfilelist)))
        ncconvert_outfile = os.path.join(convertdir, os.path.basename(outfilelist[count]))#Create an output filename
        ncconvert.to_netcdf(ncconvert_outfile, 'w') 
        
    spacefilelist = glob.glob(convertdir+'/*.nc')
    spacefilelist.sort()
    
    ncconcat_space = xr.open_mfdataset(spacefilelist, concat_dim='hru')

    concatfilename = os.path.join(outdir, outfile)   #Full dir + name of the final concatenated file

    ncconcat_space.to_netcdf(concatfilename, 'w')

    print('Step 2: Deleting temporary convert directory!')
    shutil.rmtree(convertdir)

    return concatfilename
