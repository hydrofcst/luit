'''Utilities for spatial operations'''
import geopandas as gpd

def subShp(shapefile, subsetvar, subsetarray):
    '''
    Reads a shapefile, subsets for an array and converts to EPSG:4326 projection
    '''
    shpdat = gpd.read_file(shapefile)
    shpsubset = shpdat[shpdat[subsetvar].isin(subsetarray)]
    shpsubset = shpsubset.to_crs({'init': 'epsg:4326'})
    return shpsubset
