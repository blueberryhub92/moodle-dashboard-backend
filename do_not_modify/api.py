from flask import Flask, render_template
from flask_cors import CORS

from group_assessment.assessment import GroupAssessment
from group_overall_progress.overall_progress import GroupOverallProgress
from group_planning.planning import GroupPlanning

app = Flask(__name__)
CORS(app)


@app.route('/')
def api_init():
    return render_template('home.html')


@app.route('/group/assessment')
def get_assessment_view():
    return render_template('assessment.html')


@app.route('/api/group/assessment')
def get_assessment_api():
    instance_of_assessment = GroupAssessment(app=app)
    return instance_of_assessment.operation()


@app.route('/api/group/overall_progress')
def get_overall_progress():
    instance_of_overall_progress = GroupOverallProgress(app=app)
    return instance_of_overall_progress.operation()


@app.route('/api/group/planning')
def get_planning():
    instance_of_overall_progress = GroupPlanning(app=app)
    return instance_of_overall_progress.operation()


app.run(host='localhost', port=5000)
