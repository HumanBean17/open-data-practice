import requests, json, sys, os, time

class DataCollector:
    CitiesFname = 'cities.json'
    DataFname_CO = 'pollution_data_CO.json'
    DataFname_SO = 'pollution_data_SO.json'
    ApiKey = '798b18e906e2847ea3756686a1f48263'
    Datetime = 'current'

    def __init__(self):
        self.Regions = {}

        self.Data_CO = []
        self.Data_SO = []
        self.UpdateData()

    def GetCities(self):
        with open(self.CitiesFname, 'r', encoding='utf-8-sig') as f:
            cities = json.load(f)
        f.close()
        return cities

    def GetPollutionDataCO(self):
        with open(self.DataFname_CO, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        f.close()
        return data

    def GetPollutionDataSO(self):
        with open(self.DataFname_SO, 'r', encoding='utf-8-sig') as f:
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
            self.GetData(city, 'co')
            self.GetData(city, 'so')
        
        self.FData_CO = open(self.DataFname_CO, 'w', encoding='utf-8-sig')
        self.FData_SO = open(self.DataFname_SO, 'w', encoding='utf-8-sig')

        json.dump(self.Data_CO, self.FData_CO, ensure_ascii=False)
        json.dump(self.Data_SO, self.FData_SO, ensure_ascii=False)
        self.FData_CO.close()
        self.FData_SO.close()

    def GetData(self, cityInfo, dataType):
        try:
            if int(cityInfo['Население']) < 100000:
                return
            reqStr = self.GetReqStr(cityInfo, dataType)
            res = requests.get(reqStr)
            data = self.FillData(cityInfo, res)
            if 'message' in data['Загрязнение']:
                return
            else:
                print('Got info about ' + data['Город'])
            
            if dataType == 'co': self.Data_CO.append(data)
            elif dataType == 'so': self.Data_SO.append(data)
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
    def GetReqStr(self, cityInfo, dataType):
        location = str(cityInfo['Широта'].split('.')[0]) + ',' + str(cityInfo['Долгота'].split('.')[0])
        if dataType == 'co':    
            req = 'http://api.openweathermap.org/pollution/v1/co/' + location + '/' + self.Datetime + '.json?appid=' + self.ApiKey
        elif dataType == 'so':
            req = 'http://api.openweathermap.org/pollution/v1/so2/' + location + '/' + self.Datetime + '.json?appid=' + self.ApiKey
        return req
