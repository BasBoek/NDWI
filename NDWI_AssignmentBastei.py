#Import required modules
import os  # for finding the working directory
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32

# Register the drivers
print "the GDAL version"
print(gdal.__version__)
gdal.AllRegister()

# Get working directory to double check in which directory we are working
os.getcwd()

# Choose the driver type
driver = gdal.GetDriverByName('GTiff')

# Import the landsat input data
filename4 = 'data/LC81980242014260LGN00_sr_band4.tif'
filename5 = 'data/LC81980242014260LGN00_sr_band5.tif'
dataSource4 = gdal.Open(filename4, GA_ReadOnly)
dataSource5 = gdal.Open(filename5, GA_ReadOnly)

# Make arrays of the inputdata
band4Arr = dataSource4.ReadAsArray(0,0,dataSource4.RasterXSize, dataSource4.RasterYSize)
band5Arr = dataSource5.ReadAsArray(0,0,dataSource5.RasterXSize, dataSource5.RasterYSize)

# Making float values
import numpy as np
band4Arr=band4Arr.astype(np.float32)
band5Arr=band5Arr.astype(np.float32)

# Some information about the distribution of the values of the datasets 
print "max min mean band 4"
print band4Arr.max()
print band4Arr.min()
print band4Arr.mean()

print "max min mean band 5"
print band5Arr.max()
print band5Arr.min()
print band5Arr.mean()

# Replace all negative numbers by "0" values in order to filter nodata (-9999) and other negative values which make no sense for reflectences.
band4Arr[band4Arr < 0] =0
band5Arr[band5Arr < 0] =0

# Calculating the NDWI values for all the not nodatavalues. Also band4+ band 5 together cannot be 0 as division by zero is not possible.
mask = np.greater(band4Arr+band5Arr,0)
NDWI = np.choose(mask,(-99,(band4Arr-band5Arr)/(band4Arr+band5Arr)))

# Information about NDWI values
print "max min mean NDWI"
print NDWI.max()
print NDWI.min()
print NDWI.mean()

# Create .tif output file
outDataSet=driver.Create('data/NDWI.tif', dataSource4.RasterXSize, dataSource4.RasterYSize, 1, GDT_Float32)
outBand = outDataSet.GetRasterBand(1)
outBand.WriteArray(NDWI,0,0)
outBand.SetNoDataValue(-99)

# Set projection
outDataSet.SetProjection(dataSource4.GetProjection())

# Saving it
outBand.FlushCache()
outDataSet.FlushCache()
