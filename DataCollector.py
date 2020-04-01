import requests, json, sys, os, time

class DataCollector:
    CitiesFname = 'cities.json'
    DataFname = 'pollution_data.json'
    ApiKey = '798b18e906e2847ea3756686a1f48263'
    Datetime = 'current'

    def __init__(self):
        self.Data = []

    def UpdateData(self):
        with open(self.CitiesFname, 'r', encoding='utf-8-sig') as f:
            cities = json.load(f)
        while True:
            ans = input('All data about pollution will be updated, continue? [y/n] ')
            if ans == 'n': return
            elif ans == 'y':
                self.FData = open(self.DataFname, 'w', encoding='utf-8-sig')
                break
        for city in cities:
            self.GetData(city)
        json.dump(self.Data, self.FData, ensure_ascii=False)
        
    def GetData(self, cityInfo):
        try:
            reqStr = self.GetReqStr(cityInfo)
            res = requests.get(reqStr)
            data = {'Город': None, 'Регион': None, 'Население': None, 'Загрязнение': None}
            data['Город'] = cityInfo['Город']
            data['Регион'] = cityInfo['Регион']
            data['Население'] = cityInfo['Население']
            data['Загрязнение'] = res.json()
            print('Got info about ' + data['Город'])
            self.Data.append(data)
        except Exception as e:
            print("Exception (weather):", e)
            pass

    @classmethod
    def GetReqStr(self, cityInfo):
        location = str(cityInfo['Широта'].split('.')[0]) + ',' + str(cityInfo['Долгота'].split('.')[0])
        #http://api.openweathermap.org/pollution/v1/co/{location}/{datetime}.json?appid={api_key}
        return 'http://api.openweathermap.org/pollution/v1/co/' + location + '/' + self.Datetime + '.json?appid=' + self.ApiKey