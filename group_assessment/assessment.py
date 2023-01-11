"""
@Author: RojalM
"""

import json
from do_not_modify.sql_handler import SQLHandlerFacade
import pandas as pd


# #########################################
# Fetching data and pass them to frontend #
# #########################################

class GroupAssessment:
    def __init__(self, app):
        self.app = app

    def operation(self) -> dict:
        """
          Returns a list of quiz and assumption grades and pass them to the frontend.

                  Parameters:
                          ! current_user (int): the logged-in user can be added as a parameter.

                  Returns:
                          list_df (dict): Values of grades as new dictionary
                          initialized from a mapping object's (key, value) pairs.
        """
        # logged in user
        current_user = 185
        # handler = SQLHandlerFacade(app=self.app, query="SELECT * FROM mdl_quiz_grades")
        # operation_result, quiz_grades_df = handler.operation()

        assign_grades_df = pd.read_csv('C:/Users/Rojal/Desktop/dashboard project/mdl_assign_grades.csv',
                                       on_bad_lines='skip', encoding='utf-8')
        quiz_grades_df = pd.read_csv('C:/Users/Rojal/Desktop/Dashboard our job/quizgrades final 0.csv',
                                     on_bad_lines='skip', encoding='utf-8')

        # Work with pandas.

        # convert the grade type to float
        quiz_grades_df.grade = quiz_grades_df.grade.astype(float)
        quiz_grades_df['grade'] = quiz_grades_df['grade'].fillna(.0).astype(float)

        # display the panda file as float .0
        pd.options.display.float_format = '{:,.0f}'.format

        # changing the values of quiz names
        quiz_grades_df['quiz'] = quiz_grades_df['quiz'].replace(
            {37: 'quiz 1', 38: 'quiz 2', 39: 'quiz 3', 40: 'quiz 4', 41: 'quiz 5', 42: 'quiz 6', 43: 'quiz final',
             -1: 0, 'Null': 0})

        # eliminating invalid values
        quiz_grades_df['grade'] = quiz_grades_df['grade'].replace({-1: 0, 'Null': 0})

        # specifying the current user data for grades
        quiz_grades_df_edited = quiz_grades_df.loc[quiz_grades_df['userid'] == current_user]

        # changing the values of assignment
        assign_grades_df['assignment'] = assign_grades_df['assignment'].replace(
            {27: 'AS1 - W3', 28: 'AS2 - W5', 30: 'AS3 - W10', 31: 'AS4 - W11', -1: 0, 'Null': 0})

        assign_grades_df['grade'] = assign_grades_df['grade'].replace({-1: 0, 'Null': 0})

        # specifying current user data for assignment
        assign_edited = assign_grades_df.loc[assign_grades_df['userid'] == 185]

        # Work with json data.
        # converting quiz grades to json data
        user_quiz_grades = quiz_grades_df_edited.to_json(orient="columns")

        # converting assign grades to json data
        user_assign_grades = assign_edited.to_json(orient="columns")

        # combined both data frames in a list
        list_df = [user_quiz_grades, user_assign_grades]

        # convert a subset of Python objects into a json string. (can be used later)
        json_data = json.dumps(list_df)

        return list_df
