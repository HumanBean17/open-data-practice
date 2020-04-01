import folium
#import pandas as pd

import sys, os

class Map:
    MapDelim = 'file://'
    MapName = os.path.abspath('PollutionMap.html')

    def __init__(self, data, cities):
        self.Data = data
        self.Cities = cities

        self.CreateMap()
        self.SetMarkers()

        self.Map.save(self.MapName)

    def CreateMap(self):
        self.Map = folium.Map(location=[55.7522200, 37.6155600], zoom_start = 4)

    def GetMapUrl(self):
        return self.MapDelim + self.MapName
    
    def SetMarkers(self):
        for city in self.Data:
            folium.Marker(location=[float(city['Широта']),float(city['Долгота'])], popup = city['Город'], icon=folium.Icon(color = 'gray')).add_to(self.Map)