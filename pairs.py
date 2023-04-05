### SCRIPT STILL IN DEVELOPMENT####

# import required packages
import arcpy
from arcpy import env
from arcpy.sa import *
import csv
import pandas as pd
import os
import itertools

# allows arcpy to overwrite previous outputs
arcpy.env.overwriteOutput = True
# set workspace - replace this with your project workspace!
arcpy.env.workspace = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\SRER.gdb"
# crop input raster to bounds (DEM of general area via USGS) - replace this with your area's DEM!
uncropRaster = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\output_USGS30m.tif"
#boundary polygon for the extent of our area - replace this with your area's boundaries!
bounds = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\SRER.gdb\bounds"
cropRaster = ExtractByMask(uncropRaster, bounds)
cropRaster.save("C:\\Users\\lilyb\\OneDrive\\Documents\\ArcGIS\\Projects\\SRER\\SRER.gdb\\cropRaster")
# set input raster to cropped raster
in_raster = "C:\\Users\\lilyb\\OneDrive\\Documents\\ArcGIS\\Projects\\SRER\\SRER.gdb\\cropRaster"
# set feature class, can be any shapefile of points
points_class = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\SRER.gdb\selected_points"
fields = arcpy.ListFields(points_class)
for field in fields:
    print(field.name)

# initialize variables to keep track of the maximum visibility count and the combination of points with the highest count
max_count = -1
max_count_points = []

# loop through all possible combinations of points
for point1, point2 in itertools.combinations(arcpy.da.SearchCursor(points_class, ['OBJECTID']), 2):
    # create a where clause to select only the two points with these object IDs
    sql = "OBJECTID IN ({0},{1})".format(point1[0], point2[0])
    # create a layer with only these two points in it
    arcpy.management.SelectLayerByAttribute(points_class, "NEW_SELECTION", sql)
    # run visibility analysis, with in_raster and the selected points as observers
    outvis = arcpy.sa.Visibility(in_raster, points_class, analysis_type="OBSERVERS", nonvisible_cell_value="NODATA")
    # get the visibility count from the raster attribute table
    count_field = "Count"
    count_max = arcpy.management.GetRasterProperties
