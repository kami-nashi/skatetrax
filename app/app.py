from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Response
from flask import request

import json
import pymysql

import lib.logic_json as lj
import lib.logic_main as lm

app = Flask(__name__)

@app.route("/")
def index():

    costs = lm.addCostsTotal()
    hours = lm.addHoursTotal()
    maint = lm.maintenance()
    sessions = lm.sessionsBrief()

    return render_template('etemp_dashboard.html', costs=costs, hours=hours, maint=maint, chart_body=sessions, thour=hours[0])

@app.route('/api/json/sessionsFull', methods=['GET'])
def sessionsFull():
    session = json.loads(lj.sessionsFull())
    jsession = json.dumps(session, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/sessionsBrief', methods=['GET'])
def sessionsBrief():
    session = json.loads(lj.sessionsBrief())
    jsession = json.dumps(session, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, use_reloader=True, debug=True)
