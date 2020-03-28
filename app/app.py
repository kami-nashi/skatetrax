from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Response
from flask import request
from flask import redirect

import json
import pymysql
import datetime

import lib.logic_json as lj
import lib.logic_main as lm

app = Flask(__name__)

# Global Stuff
now = datetime.date.today()

@app.route("/")
def index():
    costs = lm.addCostsTotal()
    hours = lm.addHoursTotal()
    maint = lm.maintenance()
    sessions = lm.sessionsBrief()
    modalSessions = lj.sessionModal()
    return render_template('etemp_dashboard.html', costs=costs, hours=hours, maint=maint, chart_body=sessions, thour=hours[0], modal1=modalSessions, calDate=now)

@app.route("/ice_time")
def iceTime():
    costs = lm.addCostsTotal()
    hours = lm.addHoursTotal()
    maint = lm.maintenance()
    sessions = lm.sessionsFull()
    hLast = float(lm.icetimeLast())
    hCurrent = float(lm.icetimeCurrent())
    hStatus = "normal"
    if hCurrent >= hLast:
        hStatus = "text-success"
    elif hCurrent < hLast:
        hStatus = "text-danger"
    else:
        hStatus = "normal"
    hResults = [hLast,hCurrent,hStatus]
    modalSessions = lj.sessionModal()

    return render_template('etemp_icetime.html', costs=costs, hours=hours, maint=maint, chart_body=sessions, thour=hours[0], hStatus=hResults, modal1=modalSessions, calDate=now)

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


@app.route('/submit_modalSession', methods=['POST'])
def submit_modalSession():
    if request.method == 'POST':
        iceDate = request.form['date']
        iceTime = request.form['ice_time']
        iceCost = request.form['ice_cost']
        iceType = request.form['skate_type']
        iceLoc = request.form['location']
        iceCoach = request.form['coach']
        coachTime = request.form['coach_time']

        sql = """insert into ice_time(date,ice_time,ice_cost,skate_type,coach_time,coach_id,rink_id)values(%s, %s, %s, %s, %s, %s, %s) """
        recordTuple = (iceDate,iceTime,iceCost,iceType,iceLoc,iceCoach,coachTime)
        lm.dbinsert(sql, recordTuple)
        return redirect(request.referrer)
    else:
        return redirect(request.referrer)

@app.route('/submit_modalMaintenance', methods=['POST'])
def submit_modalMaintenance():
    if request.method == 'POST':
        mDate = request.form['m_date']
        mOn = request.form['m_hours_on']
        mCost = request.form['m_cost']
        mLocation = request.form['locationID']

        sql = """insert into maintenance(m_date,m_hours_on,m_cost,m_location)values(%s, %s, %s, %s) """
        recordTuple = (mDate,mOn,mCost,mLocation)
        lm.dbinsert(sql, recordTuple)
        return redirect(request.referrer)
    else:
        return redirect(request.referrer)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, use_reloader=True, debug=True)
