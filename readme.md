#### These scripts are written in Python and use the ArcPy module to perform geoprocessing tasks within ArcGIS Pro to find the points within a digital elevation model (DEM) that have the highest visibility.

The code reads in a digital elevation model of any area and a boundary polygon shapefile that defines the extent of the analysis area. Using this information, it determines which point has the highest visibility and saves the resulting rasters to a specified folder.

<img height="350" src="C:\Users\lilyb\OneDrive\Desktop\LOS tool pictures\Screenshot 2023-04-20 000731.png"/>

This code can be modified to run viewshed analysis on a higher or lower amount of points, for different heights of 'observers' or towers, and for any area.

If some of your area does not have access to cell service and you are using this script for a tower, or something else that requires cell service, you can run the **cellServiceMain** script that will only find points within cell service range. 

If you are limited to how far you can select a point from a road or trail, you can run the **roadsMain** script to identify locations within a specified distance of a road or trail.

<img height="350" src="C:\Users\lilyb\OneDrive\Desktop\LOS tool pictures\Screenshot 2023-04-20 000758.png"/>

Finally, you can modify the code to perform viewshed analysis for two points' combined visibility. This is useful if you have two towers, for example. To do this, you will want to run the **pairs** script.

<img height="350" src="C:\Users\lilyb\OneDrive\Desktop\LOS tool pictures\Screenshot 2023-04-20 000811.png"/>

The user can access coordinates for the selected point(s), as well as a raster with the visible area from that point(s).

Please feel free to view the tutorials about these scripts within the **Tutorials** folder as needed.