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

@app.before_request
def load_session_from_cookie():
    try:
        if session['logged_in'] == True:
            g.sessID = session.get('uSkaterUUID')
            g.now = datetime.date.today()
            g.modalSessions = lj.sessionModal()
            g.costs = lm.addCostsTotal(g.sessID)
            g.hours = lm.addHoursTotal(g.sessID)
            g.cHours = lm.monthlyCoachTime(g.sessID)
            g.sHours = lm.monthlyIceTime(g.sessID)
            g.uHours = math.ceil(g.sHours[0]['monthly_ice']*4)/4-math.ceil(g.cHours[0]['monthly_coach']*4)/4
            g.mHours = [g.uHours, math.ceil(g.cHours[0]['monthly_coach']*4)/4]
            g.maint = lm.uMantenanceV2(g.sessID)
            g.sessions = lm.sessionsBrief(g.sessID)
            g.sessfull = lm.sessionsFull(g.sessID)
            g.mPVC = [g.uHours, math.ceil(g.cHours[0]['monthly_coach']*4)/4, g.sHours[0]['ice_cost']]
            g.ice = g.maint[6]

    except:
        pass

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
# Landing Page
@app.route('/')
def home():
    return render_template('unauth_welcome.html')

# use decorators to link the function to a url
@app.route('/')
@login_required
def index():
    sql = "select * from uSkaterConfig where uSkaterUUID = %s"
    subUserUUID = session['sUUID']
    results = lm.dbconnect(sql,subUserUUID)
    return render_template('etemp_dashboard.html', ses=session, costs=g.costs, hours=g.mHours, maint=g.maint, chart_body=g.sessions, thour=g.hours[2], modal1=g.modalSessions, calDate=g.now)  # render a template

@app.route('/logout')
@login_required
def logout():
        session.pop('logged_in', None)
        flash('You were logged out.')
        return redirect(url_for('index'))

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    aUser = None
    sql = None
    if request.method == 'POST':
        input = str(request.form['username'])
        sql = "select * from aUserTable where uLoginID = %s"
        aUser = lm.dbconnect(sql,input)

    if request.method == 'POST':
        if (request.form['username'] != aUser[0]['uLoginID']) \
                or request.form['password'] != aUser[0]['uHash']:
            error = 'Invalid Credentials. Please try again.'

        else:
            session['logged_in'] = True
            if session['logged_in'] == True:
                authSkaterUUID = aUser
                asUUID = (authSkaterUUID[0]['uSkaterUUID'])
                aSkater = 'select * from uSkaterConfig where uSkaterUUID = %s'
                aUserInfo = lm.dbconnect(aSkater,asUUID)
                session['username'] = aUser[0]['uLoginID']
                session['sUUID'] = aUser[0]['uSkaterUUID']
                session['username'] = aUser[0]['uLoginID']
                session['sUUID'] = aUser[0]['uSkaterUUID']
                session['fName'] = aUserInfo[0]['uSkaterFname']
                session['lName'] = aUserInfo[0]['uSkaterLname']
                session['uSkaterUUID'] = aUserInfo[0]['uSkaterUUID']
                g.sessID = session.get('uSkaterUUID')
            else:
                pass
            flash('You were logged in.')
            return redirect(url_for('dashboard'))
    return render_template('unauth_login.html', error=error)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('etemp_dashboard.html', modal1=g.modalSessions, ses=session, thour=g.hours[2], hours=g.mHours, costs=g.costs, maint=g.maint, chart_body=g.sessions )

@app.route("/journal")
@login_required
def journal():
    jDate = request.args.get('date', default = '', type = str)
    if jDate == '':
        jTable = lm.jVideos(g.sessID,jv=0)
    else:
        print(jDate, 'its not empty')
        jTable = lm.jVideos(g.sessID,jDate)
    return render_template('etemp_journals.html', ses=session, thour=g.hours[2], modal1=g.modalSessions, calDate=g.now, journalTable=jTable)

@app.route("/skater_overview")
@login_required
def skater_overview():
    sOff = lm.skaterOffBlades(g.sessID)
    sIce = lm.skaterIceBlades(g.sessID)
    return render_template('etemp_skater_overview.html',ses=session, thour=g.hours[2], modal1=g.modalSessions, skateOff=sOff, skateIce=sIce)

@app.route("/maintenance")
@login_required
def maintenance():
    maintTable = lm.maintTable(g.sessID)
    return render_template('etemp_maintenance.html', ses=session, costs=g.costs, hours=g.hours, maint=g.maint, chart_body=g.sessions, thour=g.hours[2], modal1=g.modalSessions, calDate=g.now,maintTable=maintTable)

@app.route("/ice_time")
@login_required
def iceTime():
    hLast = float(lm.icetimeLast(g.sessID))
    hCurrent = float(lm.icetimeCurrent(g.sessID))
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

    inlineLast = float(lm.inlinetimeLast(g.sessID))
    inlineCurrent = float(lm.inlinetimeCurrent(g.sessID))
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

    pData = lm.punchCard(g.sessID)
    return render_template('etemp_icetime.html', ses=session, costs=g.costs, hours=g.hours, mPVC=g.mPVC, maint=g.maint, chart_body=g.sessfull, thour=g.hours[2], hStatus=hResults, inlineStatus=inlineResults, modal1=g.modalSessions, calDate=g.now, pData=pData)


### JSON/API Stuff ###
@app.route('/api/json/areaTest', methods=['GET'])
@login_required
def areaTest():
    JSONsession = json.loads(lj.areaTest(g.sessID))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/budget', methods=['GET'])
@login_required
def budget():
    JSONsession = json.loads(lj.budget(g.sessID))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/maintClock', methods=['GET'])
@login_required
def maintClock():
    JSONsession = json.loads(lj.maintClock(g.sessID))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/monthlyPie', methods=['GET'])
@login_required
def monthlyPie():
    JSONsession = json.loads(lj.monthlyPie(g.sessID))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/monthlyPieCost', methods=['GET'])
@login_required
def monthlyPieCost():
    JSONsession = json.loads(lj.monthlyPieCost(g.sessID))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/sessionsArea', methods=['GET'])
@login_required
def sessionsArea():
    JSONsession = json.loads(lj.sessionsArea(g.sessID))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/sessionsFull', methods=['GET'])
@login_required
def sessionsFull():
    JSONsession = json.loads(lj.sessionsFull(g.sessID))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/sessionsBrief', methods=['GET'])
@login_required
def sessionsBrief():
    JSONsession = json.loads(lj.sessionsBrief(g.sessID))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp


@app.route('/submit_modalSession', methods=['POST'])
@login_required
def submit_modalSession():
    if request.method == 'POST':
        iceDate = request.form['date']
        iceTime = request.form['ice_time']
        iceCost = request.form['ice_cost']
        iceType = request.form['skate_type']
        iceLoc = request.form['rLocation']
        iceCoach = request.form['coach']
        coachTime = request.form['coach_time']

        if int(iceType) == 9 or int(iceType) == 10:
            skates = 0
        else:
            skates = g.ice

        sql = """insert into ice_time(date,ice_time,ice_cost,skate_type,coach_time,coach_id,rink_id,uSkaterUUID,uSkaterConfig)values(%s, %s, %s, %s, %s, %s, %s, %s, %s) """
        recordTuple = (iceDate,iceTime,iceCost,iceType,coachTime,iceCoach,iceLoc,g.sessID,skates)
        lm.dbinsert(sql, recordTuple)
        return redirect(request.referrer)
    else:
        return redirect(request.referrer)

@app.route('/submit_modalMaintenance', methods=['POST'])
@login_required
def submit_modalMaintenance():
    uSuid = session.get('uSkaterUUID')

    if request.method == 'POST':
        mDate = request.form['m_date']
        mOn = request.form['m_hours_on']
        mCost = request.form['m_cost']
        mLocation = request.form['locationID']

        sql = """insert into maintenance(m_date,m_hours_on,m_cost,m_location,conf_id,uSkaterUUID)values(%s, %s, %s, %s, %s,%s) """
        recordTuple = (mDate,mOn,mCost,mLocation,g.ice,g.sessID)
        lm.dbinsert(sql, recordTuple)
        return redirect(request.referrer)
    else:
        return redirect(request.referrer)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, use_reloader=True, debug=True)
