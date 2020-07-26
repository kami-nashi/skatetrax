from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Response
from flask import request
from flask import redirect
from flask import session
from flask import flash
from flask import url_for
from flask import g

from functools import wraps

import json
import pymysql
import datetime
import math

import lib.logic_json as lj
import lib.logic_main as lm

app = Flask(__name__)
app.secret_key = 'password1'

# Make Shift/Pretend logged in user
AuthSkaterUUID = 1

@app.before_request
def globalStuff():
    # Global Stuff
    g.now = datetime.date.today()
    g.modalSessions = lj.sessionModal()
    g.costs = lm.addCostsTotal(AuthSkaterUUID)
    g.hours = lm.addHoursTotal(AuthSkaterUUID)
    g.cHours = lm.monthlyCoachTime(AuthSkaterUUID)
    g.sHours = lm.monthlyIceTime(AuthSkaterUUID)
    g.uHours = math.ceil(g.sHours[0]['monthly_ice']*4)/4-math.ceil(g.cHours[0]['monthly_coach']*4)/4
    g.mHours = [g.uHours, math.ceil(g.cHours[0]['monthly_coach']*4)/4]

# Login Decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    aUser = None
    sql = None
    if request.method == 'POST':
        vTUP = request.form['username']
        sql = "select * from aUserTable where uLoginID = %s"
        aUser = lm.dbconnect(sql, vTUP)
    if request.method == 'POST':
        if (request.form['username'] != aUser[0]['uLoginID']) \
                or request.form['password'] != aUser[0]['uHash']:
            error = 'Invalid Credentials. Please try again.'

        else:
            session['logged_in'] = True
            if session['logged_in'] == True:
                session['username'] = aUser[0]['uLoginID']
                session['sUUID'] = aUser[0]['uSkaterUUID']
                authSkaterUUID = aUser
                asUUID = (authSkaterUUID[0]['uSkaterUUID'])
                aSkater = 'select * from uSkaterConfig where uSkaterUUID = %s'
                aUserInfo = lm.dbconnect(aSkater,asUUID)
                session['fName'] = aUserInfo[0]['uSkaterFname']
                session['lName'] = aUserInfo[0]['uSkaterLname']
            else:
                pass
            flash('You were logged in.')
            return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route("/")
def index():
    maint = lm.uMantenanceV2(AuthSkaterUUID)
    sessions = lm.sessionsBrief(AuthSkaterUUID)
    return render_template('etemp_dashboard.html', ses=session, costs=g.costs, hours=g.mHours, maint=maint, chart_body=sessions, thour=g.hours[2], modal1=g.modalSessions, calDate=g.now)

@app.route("/journal")
def journal():
    jDate = request.args.get('date', default = '', type = str)
    if jDate == '':
        jTable = lm.jVideos(AuthSkaterUUID,jv=0)
    else:
        print(jDate, 'its not empty')
        jTable = lm.jVideos(AuthSkaterUUID,jDate)
    return render_template('etemp_journals.html', thour=g.hours[2], modal1=g.modalSessions, calDate=g.now, journalTable=jTable)

@app.route("/skater_overview")
@login_required
def skater_overview():
    sOff = lm.skaterOffBlades(AuthSkaterUUID)
    sIce = lm.skaterIceBlades(AuthSkaterUUID)
    return render_template('etemp_skater_overview.html',ses=session, thour=g.hours[2], modal1=g.modalSessions, skateOff=sOff, skateIce=sIce)

@app.route("/maintenance")
def maintenance():
    maint = lm.uMantenanceV2(AuthSkaterUUID)
    sessions = lm.sessionsBrief(AuthSkaterUUID)
    maintTable = lm.maintTable(AuthSkaterUUID)
    return render_template('etemp_maintenance.html', costs=g.costs, hours=g.hours, maint=maint, chart_body=sessions, thour=g.hours[2], modal1=g.modalSessions, calDate=g.now,maintTable=maintTable)

@app.route("/ice_time")
def iceTime():
    maint = lm.uMantenanceV2(AuthSkaterUUID)
    sessions = lm.sessionsFull(AuthSkaterUUID)
    hLast = float(lm.icetimeLast(AuthSkaterUUID))
    hCurrent = float(lm.icetimeCurrent(AuthSkaterUUID))
    hStatus = "normal"
    if hCurrent > hLast:
        hStatus = "text-success"
    elif hCurrent < hLast:
        hStatus = "text-danger"
    elif hCurrent == 0:
        hStatus = "text-danger"
    else:
        hStatus = "normal"
    hResults = [hLast,hCurrent,hStatus]

    inlineLast = float(lm.inlinetimeLast(AuthSkaterUUID))
    inlineCurrent = float(lm.inlinetimeCurrent(AuthSkaterUUID))
    inlineStatus = "normal"
    if inlineCurrent > inlineLast:
        inlineStatus = "text-success"
    elif inlineCurrent < inlineLast:
        inlineStatus = "text-danger"
    elif inlineCurrent == 0:
        inlineStatus = "text-danger"
    else:
        inlineStatus = "normal"
    inlineResults = [inlineLast,inlineCurrent,inlineStatus]

    pData = lm.punchCard(AuthSkaterUUID)
    return render_template('etemp_icetime.html', ses=session, costs=g.costs, hours=g.hours, maint=maint, chart_body=sessions, thour=g.hours[2], hStatus=hResults, inlineStatus=inlineResults, modal1=g.modalSessions, calDate=g.now, pData=pData)

@app.route('/api/json/areaTest', methods=['GET'])
def areaTest():
    session = json.loads(lj.areaTest(AuthSkaterUUID))
    jsession = json.dumps(session, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/sessionsArea', methods=['GET'])
def sessionsArea():
    session = json.loads(lj.sessionsArea(AuthSkaterUUID))
    jsession = json.dumps(session, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

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
        iceLoc = request.form['rLocation']
        iceCoach = request.form['coach']
        coachTime = request.form['coach_time']

        sql = """insert into ice_time(date,ice_time,ice_cost,skate_type,coach_time,coach_id,rink_id,uSkaterUUID)values(%s, %s, %s, %s, %s, %s, %s, %s) """
        recordTuple = (iceDate,iceTime,iceCost,iceType,coachTime,iceCoach,iceLoc,AuthSkaterUUID)
        lm.dbinsert(sql, recordTuple)
        return redirect(url_for('index'))
        #return redirect(request.referrer)
    else:
        return redirect(request.referrer)

@app.route('/submit_modalMaintenance', methods=['POST'])
def submit_modalMaintenance():
    if request.method == 'POST':
        mDate = request.form['m_date']
        mOn = request.form['m_hours_on']
        mCost = request.form['m_cost']
        mLocation = request.form['locationID']

        sql = """insert into maintenance(m_date,m_hours_on,m_cost,m_location,uSkaterUUID)values(%s, %s, %s, %s,%s) """
        recordTuple = (mDate,mOn,mCost,mLocation,AuthSkaterUUID)
        lm.dbinsert(sql, recordTuple)
        return redirect(request.referrer)
    else:
        return redirect(request.referrer)

@app.route('/logout')
@login_required
def logout():
        session.pop('logged_in', None)
        flash('You were logged out.')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, use_reloader=True, debug=True)
