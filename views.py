from core import app
from models import db, quiz_grade_schemas, QuizGradesModel
from flask import jsonify, render_template
import groups.assessment as assess
import groups.overall_progress as overall_prog
import groups.planning as plan


@app.route('/')
def fetch_acceleration_data():
    return 'Hello world'
    # grades = QuizGradesModel.query.all()
    # return render_template('index.html', grades=grades)

@app.route('/api')
def api():
    grades = QuizGradesModel.query.all()
    result = quiz_grade_schemas.dump(grades)
    return jsonify(result)

@app.route('/api/assessment')
def assessment():
    return assess.assessment()

@app.route('/api/overall_progress')
def overall_progress():
    return overall_prog.overall_progress()

@app.route('/api/planning')
def planning():
    return plan.planning()