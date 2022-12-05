from do_not_modify.sql_handler import SQLHandlerFacade

import pandas as pd
import openpyxl
import plotly.express as px

class GroupOverallProgress:
    def __init__(self, app):
        self.app = app


    def operation(self) -> dict:
        '''handler = SQLHandlerFacade(app=self.app, query="SELECT * logs_LA_20__21_20221202-1706")
        operation_result, pd_dataframe = handler.operation()
        # Work with pandas.
        print(pd_dataframe.head())
        print(pd_dataframe["id"])
        print(pd_dataframe.loc[:5, ["id", "grade"]])
        print(pd_dataframe.iloc[0])
        print(pd_dataframe[pd_dataframe["grade"] == '8.50000'])
        print(pd_dataframe[pd_dataframe["timemodified"].isin([1577442881, 1577442882])])
        # Work with json data.
        data = operation_result.get("result")
        return operation_result'''



        # reading the data frame

        df = pd.read_csv(r'C:\Users\admin\Downloads\Py_DS_ML_Bootcamp-master\logs_LA_20__21_20221202-1706.csv')
        print(df.head())
        # enrolled users
        df_users = pd.read_excel(io=r"C:\Users\admin\Downloads\Py_DS_ML_Bootcamp-master\enrolledusers.xlsx")
        enrolled_users = list(df_users['User full name'].unique())
        enrolled_users.remove('anonfirstname12 anonlastname12')

        print(enrolled_users)

        default_user = str(63)

        # user quisez
        Quiz_module_id = ['610', '616', '664', '669', '679', '697']

        df_user_quiz = df[(df['UserID'] == default_user)
                          & (df["Event context"] != "Quiz: E-exam") &
                          (df['Event name'] == 'Quiz attempt submitted')]
        print(df_user_quiz)

        # user assignments
        Asg_module_id = ['623', '640', '698', '708']
        df_user_assignment = df[(df['UserID'] == default_user) & (df["Component"] == "Assignment") &
                                (df['Event name'] == "A submission has been submitted.")]
        print(df_user_assignment)
        # user url
        df_user_url = df[(df["Component"] == "URL") & (df["Event name"] == "Course module viewed") &
                         (df['UserID'] == default_user)]
        df_user_url = df_user_url.drop_duplicates(subset='Event context', keep='first')
        print(df_user_url)
        
        # user files
        df_user_file = df[(df["Component"] == "File") & (df["Event name"] == "Course module viewed") &
                          (df['UserID'] == default_user)]
        df_user_file = df_user_file.drop_duplicates(subset=["Event context"], keep='first')
        print(df_user_file)

        all_activities = pd.concat([df_user_quiz, df_user_assignment, df_user_url, df_user_file], ignore_index=True)

        # all quizes
        df_quizes = df[(df['Component'] == "Quiz") & (df['User full name'].isin(enrolled_users)) &
                       (df['Event context'] != 'Quiz: E-exam')]
        dq = df_quizes.drop_duplicates(subset='Event context', keep='first')
        print(dq)
        Quiz_amount = dq["Component"].count()

        # all assignments
        df_asg = df[(df['Component'] == "Assignment") &
                    (df["Event name"] == 'A submission has been submitted.')]
        print(df_asg)
        da = df_asg.drop_duplicates(subset='Event context', keep='first')
        print(da)
        Assignment_amount = da["Component"].count()

        # all Urls
        df_url = df[(df['Component'] == "URL") & (df['User full name'].isin(enrolled_users)) &
                    (df["Event name"] == "Course module viewed")]

        du = df_url.drop_duplicates(subset='Event context', keep='first')
        print(du)
        Url_amount = du["Component"].count()

        # all files
        df_file = df[(df["Component"] == "File") & df['User full name'].isin(enrolled_users)]
        dff = df_file.drop_duplicates(subset=['Event context'], keep='first')
        print(dff)
        File_amount = dff["Component"].count()

        participation = all_activities.groupby(['Component'])['Component'].count()
        participation.index.rename("Learning Materials", inplace=True)
        print(participation)

        # final data frame
        final_frame = pd.DataFrame(participation, index=["Assignment", "File", "Quiz", "URL"])

        final_frame.insert(1, "Max", [Assignment_amount, File_amount, Quiz_amount, Url_amount], True)
        print(final_frame)

        percentage = final_frame.Component * 100 / final_frame.Max
        fig1 = px.bar(all_activities, x=percentage, y=final_frame.index,
                      title='<b>Overall Progress </b>', orientation='h', color=percentage, range_x=[0, 100]
                      )
        fig1.update_layout(
            yaxis_title="Learning Materials",
            xaxis_title="Your Progress")
        a = all_activities['Event context']

        fig1.show()
