# How to Find the Optimal Location for Virtual Fence Base Stations

## Requirements

License Requirements: 
    ArcGIS Pro >3.0 
    Spatial Analyst Extension

You must have ArcGIS Pro installed on your computer to run these Python scripts/Jupyter Notebooks, and you must have the Spatial Analyst extension enabled.

If you are not familiar with the ArcGIS Pro ArcPy package, please view the [What is ArcPy?](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/what-is-arcpy-.htm).

## What is this project?

<div>
    <img alt="Santa Rita Experimental Range Visibility Analysis" height="350" src="Images/img_3.png"/>
</div>

The code reads in a digital elevation model of any area and a boundary polygon shapefile that defines the extent of the analysis area. Using this information, it determines which point has the highest visibility and saves the resulting rasters to a specified folder. It determines the optimal location for a virtual fence base station, pair of base stations, base station only within cell service range, or base station only within a specified distance of a road or trail.

This code can be modified to run viewshed analysis on a higher or lower amount of points, for different heights of 'observers' or towers, and for any area.

If some of your area does not have access to cell service and you are using this script for a tower, or something else that requires cell service, you can run the **cellServiceMain** script that will only find points within cell service range. 

If you are limited to how far you can select a point from a road or trail, you can run the **roadsMain** script to identify locations within a specified distance of a road or trail.

Finally, you can modify the code to perform viewshed analysis for two points' combined visibility. This is useful if you have two towers, for example. To do this, you will want to run the **pairs** script.

The user can access coordinates for the selected point(s), as well as a raster with the visible area from that point(s).

Please feel free to view the tutorials about these scripts within the **Tutorials** folder as needed.

### References

McClaran, Mitchel P.; Angell, Deborah L.; Wissler, Craig. 2002. Santa Rita Experimental Range digital database: user’s guide. Gen. Tech. Rep. RMRS-GTR-100. Ogden, UT: U.S. Department of Agriculture, Forest Service, Rocky Mountain Research Station. 13 p.

United States Geological Survey (2021). United States Geological Survey 3D Elevation Program 1/3 arc-second Digital Elevation Model. Distributed by OpenTopography. https://doi.org/10.5069/G98K778D. Accessed: 2023-06-15