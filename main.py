# import required packages
import arcpy
from arcpy import env
from arcpy.sa import *
import csv
import pandas as pd
import os

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
feature_class = arcpy.defense.FindLocalPeaksValleys(in_raster, points_class, "PEAKS", 15)
#see if we can clip the raster to the cell service raster and also clip the raster to road buffer
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
    # run visibility analysis, with in_raster and templayer as observer. observer height is 6 (meters)
    outvis = arcpy.sa.Visibility(in_raster, 'templayer', analysis_type="OBSERVERS", nonvisible_cell_value="NODATA", observer_offset=6)
    # name the objects using object ID
    # I named them visibility_analysis_1.tif, visibility_analysis_2.tif etc...
    output_raster_name = os.path.join(r"C:\Users\lilyb\OneDrive\Desktop\visibout",
                                      "visiblity_analysis_{0}.tif".format(pointid))
    # save output raster with name called in above
    outvis.save(output_raster_name)

# Set the workspace environment to the folder containing the rasters
arcpy.env.workspace = r"C:\Users\lilyb\OneDrive\Desktop\visibout"

# Use the ListRasters function to create a list of rasters in the folder
rasters = arcpy.ListRasters()

# Initialize variables to keep track of the maximum count value and the name of the raster with the maximum count value
max_count = -1
max_count_raster = ""

# Iterate through the list of rasters
for raster in rasters:
    # Create a unique filename for the output dataframe
    output_filename = f"{raster}_table.csv"

    # Get the raster attribute table as a table view
    table_view_name = f"{raster}_view"
    table_view = arcpy.MakeTableView_management(raster, table_view_name)

    # Get the Count value from each raster table using a SearchCursor
    count_field = "Count"
    with arcpy.da.SearchCursor(table_view, count_field) as cursor:
        count_values = [row[0] for row in cursor]

    # Find the maximum count value
    count_max = max(count_values)

    # Check if the Count value is greater than the current maximum count value
    if count_max > max_count:
        # If so, update the maximum count value and the name of the raster with the maximum count value
        max_count = count_max
        max_count_raster = raster

    # Convert the table view to a Pandas dataframe
    dataframe = pd.DataFrame.from_records(arcpy.da.TableToNumPyArray(table_view, count_field))

    # Save the dataframe to a file
    dataframe.to_csv(output_filename, index=False)

    # Print a message indicating the dataframe has been saved
    print(f"{output_filename} saved successfully.")

# Print the name of the raster with the maximum count value
print(f"Raster with the highest visibility is {max_count_raster} with a count of {max_count}")