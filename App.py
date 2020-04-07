from DataCollector import DataCollector
from GUI import *
from Map import Map

if __name__ == '__main__':
    dataCollector = DataCollector()

    m = Map(dataCollector.GetPollutionDataCO()
        ,dataCollector.GetPollutionDataSO()
        ,dataCollector.GetCities())

    app = QApplication(sys.argv)
    app.setApplicationName("Pollution Map")

    window = MainWindow(m.GetMapUrl())
    app.exec_()

    