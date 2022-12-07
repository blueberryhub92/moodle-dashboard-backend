from do_not_modify.sql_handler import SQLHandlerFacade
import matplotlib.pyplot as plt
import seaborn as sns

class GroupAssessment:
    def __init__(self, app):
        self.app = app
        print("push commit")

    def operation(self) -> dict:
        handler = SQLHandlerFacade(app=self.app, query="SELECT * FROM mdl_quiz_grades")
        handler2 = SQLHandlerFacade(app= self.app, query="SELECT * FROM mdl_assign_grades")
        quiz_grades, pd_dataframe = handler.operation()
        assign_grades, pd_dataframe2 = handler2.operation()
        # Work with pandas.
        print(pd_dataframe.head())
        print(pd_dataframe2.head())
        #id_grades=pd_dataframe["id"]
        #print(id_grades)
        print(pd_dataframe)
        #print(pd_dataframe.loc[:5, ["id", "grade"]])
        #print(pd_dataframe.iloc[0])
        #print(pd_dataframe[pd_dataframe["grade"] == '8.50000'])
        #print(pd_dataframe[pd_dataframe["timemodified"].isin([1577442881, 1577442882])])

        # Work with json data.
        data = quiz_grades.get("result")
        data2 = assign_grades.get("result")
        return quiz_grades, assign_grades
