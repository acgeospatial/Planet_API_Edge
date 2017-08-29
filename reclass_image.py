#!/usr/bin/python
# -*- coding: utf-8 -*-
## Written by Andrew Cutts

from osgeo import gdal
import numpy
### open the raster
gdalData = gdal.Open("....edges.jpg")
### read into array
raster = gdalData.ReadAsArray()

#reclassify raster values using Numpy! in this case less and greater functions
temp = numpy.less(raster, 10)
numpy.putmask(raster, temp, 0)
temp = numpy.greater_equal(raster, 10)
numpy.putmask(raster, temp, 1)

# write results to file (lets set it to tif)
format = "GTiff"
driver = gdal.GetDriverByName(format)

# CreateCopy() method instead of Create() to save our time as the raster is the same only the extension is changing
outDataRaster = driver.CreateCopy("...edges_reclass.tif", gdalData, 0)
outDataRaster.GetRasterBand(1).WriteArray(raster)
