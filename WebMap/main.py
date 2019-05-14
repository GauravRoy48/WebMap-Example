##################################################################################
# Creator     : Gaurav Roy
# Date        : 14 May 2019
# Description : The code contains the basic methodolgy to create a WebMap using
#               Folium. The code creates 2 feature groups: Volcano data for West
#               USA and World Population. Each feature group can be toggled using 
#               the LayerControl() function provided by Folium.
##################################################################################

import folium # Need to install first: pip install folium
import pandas as pd


volcanoes = pd.read_csv('Volcanoes.txt') # Import the Volcanoes.txt file which contains volcano data
# generate multiple list items for use in Feature Group fg1
lat = list(volcanoes["LAT"])
lon = list(volcanoes["LON"])
elev = list(volcanoes["ELEV"])
name = list(volcanoes["NAME"])
status = list(volcanoes["STATUS"])
typ = list(volcanoes["TYPE"])

# html text to define the popup parameter in folium.Marker()
html = """
<h4>Volcano information:</h4>
Volcano name: 
<a href="https://www.google.com/search?q=%s volcano" target="_blank"> %s</a><br>
Height: %s m<br>
Status: %s<br>
Type: %s
"""

location_coordinates = [39,-98] # Default Map Load Location: USA


# Function to choose a color based on Elevation of a volcano as given in 
#       Volcanoes.txt file
# To be used by FeatureGroup fg1
def color_fill(el):
    if el < 1000:
        return 'green'
    elif el < 2000:
        return 'yellow'
    elif el < 3000:
        return 'orange'
    else:
        return 'red'
    
# Function to choose a color based on Population of a region as given in 
#       world.json file
# To be used by FeatureGroup fg2
def fill_pop_col(x):
    if x['properties']['POP2005']<100000000:
        return {'fillColor':'green'}
    elif x['properties']['POP2005']<200000000:
        return {'fillColor':'yellow'}
    elif x['properties']['POP2005']<400000000:
        return {'fillColor':'orange'}
    else:
        return {'fillColor':'red'}



map = folium.Map(location = location_coordinates, tiles = 'Mapbox Bright', zoom_start=4.5)

# Creating a feature group to keep track of all features (markers,etc) in one place
fg1 = folium.FeatureGroup(name = "Volcano Locations")

for lt,ln,el,nm,st,tp in zip(lat,lon,elev,name,status,typ):
    iframe = folium.IFrame(html=html%(nm,nm,el,st,tp), width=300, height=150) # Defines the marker popup text properties
    fg1.add_child(folium.Marker(location=[lt,ln], popup = folium.Popup(iframe), icon=folium.Icon(color=color_fill(el)))) # Adding red marker 'Home' to location coordinate
    #fg1.add_child(folium.CircleMarker(location=[lt,ln], radius=10, popup=folium.Popup(iframe), 
    #                                 fill_color=color_fill(el), color='grey', fill_opacity=0.7)) # Adding CircleMarker instead of normal Marker

map.add_child(fg1) # Adding the whole feature group fg1 to the map



fg2 = folium.FeatureGroup(name = "World Population")

fg2.add_child(folium.GeoJson(data =open('world.json','r',encoding='utf-8-sig').read(),
                            style_function=fill_pop_col)) # Adding the world population layer using GeoJson

map.add_child(fg2) # Adding the whole feature group fg2 to the map

map.add_child(folium.LayerControl()) # Adding a layer control option to toggle the 2 feature groups

map.save('Map1.html')
