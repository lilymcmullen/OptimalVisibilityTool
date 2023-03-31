# import required packages
import arcpy
from arcpy import env
from arcpy.sa import *
import os
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
feature_class = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\SRER.gdb\selected_points"
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
    outvis = arcpy.sa.Visibility(in_raster, 'templayer')
    # name the objects using object ID
    # I named them visibility_analysis_1.tif, visibility_analysis_2.tif etc...
    output_raster_name = os.path.join(r"C:\Users\lilyb\OneDrive\Desktop\visibout",
                                      "visiblity_analysis_{0}.tif".format(pointid))
    # save output raster with name called in above
    outvis.save(output_raster_name)
all_rasters = arcpy.ListRasters("*visibility*", "TIF")
for raster in all_rasters:

#Loop that adds 1 to each raster in the folder
#Find raster with max visible values
#Loop through each combination of max raster and other raster and run diff
#Store values into a new data frame -> value '2' is new coverage from second raster that "max" raster does not have
#Print raster combination with highest '2' value (most new coverage)
#Yay.
