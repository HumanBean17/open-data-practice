import folium
#import pandas as pd

import sys, os

class Map:
    MapDelim = 'file://'
    MapName = os.path.abspath('PollutionMap.html')
    Factor = 100000000

    def __init__(self, data, cities):
        self.Data = data
        self.Cities = cities

        self.Pollution = []

        self.CreateMap()
        self.SetMarkers()

        self.Map.save(self.MapName)

    def CreateMap(self):
        self.Map = folium.Map(location=[55.7522200, 37.6155600], zoom_start = 4)

    def GetMapUrl(self):
        return self.MapDelim + self.MapName
    
    def GetPollutionColor(self, city):
        for i in self.Pollution:
            if city['Город'] in i:
                val = i[city['Город']]
        if val > self.PolDistr[3] and val <= self.PolDistr[4]:
            return (val, 'red')
        elif val > self.PolDistr[2] and val <= self.PolDistr[3]:
            return (val, 'lightred')
        elif val > self.PolDistr[1] and val <= self.PolDistr[2]:
            return (val, 'orange')
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



    def SetMarkers(self):
        self.PollutionCalculate()
        for city in self.Data:
            pollution, clr = self.GetPollutionColor(city)
            folium.Marker(location=[float(city['Широта']), float(city['Долгота'])]
                        ,popup = str(pollution)
                        ,icon=folium.Icon(color=clr)).add_to(self.Map)
