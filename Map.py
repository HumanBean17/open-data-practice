import folium
from folium.plugins import MarkerCluster
#import pandas as pd

import sys, os, json, time

class Map:
    MapDelim = 'file://'
    MapName = os.path.abspath('PollutionMap.html')
    Factor = 100000000

    def __init__(self, data, cities):
        self.Data = data
        self.Cities = cities

        self.Colored = {}
        self.Pollution = []

        self.CreateMap()

        self.SetClusters()

        self.AddGeoJson()
        self.Map.save(self.MapName)

    def StyleFunction(self, feature):
        region = feature['name'].split()[0]
        if region == 'Республика': region = feature['name'].split()[1]
        clr = 'green'
        for r in self.Data:
            if region == r['Регион']:
                pollution, clr = self.GetPollutionColor(r)
        return {
            'fillOpacity': 0.5,
            'weight': 0,
            'fillColor': clr
        }

    def CreateMap(self):
        self.PollutionCalculate()
        self.Map = folium.Map(location=[55.7522200, 37.6155600], zoom_start = 1)
        
    def AddGeoJson(self):
        country_path = open('admin_level_2.geojson', encoding='utf-8-sig')
        country_geojson = json.load(country_path)
        
        folium.GeoJson(country_geojson, name='geojson', style_function=self.StyleFunction).add_to(self.Map)
        folium.LayerControl().add_to(self.Map)


    def GetMapUrl(self):
        return self.MapDelim + self.MapName
    
    def GetPollutionColor(self, city):
        for i in self.Pollution:
            if city['Город'] in i:
                val = i[city['Город']]
        if val > self.PolDistr[3] and val <= self.PolDistr[4]:
            return (val, 'red')
        elif val > self.PolDistr[2] and val <= self.PolDistr[3]:
            return (val, 'orange')
        elif val > self.PolDistr[1] and val <= self.PolDistr[2]:
            return (val, 'lightred')
        else:
            return (val, 'green')

    def PollutionCalculate(self):
        bMax = -1
        bMin = 100000
        for city in self.Data:
            data = city['Загрязнение']['data']
            m = -1
            for d in data:
                if float(d['value'] > m):
                    m = float(d['value'])
            m *= self.Factor
            if m > bMax: bMax = m
            if m < bMin: bMin = m
            self.Pollution.append({city['Город']: int(m)})
        midQuart = int(bMax - bMin) / 5

        self.PolDistr = []
        self.PolDistr.append(midQuart)
        self.PolDistr.append(midQuart*2)
        self.PolDistr.append(midQuart*3)
        self.PolDistr.append(midQuart*4)
        self.PolDistr.append(midQuart*5)

    def SetClusters(self):
        marker_cluster = MarkerCluster().add_to(self.Map)
        for city in self.Data:
            pollution, clr = self.GetPollutionColor(city)
            folium.Marker(location=[float(city['Широта']), float(city['Долгота'])]
                        ,radius=9
                        ,popup = str(pollution)
                        ,icon=folium.Icon(color=clr)
                        ,fill_color=clr, fill_opacity=0.9).add_to(marker_cluster)

    """def SetMarkers(self):
        for city in self.Data:
            pollution, clr = self.GetPollutionColor(city)
            folium.Marker(location=[float(city['Широта']), float(city['Долгота'])]
                        ,popup = str(pollution)
                        ,icon=folium.Icon(color=clr)).add_to(self.Map)"""
