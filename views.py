from core import app, open_ssh_tunnel, mysql_connect, run_query, mysql_disconnect, close_ssh_tunnel
from flask import jsonify
import groups.assessment as assess
import groups.overall_progress as overall_prog
import groups.planning as plan

@app.route('/')
def index():
    return 'Hello world'

@app.route('/api/assessment')
def assessment():
    open_ssh_tunnel()
    mysql_connect()
    df = run_query(assess.assessment())
    print(df.head())
    dfList = df.values.tolist() 
    mysql_disconnect()
    close_ssh_tunnel()
    return jsonify(dfList)

@app.route('/api/overall_progress')
def overall_progress():
    open_ssh_tunnel()
    mysql_connect()
    df = run_query(overall_prog.overall_progress())
    print(df.head())
    dfList = df.values.tolist() 
    mysql_disconnect()
    close_ssh_tunnel()
    return jsonify(dfList)

@app.route('/api/planning')
def planning():
    open_ssh_tunnel()
    mysql_connect()
    df = run_query(plan.planning())
    print(df.head())
    dfList = df.values.tolist()
    mysql_disconnect()
    close_ssh_tunnel()
    return jsonify(dfList)