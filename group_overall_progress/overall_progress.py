

from do_not_modify.sql_handler import SQLHandlerFacade
import json
import pandas as pd
import math

# enrolled users(localy)
# df_users = pd.read_excel(io=r"C:\Users\admin\Downloads\Py_DS_ML_Bootcamp-master\enrolledusers.xlsx")
# enrolled_users = list(df_users['User full name'].unique())
# enrolled_users.remove('anonfirstname12 anonlastname12')"""
class GroupOverallProgress:
    def __init__(self, app):
        self.app = app


    def operation(self):

        # reading the file localy
        # df = pd.read_csv(r'C:\Users\admin\moodle-dashboard-backend\logs_LA_20__21_20221202-1706.csv')

        # reading the file from the repository
        url = 'https://raw.githubusercontent.com/blueberryhub92/moodle-dashboard-backend/main/logs_LA_20__21_20221202-1706.csv'
        df = pd.read_csv(url)

        #  the list of all the enrolled users
        eu = ['anonfirstname31 anonlastname31', 'anonfirstname62 anonlastname62', 'anonfirstname65 anonlastname65',
         'anonfirstname51 anonlastname51', 'anonfirstname66 anonlastname66', 'anonfirstname47 anonlastname47',
         'anonfirstname48 anonlastname48', 'anonfirstname68 anonlastname68', 'anonfirstname59 anonlastname59',
         'anonfirstname64 anonlastname64', 'anonfirstname67 anonlastname67', 'anonfirstname53 anonlastname53',
         'anonfirstname49 anonlastname49', 'anonfirstname55 anonlastname55', 'anonfirstname73 anonlastname73',
         'anonfirstname60 anonlastname60', 'anonfirstname57 anonlastname57', 'anonfirstname70 anonlastname70',
         'anonfirstname63 anonlastname63', 'anonfirstname54 anonlastname54', 'anonfirstname56 anonlastname56',
         'anonfirstname61 anonlastname61', 'anonfirstname69 anonlastname69', 'anonfirstname58 anonlastname58',
         'anonfirstname52 anonlastname52', 'anonfirstname71 anonlastname71', 'anonfirstname72 anonlastname72',
         'anonfirstname21 anonlastname21']



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

        # concatenating all the user activities in one dataframe
        user_all_activities = pd.concat([df_user_quiz, df_user_assignment, df_user_url, df_user_file],
                                        ignore_index=True)

        # all quizes
        df_quizes = df[(df['Component'] == "Quiz") & (df['User full name'].isin(eu)) &
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
        df_url = df[(df['Component'] == "URL") & (df['User full name'].isin(eu)) &
                    (df["Event name"] == "Course module viewed")]

        du = df_url.drop_duplicates(subset='Event context', keep='first')
        print(du)
        Url_amount = du["Component"].count()

        # all files
        df_file = df[(df["Component"] == "File") & df['User full name'].isin(eu)]
        dff = df_file.drop_duplicates(subset=['Event context'], keep='first')
        print(dff)
        File_amount = dff["Component"].count()

        # dataframe of all the activities that exist in the course
        all_activities = pd.concat([dq, da, du, dff], ignore_index=True)

        print(all_activities)


        seen_activities = list(user_all_activities['Event context'])
        unseen = all_activities[~all_activities["Event context"].isin(seen_activities)]

        # percentage of each learning material
        quiz_perc = math.ceil(df_user_quiz["Component"].count() * 100 / Quiz_amount)
        assignment_perc = math.ceil(df_user_assignment["Component"].count() * 100 / Assignment_amount)
        url_perc = math.ceil(df_user_url["Component"].count() * 100 / Url_amount)
        file_perc = math.ceil(df_user_file["Component"].count() * 100 / File_amount)


        # converting the dataframes to json


        data_user = user_all_activities.to_json(orient="columns")
        data_unseen = unseen.to_json(orient="columns")
        perc = json.dumps([quiz_perc, assignment_perc, url_perc, file_perc])
        list_df=[data_user,data_unseen,perc]
        json_data=json.dumps(list_df)

        return list_df


