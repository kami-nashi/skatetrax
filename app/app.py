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
global AnotherUUID
@app.before_request
def globalStuff():


    # Look to see if we're logged in. If not, ignore user specific stuff and move on
    g.AuthSkaterUUID = None
    if g.AuthSkaterUUID == None:
        pass
    else:
        # Global Stuff
        g.now = datetime.date.today()
        g.modalSessions = lj.sessionModal()
        g.costs = lm.addCostsTotal(session.get('uSkaterUUID'))
        g.hours = lm.addHoursTotal(session.get('uSkaterUUID'))
        g.cHours = lm.monthlyCoachTime(session.get('uSkaterUUID'))
        g.sHours = lm.monthlyIceTime(session.get('uSkaterUUID'))
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
# Landing Page
@app.route('/welcome')
def index():
    return render_template('unauth_welcome.html')

# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    sql = "select * from uSkaterConfig where uSkaterUUID = %s"
    subUserUUID = session['sUUID']
    results = lm.dbconnect(sql,subUserUUID)
    maint = lm.uMantenanceV2(AuthSkaterUUID)
    sessions = lm.sessionsBrief(AuthSkaterUUID)
    return render_template('etemp_dashboard.html', ses=session, costs=g.costs, hours=g.mHours, maint=maint, chart_body=sessions, thour=g.hours[2], modal1=g.modalSessions, calDate=g.now)  # render a template
    # return "Hello, World!"  # return a string

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
            else:
                pass
            flash('You were logged in.')
            return redirect(url_for('dashboard'))
    return render_template('unauth_login.html', error=error)


@app.route("/dashboard")
@login_required
def dashboard():
    uSuid = session.get('uSkaterUUID')
    print('SUID IS: ', uSuid)
    maint = lm.uMantenanceV2(uSuid)
    sessionTable = lm.sessionsBrief(uSuid)
    modal1 = lj.sessionModal()
    hours = lm.addHoursTotal(uSuid)
    now = datetime.date.today()
    costs = lm.addCostsTotal(uSuid)
    cHours = lm.monthlyCoachTime(uSuid)
    sHours = lm.monthlyIceTime(uSuid)
    uHours = math.ceil(sHours[0]['monthly_ice']*4)/4-math.ceil(cHours[0]['monthly_coach']*4)/4
    mHours = [uHours, math.ceil(cHours[0]['monthly_coach']*4)/4]

    return render_template('etemp_dashboard.html', modal1=modal1, ses=session, thour=hours[2], hours=mHours, costs=costs, maint=maint, chart_body=sessionTable )


@app.route("/journal")
@login_required
def journal():
    uSuid = session.get('uSkaterUUID')
    print('SUID IS: ', uSuid)
    maint = lm.uMantenanceV2(uSuid)
    sessionTable = lm.sessionsBrief(uSuid)
    modal1 = lj.sessionModal()
    hours = lm.addHoursTotal(uSuid)
    now = datetime.date.today()
    costs = lm.addCostsTotal(uSuid)
    cHours = lm.monthlyCoachTime(uSuid)
    sHours = lm.monthlyIceTime(uSuid)
    uHours = math.ceil(sHours[0]['monthly_ice']*4)/4-math.ceil(cHours[0]['monthly_coach']*4)/4
    mHours = [uHours, math.ceil(cHours[0]['monthly_coach']*4)/4]
    jDate = request.args.get('date', default = '', type = str)
    if jDate == '':
        jTable = lm.jVideos(uSuid,jv=0)
    else:
        print(jDate, 'its not empty')
        jTable = lm.jVideos(uSuid,jDate)
    return render_template('etemp_journals.html', ses=session, thour=hours[2], modal1=modal1, calDate=now, journalTable=jTable)

@app.route("/skater_overview")
@login_required
def skater_overview():

    uSuid = session.get('uSkaterUUID')
    print('SUID IS: ', uSuid)
    maint = lm.uMantenanceV2(uSuid)
    sessionTable = lm.sessionsBrief(uSuid)
    modal1 = lj.sessionModal()
    hours = lm.addHoursTotal(uSuid)
    now = datetime.date.today()
    costs = lm.addCostsTotal(uSuid)
    cHours = lm.monthlyCoachTime(uSuid)
    sHours = lm.monthlyIceTime(uSuid)
    uHours = math.ceil(sHours[0]['monthly_ice']*4)/4-math.ceil(cHours[0]['monthly_coach']*4)/4
    mHours = [uHours, math.ceil(cHours[0]['monthly_coach']*4)/4]

    sOff = lm.skaterOffBlades(uSuid)
    sIce = lm.skaterIceBlades(uSuid)
    return render_template('etemp_skater_overview.html',ses=session, thour=hours[2], modal1=modal1, skateOff=sOff, skateIce=sIce)

@app.route("/maintenance")
@login_required
def maintenance():

    uSuid = session.get('uSkaterUUID')
    print('SUID IS: ', uSuid)
    maint = lm.uMantenanceV2(uSuid)
    sessionTable = lm.sessionsBrief(uSuid)
    modal1 = lj.sessionModal()
    hours = lm.addHoursTotal(uSuid)
    now = datetime.date.today()
    costs = lm.addCostsTotal(uSuid)
    cHours = lm.monthlyCoachTime(uSuid)
    sHours = lm.monthlyIceTime(uSuid)
    uHours = math.ceil(sHours[0]['monthly_ice']*4)/4-math.ceil(cHours[0]['monthly_coach']*4)/4
    mHours = [uHours, math.ceil(cHours[0]['monthly_coach']*4)/4]

    maint = lm.uMantenanceV2(uSuid)
    sessions = lm.sessionsBrief(uSuid)
    maintTable = lm.maintTable(uSuid)
    return render_template('etemp_maintenance.html', ses=session, costs=costs, hours=hours, maint=maint, chart_body=sessions, thour=hours[2], modal1=modal1, calDate=now,maintTable=maintTable)

@app.route("/ice_time")
@login_required
def iceTime():

    uSuid = session.get('uSkaterUUID')
    print('SUID IS: ', uSuid)
    maint = lm.uMantenanceV2(uSuid)
    sessionTable = lm.sessionsBrief(uSuid)
    modal1 = lj.sessionModal()
    hours = lm.addHoursTotal(uSuid)
    now = datetime.date.today()
    costs = lm.addCostsTotal(uSuid)
    cHours = lm.monthlyCoachTime(uSuid)
    sHours = lm.monthlyIceTime(uSuid)
    uHours = math.ceil(sHours[0]['monthly_ice']*4)/4-math.ceil(cHours[0]['monthly_coach']*4)/4
    mHours = [uHours, math.ceil(cHours[0]['monthly_coach']*4)/4]

    maint = lm.uMantenanceV2(uSuid)
    sessions = lm.sessionsFull(uSuid)
    hLast = float(lm.icetimeLast(uSuid))
    hCurrent = float(lm.icetimeCurrent(uSuid))
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

    inlineLast = float(lm.inlinetimeLast(uSuid))
    inlineCurrent = float(lm.inlinetimeCurrent(uSuid))
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

    pData = lm.punchCard(uSuid)
    return render_template('etemp_icetime.html', ses=session, costs=costs, hours=hours, maint=maint, chart_body=sessions, thour=hours[2], hStatus=hResults, inlineStatus=inlineResults, modal1=modal1, calDate=now, pData=pData)

@app.route('/api/json/areaTest', methods=['GET'])
@login_required
def areaTest():
    uSuid = session.get('uSkaterUUID')
    JSONsession = json.loads(lj.areaTest(uSuid))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/sessionsArea', methods=['GET'])
@login_required
def sessionsArea():
    uSuid = session.get('uSkaterUUID')
    JSONsession = json.loads(lj.sessionsArea(uSuid))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/sessionsFull', methods=['GET'])
@login_required
def sessionsFull():
    uSuid = session.get('uSkaterUUID')
    JSONsession = json.loads(lj.sessionsFull(uSuid))
    jsession = json.dumps(JSONsession, indent=4)
    resp = Response(jsession, status=200, mimetype='application/json')
    return resp

@app.route('/api/json/sessionsBrief', methods=['GET'])
@login_required
def sessionsBrief():
    uSuid = session.get('uSkaterUUID')
    JSONsession = json.loads(lj.sessionsBrief(uSuid))
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

        sql = """insert into ice_time(date,ice_time,ice_cost,skate_type,coach_time,coach_id,rink_id,uSkaterUUID)values(%s, %s, %s, %s, %s, %s, %s, %s) """
        recordTuple = (iceDate,iceTime,iceCost,iceType,coachTime,iceCoach,iceLoc,AuthSkaterUUID)
        lm.dbinsert(sql, recordTuple)
        return redirect(url_for('index'))
        #return redirect(request.referrer)
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

        sql = """insert into maintenance(m_date,m_hours_on,m_cost,m_location,uSkaterUUID)values(%s, %s, %s, %s,%s) """
        recordTuple = (mDate,mOn,mCost,mLocation,uSuid)
        lm.dbinsert(sql, recordTuple)
        return redirect(request.referrer)
    else:
        return redirect(request.referrer)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, use_reloader=True, debug=True)
