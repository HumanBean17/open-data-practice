import requests, json, sys, os, time

class DataCollector:
    CitiesFname = 'cities.json'
    DataFname = 'pollution_data.json'
    ApiKey = '798b18e906e2847ea3756686a1f48263'
    Datetime = 'current'

    def __init__(self):
        self.Regions = {}
        self.Data = []
        
        #self.UpdateData()

    def GetCities(self):
        with open(self.CitiesFname, 'r', encoding='utf-8-sig') as f:
            cities = json.load(f)
        f.close()
        return cities

    def GetPollutionData(self):
        with open(self.DataFname, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        f.close()
        return data

    def UpdateData(self):
        cities = self.GetCities()
        while True:
            ans = input('All data about pollution will be updated, continue? [y/n] ')
            if ans == 'n': return
            elif ans == 'y': break
        for city in cities:
            self.GetData(city)
        
        self.FData = open(self.DataFname, 'w', encoding='utf-8-sig')
        json.dump(self.Data, self.FData, ensure_ascii=False)
        self.FData.close()

    def GetData(self, cityInfo):
        try:
            if int(cityInfo['Население']) < 100000: 
                pass
            reqStr = self.GetReqStr(cityInfo)
            res = requests.get(reqStr)
            data = self.FillData(cityInfo, res)
            if 'message' in data['Загрязнение']:
                pass
            else:
                print('Got info about ' + data['Город'])
            self.Data.append(data)
        except Exception as e:
            print("Exception (weather):", e)
            pass

    @classmethod
    def FillData(self, cityInfo, res):
        data = {'Город': None, 'Регион': None, 'Население': None, 'Загрязнение': None}
        data['Город'] = cityInfo['Город']
        data['Регион'] = cityInfo['Регион']
        data['Население'] = cityInfo['Население']
        data['Широта'] = cityInfo['Широта']
        data['Долгота'] = cityInfo['Долгота']
        data['Загрязнение'] = res.json()
        return data

    @classmethod
    def GetReqStr(self, cityInfo):
        location = str(cityInfo['Широта'].split('.')[0]) + ',' + str(cityInfo['Долгота'].split('.')[0])
        #http://api.openweathermap.org/pollution/v1/co/{location}/{datetime}.json?appid={api_key}
        return 'http://api.openweathermap.org/pollution/v1/co/' + location + '/' + self.Datetime + '.json?appid=' + self.ApiKey