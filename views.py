from core import app, open_ssh_tunnel, mysql_connect, run_query, mysql_disconnect, close_ssh_tunnel
from flask import jsonify, Response, render_template
import groups.assessment as assess
import groups.overall_progress as overall_prog
import groups.planning as plan

import json
import pandas as pd
import plotly
import plotly.express as px

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart1')
def chart1():
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Fruit in North America"
    description = """
    A academic study of the number of apples, oranges and bananas in the cities of
    San Francisco and Montreal would probably not come up with this chart.
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/chart2')
def chart2():
    df = pd.DataFrame({
        "Vegetables": ["Lettuce", "Cauliflower", "Carrots", "Lettuce", "Cauliflower", "Carrots"],
        "Amount": [10, 15, 8, 5, 14, 25],
        "City": ["London", "London", "London", "Madrid", "Madrid", "Madrid"]
    })

    fig = px.bar(df, x="Vegetables", y="Amount", color="City", barmode="stack")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Vegetables in Europe"
    description = """
    The rumor that vegetarians are having a hard time in London and Madrid can probably not be
    explained by this chart.
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)


@app.route('/chart3')
def chart3():
    open_ssh_tunnel()
    mysql_connect()
    df = run_query("SELECT * FROM mdl_quiz_grades")

    fig = px.bar(df, x="userid", y="grade", barmode="stack")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="mdl_quiz_grades"
    description = """
    Grades by User ID
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)

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