# EMG722-OpenSpace

The open space code was created using python 3 in Jupiter Notebook.  

2.1	Installing
Before the open space code can be used several packages and dependencies must be installed on the computer to allow the script access to the libraries and environments it needs to run. 
To install these libraries and environments the computer must have access to a package management system such as anaconda. Anaconda was the chosen package management system that was used in the creation of the open spaces script. The below steps show the process for installing anaconda and the required dependencies. 

Anaconda can be installed on a range of operating systems by locating the correct version from this url - https://docs.anaconda.com/anaconda/install/ and following the steps within the downloader. 

Once anaconda has been installed the programming environment has to be created. Anaconda allows the user to setup several programme environments which allows different decencies to be selected depending on the requirements of the program/script being run/created. 
To create a new program environment that will run the open spaces script in anaconda select the import button on the environments tab and navigate to the environment.yml file which is part of the open space’s repository on git hub (link in section 2.2). 
The yml file will then load all the required dependencies for the open space script into anaconda. The dependencies for the open space script are shown in the list below  below.

dependencies:
  - cartopy=0.18.0
  - fiona=1.8.18
  - geopandas=0.9.0
  - matplotlib-base=3.3.4
  - notebook=6.2.0
  - pandas=1.2.3
  - python=3.8.8
  - shapely=1.7.1

When the dependencies are loaded into anaconda it will also load additional packages that the dependencies are reliant on, so there will appear to be many more than the 8 listed below that are loaded into anaconda. 


These packages are then loaded into the script at the start, as shown in figure 2 below, if there are any issues when importing these packages see section 5.1 of the how to guide on this repository.

2.2	GitHub Repository 
The open space code is hosted on GitHub and can be accessed using the following URL - https://github.com/mckenzie-h/EMG722-OpenSpace.

2.3	Downloading Datasets
During the creation process for the open space script several open-source datasets were downloaded for use in the analysis process, although this information is not provided as part of the repository the datasets can easily be downloaded from the locations show in the list 1 below.

Dataset Name	Script Name	Source 	Source URL
Roads	NS_RoadLink	Ordnance Survey Open Data Portal	https://osdatahub.os.uk/
downloads/open/OpenRoads
Glasgow Boundary	GlasgowBoundary	Ordnance Survey Open Data Portal	https://osdatahub.os.uk/
downloads/open/BoundaryLine
Open Space	NS_GreenspaceSite	Ordnance Survey Open Data Portal	https://osdatahub.os.uk/
downloads/open/OpenGreenspace
Postcode Data	g_postcode_data	Scotland Census 	https://www.scotlandscensus.gov.uk/  
Table 1: Datasets downloaded for use within the script.

2.4	Data Preparation 
After the data had been downloaded some minor preparation work was carried out. 
•	The roads link dataset was selected out of several datasets that were within the full roads download. The links were chosen as these represented the linear roads. 
•	The Glasgow boundary was selected from a shapefile of all of the parish region boundary data, this was done in ArcGIS when viewing the original download. The original parish region dataset covered the whole of the UK when first downloaded. 
•	The open spaces dataset was not processed before use but was checked in ArcGIS for format and data quality. 
•	The postcode data was originally downloaded as a csv from Scotland Census and was converted into a shapefile in ArcGIS when checking the data for quality. 

