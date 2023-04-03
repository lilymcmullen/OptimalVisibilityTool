# import required packages
import arcpy
from arcpy import env
from arcpy.sa import *
import os
from osgeo import gdal
import itertools
from itertools import permutations
import pandas as pd

# allows arcpy to overwrite previous outputs
arcpy.env.overwriteOutput = True
# set workspace
arcpy.env.workspace = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\SRER.gdb"
# crop input raster to bounds (DEM of general area via USGS)
uncropRaster = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\output_USGS30m.tif"
bounds = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\SRER.gdb\bounds"
cropRaster = ExtractByMask(uncropRaster, bounds)
cropRaster.save("C:\\Users\\lilyb\\OneDrive\\Documents\\ArcGIS\\Projects\\SRER\\SRER.gdb\\cropRaster")
# set input raster to cropped raster
in_raster = "C:\\Users\\lilyb\\OneDrive\\Documents\\ArcGIS\\Projects\\SRER\\SRER.gdb\\cropRaster"
# set feature class, can be any shapefile of points
points_class = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\SRER.gdb\selected_points"
feature_class = arcpy.defense.FindLocalPeaksValleys(in_raster, points_class, "PEAKS", 15)
# so we can call ID field
field = 'OBJECTID'
# list all object IDs (from field = 'OBJECTID'
all_object_ids = [row[0] for row in arcpy.da.SearchCursor(feature_class, field)]
# Find the object ID fieldname
objectidfield = arcpy.Describe(feature_class).OIDFieldName
# looping through the points
for pointid in all_object_ids:  # For each object id in the object id list
    # create a where clause to select only the point with this object ID
    sql = "{0}={1}".format(arcpy.AddFieldDelimiters(datasource=feature_class, field=objectidfield), pointid)
    # create a layer with only this point in it
    arcpy.MakeFeatureLayer_management(in_features=feature_class, out_layer='templayer', where_clause=sql)
    # run visibility analysis, with in_raster and templayer as observer
    outvis = arcpy.sa.Visibility(in_raster, 'templayer', analysis_type="OBSERVERS", nonvisible_cell_value="NODATA")
    # name the objects using object ID
    # I named them visibility_analysis_1.tif, visibility_analysis_2.tif etc...
    output_raster_name = os.path.join(r"C:\Users\lilyb\OneDrive\Desktop\visibout",
                                      "visiblity_analysis_{0}.tif".format(pointid))
    # save output raster with name called in above
    outvis.save(output_raster_name)

# set the environment to the folder with output rasters
env = r"C:\Users\lilyb\OneDrive\Desktop\visibout"

# create an empty list to store the dataframes
dfs = []

# loop through all raster files in the input directory
for raster in arcpy.ListRasters():
    # convert the raster to a numpy array
    arr = arcpy.RasterToNumPyArray(raster)
    # convert the numpy array to a pandas dataframe
    df = pd.DataFrame(arr)
    # add the dataframe to the list
    dfs.append(df)

# find the point with max visibility from the dataframe
best_point = max(dfs)
print(best_point)

