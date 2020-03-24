import pymysql
import configparser as conf

def dbconnect(sql):
   configParser = conf.RawConfigParser()
   configFilePath = r'/etc/skatetrax/settings.conf'
   configParser.read(configFilePath)

   host = configParser.get('dbconf', 'host')
   user = configParser.get('dbconf', 'user')
   password = configParser.get('dbconf', 'password')
   db = configParser.get('dbconf', 'db')

   con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
   cur = con.cursor()
   cur.execute(sql)
   tables = cur.fetchall()
   con.close()
   return tables

# Sums hours of current month
def icetimeCurrent():
    sql = 'SELECT ice_time FROM ice_time WHERE MONTH(CURDATE()) = MONTH(date) AND YEAR(CURDATE()) = YEAR(date)'
    results = dbconnect(sql)
    current = int(0)
    for i in results:
        current += i['ice_time']
    # Math - convert minutes to hours
    ice_hours = current/60
    return ice_hours

# Sums hours from previous month
def icetimeLast():
    sql = 'SELECT ice_time FROM ice_time WHERE MONTH(CURDATE()) - 1= MONTH(date) AND YEAR(CURDATE()) = YEAR(date)'
    results = dbconnect(sql)
    current = int(0)
    for i in results:
        current += i['ice_time']
    # Math - convert minutes to hours
    ice_hours = current/60
    return ice_hours

# Sums total amount of hours on ice and cost of time on ice
def icetimeAdd():
    ice = 0
    ice_cost = 0
    sql = 'select * from ice_time'
    results = dbconnect(sql)
    for i in results:
        ice += i['ice_time']
        ice_cost += i['ice_cost']
    ice_time = ice / 60
    query = [ice_time,ice_cost]
    return query

# Good luck figuring this one out. Sigh.
def coachtimeAdd2():
    coachTime = 0
    coachRate = 0
    coachConversion = 0
    coachCost = 0
    coachMinutes = 0
    sql = 'SELECT ice_time.*, coaches.* FROM ice_time, coaches WHERE ice_time.coach_id = coaches.id'
    results = dbconnect(sql)
    for i in results:
        coachMinutes += i['coach_time']
        coachTime = i['coach_time']
        coachRate =i['coach_rate']
        coachConversion = i['coach_rate'] / 30
        coachCost += coachTime * coachConversion
    coachHours = coachMinutes / 60
    coachTotal = coachMinutes * coachConversion
    query = [coachCost,coachHours,coachMinutes,coachRate,coachTime,coachConversion]
    return query

###############################################################
#
#  Maintenance Stuff
#
###############################################################

def maintenance():
    mHours = 0
    mCost = 0
    sql = 'select * from maintenance'
    results = dbconnect(sql)
    for i in results:
        mHours += i['m_hours_on']
        mCost += i['m_cost']
    iceTimeTotal = icetimeAdd()
    mOn = iceTimeTotal[1] - mHours
    mRemaining = 21 - mOn
    query = [mHours,mCost,mOn,mRemaining]
    return query

def addTotals():
    ice = icetimeAdd()
    coach = coachtimeAdd2()
    maint = maintenance()
    cost = [ice[0],coach[0],maint[1]]
    return cost

def addEventsC():
    cCost = 0
    sql= 'SELECT * FROM events_c'
    results = dbconnect(sql)
    for i in results:
        cCost +=i['e_cost']
    return cCost

def addEventsP():
    pCost = 0
    sql = 'SELECT * FROM events_p'
    results = dbconnect(sql)
    for i in results:
        pCost += i['e_cost']
    return pCost

def addEquip():
    eCost = 0
    sql = 'SELECT * FROM equip_manifest'
    results = dbconnect(sql)
    for i in results:
        eCost += i['cost_actual']
    return eCost

def addClub():
    cCost = 0
    sql = 'SELECT * FROM club_membership'
    results = dbconnect(sql)
    for i in results:
        cCost += i['club_cost']
    return cCost

def addSchool():
    classCost = 0
    sql = 'SELECT * FROM class_skate_school'
    results = dbconnect(sql)
    for i in results:
        classCost += i['class_cost']
    return classCost

def addCostsTotal():
    costMaint = maintenance()
    costClub = addClub()
    costClass = addSchool()
    costEquip = addEquip()
    costIce = icetimeAdd()
    eventsC = addEventsC()
    eventsP = addEventsP()
    timeCoach = coachtimeAdd2()

    total = (costEquip+costMaint[1]+costClass+eventsP+costClub+eventsC+costIce[1]+timeCoach)

    query = [costEquip,costMaint[1],costClass,eventsP,costClub,eventsC,costIce[1],timeCoach,total]
    return query

################################################################################################################
##						Calculate Punch Cards					      ##
################################################################################################################

def skateTotal():
    skateTotal = 0
    punchTotal = 0
    punchesTotal = 0
    sql = 'SELECT * FROM ice_time WHERE skate_type = 8'
    results = dbconnect(sql)
    for i in results:
        skateTotal += i['ice_time']
        punchDown = i['ice_time']/30
        punchesTotal += punchDown
    query = [skateTotal,punchesTotal]
    return query

def punchCard():
    punchTotal = 0
    sql = 'SELECT * FROM ice_punch'
    results = dbconnect(sql)
    for i in results:
        punchTotal += i['punch_time']
    return punchTotal
