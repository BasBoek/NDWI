library(raster)

setwd("/home/user/NDWI/data")
b = raster("NDWI.tif")
projection(b)
plot(b)
