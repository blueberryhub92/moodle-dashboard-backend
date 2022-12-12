from do_not_modify.sql_handler import SQLHandlerFacade
import time
import pandas as pd
import os


class GroupOverallProgress:
    def __init__(self, app):
        self.app = app

    moduleData = []
    logData = []
    moodleURL = 'http://83.212.126.199/moodle/mod/'

    def operation(self) -> dict:
        handler = SQLHandlerFacade(app=self.app, query="SELECT * FROM mdl_course_modules WHERE visible=1 ORDER BY added ASC")
        operation_result, pd_dataframe = handler.operation()

        data = operation_result.get("result")
        self.moduleData = data
        print(time.mktime(time.strptime('20/10/2020', "%d/%m/%Y")))
        self.filterTime(1450847576, 1578329680)
        # self.printModules()
        self.operation2()
        return operation_result

    def operation2(self) -> dict:
        #path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', './logs_LA_20__21_20221202-1706.csv'))
        #df = pd.read_csv(path)
        #print(df)

        self.redirect('URL', '4')
        self.redirect('File', '6')

        #return df

    def redirect(self, component, id):
        if component == 'URL':
            link = self.moodleURL+'url/view.php?id='+id
        elif component == 'File':
            link = self.moodleURL + 'resource/view.php?id=' + id
        print(link)
    def filterTime(self, start, stop):
        filteredData = []
        for module in self.moduleData:
            if (module['added'] >= start) and (module['added'] <= stop):
                filteredData.append(module)
        self.moduleData = filteredData
        return filteredData

    # http://83.212.126.199/moodle/mod/resource/view.php?id=6
    # http://83.212.126.199/moodle/mod/url/view.php?id=4
    def printModules(self):
        for module in self.moduleData:
            print('id: ', module['id'])
            # print('timestamp: ', module['added'])