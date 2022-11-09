from core import app, open_ssh_tunnel, mysql_connect, run_query, mysql_disconnect, close_ssh_tunnel
from flask import jsonify, Response
import groups.assessment as assess
import groups.overall_progress as overall_prog
import groups.planning as plan

@app.route('/')
def index():
    return 'Hello world'

@app.route('/api')
def api():
    open_ssh_tunnel()
    mysql_connect()
    df = run_query("SELECT * FROM mdl_quiz_grades")
    print(df.head())
    mysql_disconnect()
    close_ssh_tunnel()
    return Response(df.to_json(orient="records"), mimetype='application/json')

@app.route('/api/assessment')
def assessment():
    open_ssh_tunnel()
    mysql_connect()
    df = run_query(assess.assessment())
    print(df.head())
    mysql_disconnect()
    close_ssh_tunnel()
    return Response(df.to_json(orient="records"), mimetype='application/json')

@app.route('/api/overall_progress')
def overall_progress():
    open_ssh_tunnel()
    mysql_connect()
    df = run_query(overall_prog.overall_progress())
    print(df.head())
    mysql_disconnect()
    close_ssh_tunnel()
    return Response(df.to_json(orient="records"), mimetype='application/json')

@app.route('/api/planning')
def planning():
    open_ssh_tunnel()
    mysql_connect()
    df = run_query(plan.planning())
    print(df.head())
    mysql_disconnect()
    close_ssh_tunnel()
    return Response(df.to_json(orient="records"), mimetype='application/json')