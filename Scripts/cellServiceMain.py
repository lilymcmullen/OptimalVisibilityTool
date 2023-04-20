# import required packages
import arcpy
from arcpy import env
from arcpy.sa import *
import csv
import pandas as pd
import os

# set workspace - replace this with your project workspace!
arcpy.env.workspace = r"C:\example\ArcGIS\Projects\folder\geodatabase.gdb"
# set location for raster files - replace this with a folder on your computer!
folder = r"C:\folderLocation"
# crop input raster to bounds (DEM of general area via USGS) - replace this with your area's DEM!
uncropRaster = r"C:\RasterDEM"
#boundary polygon for the extent of our area - replace this with your area's boundaries!
bounds = r"C:\boundaryPolygon"

# allows arcpy to overwrite previous outputs
arcpy.env.overwriteOutput = True

#crop raster to boundary to create cropped raster
cropRaster = ExtractByMask(uncropRaster, bounds)
cropRaster.save("cropRaster")

# specify input feature classes- using AT&T and Verizon cell service shapefiles. You can download these from
# https://fcc.maps.arcgis.com/apps/webappviewer/index.html?id=6c1b2e73d9d749cdb7bc88a0d1bdd25b
# these specific shapefiles are only covering America.
input_fc1 = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\ATT_Mobile.shp"
input_fc2 = r"C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\Verizon_Wireless.shp"

#crop each shapefile to the area you are working with

input_poly = input_fc2
cropinput_fc1 = "ATTcrop"
cropinput_fc2 = "VWcrop"
# Create a new output polygon file name
output_poly1 = cropinput_fc1
output_poly2 = cropinput_fc2
# Use the clip tool to clip the input polygon to the clip boundary
arcpy.Clip_analysis(input_fc1, bounds, output_poly1)
arcpy.Clip_analysis(input_fc2, bounds, output_poly2)

#now, merge these polygons together so you get a total service area!
# create a new feature class to store the merged polygon
output_fc = "merged_service"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, output_fc, "POLYGON")

# create a list of the input feature classes
input_fcs = [cropinput_fc1, cropinput_fc2]

# use Union_analysis tool to merge the polygons
arcpy.analysis.Union(input_fcs, output_fc)

# merged polygon of ATT and VW range is created and saved to your workspace.

#now we will clip the cropped raster to the extent of the cell service range polygon

cellRaster = arcpy.sa.ExtractByMask(cropRaster, output_fc)

# Save the final cropped raster to a new file
cellRaster.save("cellRaster")

# point selection: please view tutorial on https://github.com/lilymcmullen/Best_LOS_Tool for point selection options!
feature_class = r'C:\Users\lilyb\OneDrive\Documents\ArcGIS\Projects\SRER\SRER.gdb\highest_pts'

in_raster = cellRaster
feature_class = arcpy.defense.FindLocalPeaksValleys(in_raster, feature_class, "PEAKS", 15)

# assign ID field
field = 'OBJECTID'
# list all object IDs (from field = 'OBJECTID'
all_object_ids = [row[0] for row in arcpy.da.SearchCursor(feature_class, field)]
# Find the object ID fieldname
objectidfield = arcpy.Describe(feature_class).OIDFieldName

# Set the path for the new folder relative to the current workspace
folder_name = "visibOutputsCell"
folder_path = os.path.join(folder, folder_name)

# Create the new folder if it doesn't already exist
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
    print(f"Folder '{folder_name}' created successfully!")

# Set the current workspace to the new folder
arcpy.env.workspace = folder_path
# looping through the points
for pointid in all_object_ids:  # For each object id in the object id list
    # create a where clause to select only the point with this object ID
    sql = "{0}={1}".format(arcpy.AddFieldDelimiters(datasource=feature_class, field=objectidfield), pointid)
    # create a layer with only this point in it
    arcpy.MakeFeatureLayer_management(in_features=feature_class, out_layer='templayer', where_clause=sql)
    # run visibility analysis, with in_raster and templayer as observer. observer height is 6 (meters)
    outvis = arcpy.sa.Visibility(cellRaster, 'templayer', analysis_type="OBSERVERS", nonvisible_cell_value="NODATA", observer_offset=6)
    # name the objects using object ID
    # I named them visibility_analysis_1.tif, visibility_analysis_2.tif etc...
    output_raster_name = os.path.join(folder_path,
                                      "visiblity_analysis_{0}.tif".format(pointid))
    # save output raster with name called in above
    outvis.save(output_raster_name)

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