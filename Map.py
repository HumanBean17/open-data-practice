import folium
from folium.plugins import MarkerCluster
import branca

import sys, os, json, time

class Map:
    MapDelim = 'file://'
    MapName = os.path.abspath('PollutionMap.html')
    Factor = 100000000

    def __init__(self, data_co, data_so, cities):
        self.Data_CO = data_co
        self.Data_SO = data_so
        self.Cities = cities

        self.Pollution_CO = []
        self.Pollution_SO = []

        self.Colored = {}

        self.CreateMap()

        self.SetClustersCO()
        self.SetClustersSO()

        self.AddGeoJson()
        self.Map.save(self.MapName)

    def StyleFunction(self, feature):
        region = feature['name'].split()[0]
        if region == 'Республика': region = feature['name'].split()[1]
        clr = 'green'
        val = -1
        for r in self.Data_CO:
            if region == r['Регион']:
                for city in self.Pollution_CO:
                    if r['Город'] in city:
                        pollution = city[r['Город']]
                        if pollution > val:
                            val = pollution
        val, clr = self.CalculateColor(val, self.PolDistr_CO)
        self.Colored[region] = clr
        return {
            'fillOpacity': 0.5,
            'weight': 0,
            'fillColor': clr
        }

    def CreateMap(self):
        self.PollutionCalculateCO()
        self.PollutionCalculateSO()
        
        self.Map = folium.Map(location=[55.7522200, 37.6155600], zoom_start = 1)
        colormap = branca.colormap.linear.YlOrRd_09.scale(self.PolDistr_CO[0], self.PolDistr_CO[3])
        colormap = colormap.to_step(index=[self.PolDistr_CO[0], self.PolDistr_CO[1], self.PolDistr_CO[2], self.PolDistr_CO[3]])
        colormap.caption = 'Pollution index'
        colormap.add_to(self.Map)

    def AddGeoJson(self):
        country_path = open('admin_level_2.geojson', encoding='utf-8-sig')
        country_geojson = json.load(country_path)
        
        folium.GeoJson(country_geojson,
            name='geojson',
            style_function=self.StyleFunction).add_to(self.Map)
        folium.LayerControl().add_to(self.Map)


    def GetMapUrl(self):
        return self.MapDelim + self.MapName
    
    def CalculateColor(self, val, data):
        if val > data[2] and val <= data[3]:
            return (val, 'red')
        elif val > data[1] and val <= data[2]:
            return (val, 'orange')
        else:
            return (val, 'green')

    def GetPollutionColorCO(self, city):
        for i in self.Pollution_CO:
            if city['Город'] in i:
                val = i[city['Город']]
        return self.CalculateColor(val, self.PolDistr_CO)

    def GetPollutionColorSO(self, city):
        for i in self.Pollution_SO:
            if city['Город'] in i:
                val = i[city['Город']]
        return self.CalculateColor(val, self.PolDistr_SO)

    def PollutionCalculateCO(self):
        bMax = -1
        bMin = 100000
        for city in self.Data_CO:
            data = city['Загрязнение']['data']
            m = -1
            for d in data:
                if float(d['value'] > m):
                    m = float(d['value'])
            m *= self.Factor
            if m > bMax: bMax = m
            if m < bMin: bMin = m
            self.Pollution_CO.append({city['Город']: int(m)})
        midQuart = int(bMax - bMin) / 4

        self.PolDistr_CO = []
        self.PolDistr_CO.append(midQuart)
        self.PolDistr_CO.append(midQuart*2)
        self.PolDistr_CO.append(midQuart*3)
        self.PolDistr_CO.append(midQuart*4)

    def PollutionCalculateSO(self):
        bMax = -1
        bMin = 10000000
        for city in self.Data_SO:
            data = city['Загрязнение']['data']
            m = -1
            for d in data:
                if float(d['value'] > m):
                    m = float(d['value'])
            m *= self.Factor
            if m > bMax: bMax = m
            if m < bMin: bMin = m
            self.Pollution_SO.append({city['Город']: int(m)})
        midQuart = int(bMax - bMin) / 4

        self.PolDistr_SO = []
        self.PolDistr_SO.append(midQuart)
        self.PolDistr_SO.append(midQuart*2)
        self.PolDistr_SO.append(midQuart*3)
        self.PolDistr_SO.append(midQuart*4)

    def SetClustersCO(self):
        marker_cluster = MarkerCluster(name="CO2").add_to(self.Map)
        for city in self.Data_CO:
            pollution, clr = self.GetPollutionColorCO(city)
            folium.Marker(location=[float(city['Широта']), float(city['Долгота'])]
                        ,radius=9
                        ,popup = str(pollution)
                        ,icon=folium.Icon(color=clr)
                        ,fill_color=clr, fill_opacity=0.9).add_to(marker_cluster)

    def SetClustersSO(self):
        marker_cluster = MarkerCluster(name="SO2").add_to(self.Map)
        for city in self.Data_SO:
            pollution, clr = self.GetPollutionColorSO(city)
            folium.Marker(location=[float(city['Широта']), float(city['Долгота'])]
                        ,radius=9
                        ,popup = str(pollution)
                        ,icon=folium.Icon(color=clr)
                        ,fill_color=clr, fill_opacity=0.9).add_to(marker_cluster)
