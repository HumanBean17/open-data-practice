import folium

import sys, os

class Map:
    MapDelim = 'file://'
    MapName = os.path.abspath('PollutionMap.html')

    def __init__(self):
        pass

    def CreateMap(self):
        self.Map = folium.Map(location=[37.296933,-121.9574983], zoom_start = 8)
        self.Map.save(self.MapName)

    def GetMapUrl(self):
        return self.MapDelim + self.MapName
    