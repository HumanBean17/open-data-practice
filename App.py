from DataCollector import DataCollector
from GUI import *
from Map import Map

if __name__ == '__main__':
    #dataCollector = DataCollector()
    #dataCollector.UpdateData()
    
    m = Map()
    #m.CreateMap()

    app = QApplication(sys.argv)
    app.setApplicationName("Pollution Map")

    print(m.GetMapUrl())
    window = MainWindow(m.GetMapUrl())
    app.exec_()

    