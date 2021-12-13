# Adopt-A-Pixel3km Notebooks

This repository will house Jupyter Notebooks that can be used for the Adopt-A-Pixel project.

## Local vs Colab
These notebooks can be run locally or on the cloud via [Google Colab](https://research.google.com/colaboratory/faq.html) (see `Open in Colab` buttons in each notebook). The Google Colab notebooks are intended to be plug-and-play with the primary cost of files being temporarily stored and runtime being disconnected after too much inactivity (for some notebooks you will have to install packages every time you use it). The local notebooks will require some setup on your end but allows permanent file storage on your computer, having it open as long as you want, and not having to install packages each time you run it.

## Required Software For Local installation
[Anaconda](https://docs.anaconda.com/anaconda/install/index.html) is necessary for you to download all the needed files.

Each folder containing a notebook has its own environment file with the packages needed for installation. If you are in the directory of that notebook you can run:
- `conda env create -f environment.yml`: To create the environment and download the necessary programs
- `conda env activate environment_name`: Activates the downloaded environment (`environment_name` is a placeholder for the name, look at notebook information to see what the value is)
-  `earthengine authenticate`: *Only if you are using the Geospatial Enrichment notebooks.* This authenticate Google Earth Engine.
- `jupyter lab`: To launch the jupyter notebook

## Available Notebooks
1. [AOI Generation](https://github.com/Piphi5/Adopt-a-Pixel3km-Notebooks/tree/main/AOI%20Generation) (Environment name: `aoi-generation`): This Jupyter Notebook should be used by each participant to generate their grid of points.
2. [CEO Project Generation](https://github.com/Piphi5/Adopt-a-Pixel3km-Notebooks/tree/main/CEO%20Project%20Generation) (Environment name: `ceo-generation`): This Jupyter Notebook workflow will take a folder of AOI CSV files and generate a csv to upload to CollectEarthOnline and one with individual plot assignments.
3. [CEO Post Processing](https://github.com/Piphi5/Adopt-a-Pixel3km-Notebooks/tree/main/CEO%20Post%20Processing) (Environment name: `ceo-processing`): This Jupyter Notebook workflow will take analyzed Collect Earth Online files and create PSU and SSU datasets. It also provides some visualizations and utilities (identifying missing plot ids, etc.). 
4. [CEO GO Join](https://github.com/Piphi5/Adopt-a-Pixel3km-Notebooks/tree/main/CEO%20GO%20Join) (Environment name: `globe-ceo-join`): This Jupyter Notebook workflow will take a folder of AOI CSV files and generate a csv to upload to CollectEarthOnline and one with individual plot assignments.
5. [Geospatial Enrichment](https://github.com/Piphi5/Adopt-a-Pixel3km-Notebooks/tree/main/Geospatial%20Enrichment) (Environment name: `geospatial-enrichment`): This Jupyter Notebook workflow will take a folder of AOI CSV files and generate a csv to upload to CollectEarthOnline and one with individual plot assignments.
