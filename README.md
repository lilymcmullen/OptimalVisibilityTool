# How to Find the Optimal Location for Virtual Fence Base Stations

## Requirements

License Requirements: 
- ArcGIS Pro >3.0 
- Spatial Analyst Extension

You must have ArcGIS Pro installed on your computer to run these Python scripts/Jupyter Notebooks, and you must have the Spatial Analyst extension/license enabled.

These scripts use ArcPy, a Python site-package that allows you to run ArcGIS geo-processing tools and other ArcGIS functionality from Python. If you are not familiar with the ArcPy package, please view the [What is ArcPy?](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/what-is-arcpy-.htm).

***These Jupyter Notebooks are intended to be run inside of ArcGIS Pro with the Spatial Analysis extension/license. It is not intended to be run in a Jupyter Notebook outside of ArcGIS Pro.***

## What is this project?

<div>
    <img alt="Santa Rita Experimental Range Visibility Analysis" height="350" src="Images/SRER-Radio-Coverage.png"/>
</div>

The goal of this project is to determine the optimal placement for a virtual fence base station to provide optimal radio coverage across your area of interest. There are multiple scripts/notebooks to analyse different placement options, such as a single base station, a pair of base stations, placing a base station only within cell service, or base station only within a specified distance of a road or trail. Each of these options is explained in more detail below.

## How it Works

The code reads in a digital elevation model (DEM) from your area of interest, finds peaks (e.g., hills, mountains) within your area, and performs a visibility analysis for each of these peaks. It then generates a raster for each of the peaks, and models how much of your area of interest is visible from each of these peaks. The amount of area visible in each raster is an approximation for the radio coverage provided by a virtual fence base station, or pair of virtual fence base stations. Actual radio coverage may vary by a number of factors, such as terrain, signal attenuation and reflectance, and vegetation cover. This code can be modified to run a viewshed analysis on a higher or lower amount of points, for different antenna heights, and for any area.

An example DEM and boundary shapefile of the Santa Rita Experimental Range is provided in each notebook, but you will need to provide a DEM and a boundary shapefile for your area of interest. There is a tutorial [HowtoFindYourDEM.md](/Tutorials/HowToFindYourDEM.md) in the "Tutorials" folder that provides some help on how to locate a DEM for your area of interest. The boundary shapefile is a polygon that defines the extent of the analysis area. If you have permission to place a virtual fence base station on land surrounding your area, such as on a nearby mountain that may not be within your grazing area, use a shapefile that includes those potential areas outside your grazing area. Doing so will give you more potential placements for your virtual fence base station and likely will give you better radio coverage.

## Overview of Scripts

If you want to find the optimal placement for a single virtual fence base station, you can run the Jupyter Notebook [Find-Optimal-Location-for-Single-Base-Station.ipynb](https://github.com/lilymcmullen/OptimalVisibilityTool/blob/master/Notebooks/Find-Optimal-Location-for-Single-Base-Station.ipynb).

If some of your area does not have access to cell service and you are using this script for a base station, or something else that requires cell service, you can run the [Find-Optimal-Location-for-Single-Base-Station-Within-Cell-Service.ipynb](https://github.com/lilymcmullen/OptimalVisibilityTool/blob/master/Notebooks/Find-Optimal-Location-for-Single-Base-Station-Within-Cell-Service.ipynb) script that will only find potential base station placements within cell service range. 

If you are limited to how far you can place a base station from a road or trail, you can run the [Find-Optimal-Location-for-Single-Base-Station-Along-a-Road.ipynb](https://github.com/lilymcmullen/OptimalVisibilityTool/blob/master/Notebooks/Find-Optimal-Location-for-Single-Base-Station-Along-a-Road.ipynb) script to identify locations within a specified distance from a road or trail.

If you have two virtual fence base stations, and you can run [Find-Optimal-Location-for-Pair-of-Base-Stations.ipynb](https://github.com/lilymcmullen/OptimalVisibilityTool/blob/master/Notebooks/Find-Optimal-Location-for-Pair-of-Base-Stations.ipynb) to estimate the radio coverage from two base stations.

Each script/notebook provides instructions on how to run it.

### References

McClaran, Mitchel P.; Angell, Deborah L.; Wissler, Craig. 2002. Santa Rita Experimental Range digital database: user’s guide. Gen. Tech. Rep. RMRS-GTR-100. Ogden, UT: U.S. Department of Agriculture, Forest Service, Rocky Mountain Research Station. 13 p.

United States Geological Survey (2021). United States Geological Survey 3D Elevation Program 1/3 arc-second Digital Elevation Model. Distributed by OpenTopography. https://doi.org/10.5069/G98K778D. Accessed: 2023-06-15