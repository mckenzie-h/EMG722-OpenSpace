#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing required libaries for code to run

get_ipython().run_line_magic('matplotlib', 'notebook')

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import fiona
import os
from shapely.geometry import Point, LineString, Polygon


plt.ion() # makes the plotting of the map interactive

# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

    
#Create variable for open spaces dataset and load data

openspace_data = gpd.read_file(r'C:\Users\angel\Programming\Project\Data\NS_GreenspaceSite.shp')

#Create variable for boundary dataset and load data, this example uses Glasgow as an area of interest

boundary_data = gpd.read_file(r'C:\Users\angel\Programming\Project\Data\GlasgowBoundary.shp')

#Create variable for roads dataset and load data

road_data = gpd.read_file(r'C:\Users\angel\Programming\Project\Data\NS_RoadLink.shp')

#Create Variable for glasgow postcode data 

postcode_g = gpd.read_file (r'C:\Users\angel\Programming\Project\Data\g_postcode_data.shp')


# In[2]:


#display open space dataset table

openspace_data


# In[3]:


#Display Boundary dataset table

boundary_data


# In[4]:


#Display road dataset table 

road_data


# In[5]:


#display postcode dataset table

postcode_g


# In[6]:


# Check co-ordinate reference systems for openspace layers

openspace_data.crs


# In[7]:


# Check co-ordinate reference systems for boundary layer

boundary_data.crs


# In[8]:


# Check co-ordinate reference systems for roads layer

road_data.crs


# In[9]:


#check co-ordinate reference systsem for postcode layer 

postcode_g.crs


# In[10]:


#Clip the open space dataset to the extent of the project boundary layer, using geopandas clip function 

# Clip data
openspace_glasgow = gpd.clip(openspace_data, boundary_data)

# Ignore missing/empty geometries
openspace_glasgow = openspace_glasgow[~openspace_glasgow.is_empty]

#Print number of rows in new clipped dataset compared to original dataset. Ensures that clip has worked.
print("The clipped data has fewer polygons (represented by rows):",
      openspace_glasgow.shape, openspace_data.shape)

#export clipped open space dataset into ESRI shapefile into data folder

openspace_glasgow.to_file('C:\\Users\\angel\\Programming\\Project\\Data\\openspace_glasgow.shp', driver = 'ESRI Shapefile')


# In[11]:


#Clip the roads dataset to the extent of the project boundary layer, using geopandas clip function 

# Clip data
road_glasgow = gpd.clip(road_data, boundary_data)

# Ignore missing/empty geometries
road_glasgow = road_glasgow[~road_glasgow.is_empty]

#Print number of rows in new clipped dataset compared to original dataset. Ensures that clip has worked.
print("The clipped data has fewer line sections (represented by rows):",
      road_glasgow.shape, road_data.shape)

#export clipped road dataset into ESRI Shapefile into data folder

road_glasgow.to_file('C:\\Users\\angel\\Programming\\Project\\Data\\road_glasgow.shp', driver = 'ESRI Shapefile')


# In[12]:


# identify the number of open space functions in the dataset to identify how many colours are required for symboloisation 
num_openspace = len(openspace_glasgow.function.unique())
print('Number of unique Open Space Types: {}'.format(num_openspace))
print(openspace_glasgow['function'].unique())


# In[13]:


# Identify the number of unique road types in the roads datasetto identify how many colours are required for symboloisation 
num_road = len(road_glasgow.function.unique())
print('Number of unique road classes: {}'.format(num_road)) 


# In[14]:


myFig = plt.figure(figsize=(16, 8))  # create a figure of size 10x10 (representing the page size in inches)

myCRS = ccrs.UTM(30)  # create a Universal Transverse Mercator reference system to transform our data.
# be sure to fill in XX above with the correct number for the area we're working in.

ax = plt.axes(projection=ccrs.Mercator())  # finally, create an axes object in the figure, using a Mercator
# projection, where we can actually plot our data.


# In[15]:


# first, we just add the outline of glasgow city council using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(boundary_data['geometry'], myCRS, edgecolor='yellow', facecolor='w')
xmin, ymin, xmax, ymax = boundary_data.total_bounds
ax.add_feature(outline_feature) # add the features we've created to the map.

# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS) # because total_bounds gives output as xmin, ymin, xmax, ymax,

#add gridlines to the map, turning off the top and rightside labels 
gridlines = ax.gridlines(draw_labels=True, color='black', alpha=0.6, linestyle='--')
gridlines.right_labels =False # turn off the right side labels
gridlines.top_labels =False # turn off the top labels

myFig # re-display the figure here.


# In[16]:


#add title to map figure
plt.title('Glasgow Open Spaces')


# In[17]:


#create colours for the open space types - for this dataset 10 colours need to be identified

openspace_colors = ['lightgreen','palevioletred', 'crimson', 'dimgrey', 'lime', 'darkorchid', 'darkorange', 'hotpink', 'indigo', 'aqua'  ]

# get a list of unique names for the Open Space type
openspace_types = list(openspace_glasgow.function.unique())

# sort the open space types alphabetically by name
openspace_types.sort() 

# add the open spaces data to the map

for i, openspace in enumerate(openspace_types):
    feat = ShapelyFeature(openspace_glasgow['geometry'][openspace_glasgow['function'] == openspace], myCRS, 
                        edgecolor='black',
                        facecolor=openspace_colors[i],
                        linewidth=1,
                        alpha=0.25)
    ax.add_feature(feat)


# In[18]:


#add roads layer to map 
road_colors = ['darkslategrey', 'navy', 'silver', 'darkmagenta', 'sienna', 'darkred', 'darkgoldenrod', 'olive']

# get a list of unique road types from the function attribute for the roads dataset
road_types = list(road_glasgow.function.unique())

# sort the open space types alphabetically by name
road_types.sort() 

# add the road data to the map
for i, road in enumerate(road_types):
    road_feat = ShapelyFeature(road_glasgow['geometry'][road_glasgow['function'] == road], myCRS, 
                                edgecolor='black',
                                facecolor=road_colors[i],
                                linewidth=0.25)
    ax.add_feature(road_feat)
    


# In[19]:


# generate a list of handles for the openspace dataset
openspace_handles = generate_handles(openspace_types, openspace_colors, alpha=0.25)

#  generate a list of handles for the road dataset
road_handles = generate_handles(road_types, road_colors, alpha=0.25)

#generate handle for boundary data
#boundary_handle = [mpatches.Patch([], [], edgecolor='yellow')]

#ax.legend() takes a list of handles and a list of labels corresponding to the objects you want to add to the legend
handles = openspace_handles + road_handles #+ boundary_handle
                                
labels = openspace_types + road_types #+ 'Glasgow Boundary'

leg = ax.legend(handles, labels, title='Legend', title_fontsize=12, 
               fontsize=10, loc='upper right',bbox_to_anchor=(1.5, 1), frameon=True, framealpha=1)


myFig #show the updated figure


# In[20]:


#save the map as a png file
myFig.savefig('Glasgow_OpenSpace_Map.png', dpi=300)


# In[21]:


##Now we can see the map of the relevent openspace and road data within the Glasgow City Council Area, analysis can be carried out to interegate the data and find out more about the openspaces and roads within Glasgow 

# Create a new column within the openspace glasgow called area and populate it with the area in m2 for each 
# Area / 1000 to get total area in km2
openspace_glasgow['area km'] = openspace_glasgow.area/1000


# In[22]:


#Display the openspace glasgow table with the added areas column
openspace_glasgow


# In[23]:


#run the a groupby with count operation on the glasgow road layer to identify the number of each type of road in the glasgow area
openspace_groupcount = openspace_glasgow.groupby('function')['function'].count()

#Display the open space group with count by table
openspace_groupcount


# In[24]:


#run the a group by operation on the glasgow open space layer to identify the number of each type of open space in the glasgow area
openspace_group = openspace_glasgow.groupby('function')

#Display the open space group by table
openspace_group


# In[25]:


#Print to show user that group 
print('Groupby Successful')


# In[26]:


#for key values in the open space groups create indivadual tables
for key, values in openspace_group:
    openspace_type = values

openspace_type.head()
#display a sample table of the openspace table seperated by key values 


# In[27]:


#Create individual shapefiles for the types of openspace data. 
#determind output folder location
outFolder = r'C:\Users\angel\Programming\Project\Data'

# Create a new folder called 'results' (if does not exist already) to cretae the folder use os.makedirs() function
resultFolder = os.path.join(outFolder, 'results')
if not os.path.exists(resultFolder):
    os.makedirs(resultFolder)

# Iterate over the key values in the open space group to create seperate shapefiles for each
for key, values in openspace_group:
    # Format the filename (replace spaces with underscores)
    outName = "%s.shp" % key.replace(" ", "_")

    # Print some information for the user
    print("Processing: %s" % key)

    # Create an output path
    outpath = os.path.join(resultFolder, outName)

    # Export the data
    values.to_file(outpath)
    
    #print finishing statement to ensure shapefiles have be saved
    print('Shapefile Saved') 
    


# In[28]:


#display the length of each road section in the road dataset
road_glasgow.length


# In[29]:


# Create a new column within the road_glasgow called length and populate it with the length in meters for each 
road_glasgow['length - m'] = road_glasgow.length


# In[30]:


#display the updated road glasgow with the length field included in the table 
road_glasgow


# In[31]:


#run the a group by operation on the glasgow open space layer to identify the number of each type of open space in the glasgow area
road_groupcount = road_glasgow.groupby('function')['function'].count()

#Display the open space group with count by table
road_groupcount


# In[32]:


#run the a group by operation on the glasgow road layer to identify the number of each type of open space in the glasgow area
road_group = road_glasgow.groupby('function')

#Display the open space group by table
road_group
print('Groupby Successful')


# In[33]:


#Create individual shapefiles for the types of road data. 
#determind output folder location
outFolder = r'C:\Users\angel\Programming\Project\Data'

# Create a new folder called 'Results' (if does not exist) to that folder using os.makedirs() function
resultFolder = os.path.join(outFolder, 'results')
if not os.path.exists(resultFolder):
    os.makedirs(resultFolder)

# Iterate over the
for key, values in road_group:
    # Format the filename (replace spaces with underscores)
    outName = "%s.shp" % key.replace(" ", "_")

    # Print some information for the user
    print("Processing: %s" % key)

    # Create an output path
    outpath = os.path.join(resultFolder, outName)

    # Export the data
    values.to_file(outpath)
    
    #print finishing statement to ensure shapefiles have be saved
    print('Shapefiles Saved')


# In[34]:


#Call in the new shapefiles which are going to be use in the analysis

#public spaces
openspace_public = gpd.read_file(r'C:\Users\angel\Programming\Project\Data\results\Public_Park_Or_Garden.shp')

#playing field
openspace_field = gpd.read_file(r'C:\Users\angel\Programming\Project\Data\results\Playing_Field.shp')

#play space
openspace_play = gpd.read_file(r'C:\Users\angel\Programming\Project\Data\results\Play_Space.shp')


# In[35]:


#calcualte the total area of public Gardens or Parks within the Glasgow City Council Boundary 
total_publicarea = openspace_public['area km'].sum()

print ('The total area -km2- for all Public Gardens of Parks within Glasgow City is:', total_publicarea)


# In[36]:


#calcualte the total area of public Gardens or Parks within the Glasgow City Council Boundary 
total_playarea = openspace_play['area km'].sum()

print('The total area -km2- for all Play Spaces within Glasgow City is:',total_playarea)


# In[37]:


#calcualte the total area of public Gardens or Parks within the Glasgow City Council Boundary 
total_fieldarea = openspace_field['area km'].sum()

print('The total area -km2- for all Playing Fields within Glasgow City is:',total_fieldarea)


# In[38]:


#buffer open space polygons

#create 100m buffer around the public open spaces
openpublic_300 = openspace_public.buffer(300)

#create 100m buffer around playing fields
openfield_300 = openspace_field.buffer(300)

#create 100m buffer aroung play spaces 
openplay_300 = openspace_play.buffer(300)

#save 100m buffer of open space public to file
openpublic_300.to_file('C:\\Users\\angel\\Programming\\Project\\Data\\openpublic_100m_buffer.shp', driver = 'ESRI Shapefile')

#save 100m buffer of open space public to file
openfield_300.to_file('C:\\Users\\angel\\Programming\\Project\\Data\\openfield_100m_buffer.shp', driver = 'ESRI Shapefile')

#save 100m buffer of open space public to file
openplay_300.to_file('C:\\Users\\angel\\Programming\\Project\\Data\\openplay_100m_buffer.shp', driver = 'ESRI Shapefile')

#print statement to ensure save has worked 
print ('Save Complete')


# In[39]:


# clip g_postcode_data to glasgow city council boundary
# Clip data
postcode_glasgow = gpd.clip(postcode_g, boundary_data)

# Ignore missing/empty geometries
postcode_glasgow = postcode_glasgow[~postcode_glasgow.is_empty]

#save glasgow postcode data to file
postcode_glasgow.to_file('C:\\Users\\angel\\Programming\\Project\\Data\\postcode_glasgow.shp', driver = 'ESRI Shapefile')


# In[40]:


#Calcualate the total number of postcodes within Glasgow City Council 
postcode_count = postcode_glasgow['Field1'].count()

print('The total number of postcodes within GLasgow City Council is:',postcode_count)


# In[41]:


#Calculate the population within Glasgow City Council 

total_pop = postcode_count *13 *2.7 # 13 is the average households within a poualation area, 2.7 is the average houshold sive within glasgow city council.

print ('The approximate Population within Glasgow City Council is:', total_pop)


# In[42]:


#clip postcode data to those inside the 100m buffer of the open space

# Clip data
postcode_play300 = gpd.clip(postcode_glasgow, openplay_300)

# Ignore missing/empty geometries
postcode_play300 = postcode_play300[~postcode_play300.is_empty]

#save glasgow postcode data to file
postcode_play300.to_file('C:\\Users\\angel\\Programming\\Project\\Data\\postcode_glasgow.shp', driver = 'ESRI Shapefile')


# In[43]:


#Calcualate the total number of postcodes within Glasgow City Council taht fall within 100m of a playspace 
postcode_playcount = postcode_play300['Field1'].count()

print('The total number of postcodes within 300m of a play space within GLasgow City Council is:',postcode_playcount)


# In[44]:


#Calulate the approximate population within 100m of a play space
play300_pop = postcode_playcount *13 *2.5 

print('The approx Population within 300m of a Play Space is:', play300_pop)


# In[45]:


#clip postcode data to those inside the 100m buffer of the open space

# Clip data
postcode_field300 = gpd.clip(postcode_glasgow, openfield_300)

# Ignore missing/empty geometries
postcode_field300 = postcode_field300[~postcode_field300.is_empty]

#save glasgow postcode data to file
postcode_field300.to_file('C:\\Users\\angel\\Programming\\Project\\Data\\postcode_glasgow.shp', driver = 'ESRI Shapefile')


# In[46]:


#Calcualate the total number of postcodes within Glasgow City Council 
postcode_fieldcount = postcode_field300['Field1'].count()

print('The total number of postcodes within 300m of a Playing field is:', postcode_fieldcount)


# In[47]:


#Calulate the approximate population within 100m of a playing field
field300_pop = postcode_fieldcount *13 *2.5 

print('The approximate Population within 300m of a Playing Field is:', field300_pop)


# In[48]:


#clip postcode data to those inside the 100m buffer of the open space

# Clip data
postcode_public300 = gpd.clip(postcode_glasgow, openpublic_300)

# Ignore missing/empty geometries
postcode_public300 = postcode_public300[~postcode_public300.is_empty]

#save glasgow postcode data to file
postcode_public300.to_file('C:\\Users\\angel\\Programming\\Project\\Data\\postcode_glasgow.shp', driver = 'ESRI Shapefile')


# In[49]:


#Calcualate the total number of postcodes within Glasgow City Council 
postcode_publiccount = postcode_public300['Field1'].count()

print('The total number of postcodes within 300m of a Public Park or Garden is:',postcode_publiccount)


# In[50]:


#Calulate the approximate population within 100m of a playing field
public300_pop = postcode_publiccount *13 *2.5 

print('The approximate Population within 300m of a Playing Field is:', public300_pop)

