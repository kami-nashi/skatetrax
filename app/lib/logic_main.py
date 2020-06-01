import pymysql
import configparser as conf
from collections import defaultdict

def dbconnect(sql):
   configParser = conf.RawConfigParser()
   configFilePath = r'/etc/skatetrax/settings.conf'
   configParser.read(configFilePath)

   host = configParser.get('dbconf', 'host')
   user = configParser.get('dbconf', 'user')
   password = configParser.get('dbconf', 'password')
   db = configParser.get('dbconf', 'db')

   con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
   cur = con.cursor()
   cur.execute(sql)
   tables = cur.fetchall()
   cur.connection.commit()
   con.close()
   return tables

def dbinsert(sql,recordTuple):
   configParser = conf.RawConfigParser()
   configFilePath = r'/etc/skatetrax/settings.conf'
   configParser.read(configFilePath)
   host = configParser.get('dbconf', 'host')
   user = configParser.get('dbconf', 'user')
   password = configParser.get('dbconf', 'password')
   db = configParser.get('dbconf', 'db')
   con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
   cur = con.cursor()
   cur.execute(sql, recordTuple)
   tables = cur.fetchall()
   cur.connection.commit()
   con.close()
   return tables

# Sums ice hours of current month
def icetimeCurrent():
    sql = 'SELECT ice_time FROM ice_time WHERE MONTH(CURDATE()) = MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type != 9 and skate_type != 10'
    results = dbconnect(sql)
    current = int(0)
    for i in results:
        current += i['ice_time']
    # Math - convert minutes to hours
    ice_hours = current/60
    return ice_hours

# Sums ice hours from previous month
def icetimeLast():
    sql = 'SELECT ice_time FROM ice_time WHERE MONTH(CURDATE()) - 1= MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type != 9 and skate_type != 10'
    results = dbconnect(sql)
    current = int(0)
    for i in results:
        current += i['ice_time']
    # Math - convert minutes to hours
    ice_hours = current/60
    return ice_hours

# Sums inline hours of current month
def inlinetimeCurrent():
    sql = 'SELECT ice_time FROM ice_time WHERE MONTH(CURDATE()) = MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type = 9 or skate_type = 10'
    results = dbconnect(sql)
    current = int(0)
    for i in results:
        current += i['ice_time']
    # Math - convert minutes to hours
    ice_hours = current/60
    return ice_hours

# Sums inline hours from previous month
def inlinetimeLast():
    sql = 'SELECT ice_time FROM ice_time WHERE MONTH(CURDATE()) - 1= MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type = 9 or skate_type = 10'
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
    sql = 'select * from ice_time where skate_type != 9 and skate_type != 10'
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
#  Maintenance Stuff
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
    mOn = (float(iceTimeTotal[0])-float(mHours))
    mRemaining = 21 - mOn
    query = [mHours,mCost,mOn,mRemaining]
    return query

def maintTable():
    sql = 'select * from maintenance, locations where maintenance.m_location = locations.id order by m_date desc'
    query = dbconnect(sql)
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
    total = (float(costEquip)+float(costMaint[1])+float(costClass)+float(eventsP)+float(costClub)+float(eventsC)+float(costIce[1])+float(timeCoach[0]))
    query = [costEquip,costMaint[1],costClass,eventsP,costClub,eventsC,costIce[1],timeCoach[0],total]
    return query

def addHoursTotal():
    hoursPract = icetimeAdd()
    hoursCoach = coachtimeAdd2()

    results = [hoursPract[0],hoursCoach[1]]
    return results

def sessionsBrief():
    sql = 'select * from ice_time, coaches, locations, ice_type where ice_time.coach_id = ice_time.coach_id and coaches.id = ice_time.coach_id and locations.id = ice_time.rink_id and ice_type.id = ice_time.skate_type and ice_time.date > (NOW() - INTERVAL 14 DAY) ORDER BY date DESC';
    results = dbconnect(sql)
    return results

def sessionsFull():
    sql = 'select * from ice_time, coaches, locations, ice_type where ice_time.coach_id = ice_time.coach_id and coaches.id = ice_time.coach_id and locations.id = ice_time.rink_id and ice_type.id = ice_time.skate_type and ice_time.date ORDER BY date DESC';
    results = dbconnect(sql)
    return results
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
    sql = 'select distinct punch_location from ice_punch'
    results = dbconnect(sql)
    rData = {}
    rResults = []
    for i in results:
        pTime = 0
        pCost = 0
        rinkId = str(i['punch_location'])
        pSql = 'select * from ice_punch where punch_location = ' + rinkId
        pResults = dbconnect(pSql)
        for z in pResults:
            pTime += z['punch_time']
            pCost += z['punch_cost']
            iceSql = 'select * from ice_time, locations where locations.id = ice_time.rink_id and skate_type = 8 and rink_id = '+ rinkId
        iResults = dbconnect(iceSql)
        iCost = 0
        iMinutes  = 0
        rinkName = ''
        for x in iResults:
            iCost += x['ice_cost']
            iMinutes += x['ice_time']
            rinkName = x['location_id']
            rinkPCST = x['pcs_time']
            rinkPunch = int(iMinutes)/int(rinkPCST)
        pPurchased = pTime/rinkPCST
        pUsed = iMinutes/rinkPCST
        pRemaining = (pTime - iMinutes)/rinkPCST
        rData = {'punches_used': int(pUsed),'punches_purchased': int(pPurchased), 'remainingPunches': int(pRemaining),'cost': pCost, 'rink': rinkName}
        rResults.append(rData)
    return rResults

def modalSessions():
    sql_coach = 'select * from coaches'
    sql_rink = 'select * from locations'
    sql_itype = 'select * from ice_type'
    result = dbconnect(sql_coach)
    other_result = dbconnect(sql_rink)
    ice_type = dbconnect(sql_itype)
    for i in ice_type:
       id = i['id']
       type = i['type']
    for i in result:
       id = i['id']
       fname = i['coach_fname']
    for i in other_result:
       id = i['id']
       location_id = i['location_id']

def jVideos(jv):
    if jv == 0:
        sql = 'SELECT ice_time.*, j_videos.* FROM ice_time, j_videos WHERE ice_time.has_video = 1 AND ice_time.date = j_videos.date order by ice_time.date desc'
    else:
        sql = "SELECT * FROM j_videos WHERE date = '" + str(jv) + "'"
    results = dbconnect(sql)
    return results

def skaterOffBlades():
    sql = 'select uSkaterBoots.bootsName, uSkaterBoots.bootsModel, uSkaterBoots.bootsSize, uSkaterBlades.bladesName, uSkaterBlades.bladesSize, uSkaterBlades.bladesModel from uSkaterConfig, uSkateConfig, uSkaterBoots, uSkaterBlades where uSkaterConfig.uSkaterUUID = uSkateConfig.uSkaterUUID and uSkaterConfig.uSkateComboOff = uSkateConfig.ID and uSkateConfig.uSkaterBootsID = uSkaterBoots.ID and uSkateConfig.uSkaterBladesID = uSkaterBlades.ID;'
    results = dbconnect(sql)
    return results

def skaterIceBlades():
    sql = 'select uSkaterBoots.bootsName, uSkaterBoots.bootsModel, uSkaterBoots.bootsSize, uSkaterBlades.bladesName, uSkaterBlades.bladesSize, uSkaterBlades.bladesModel from uSkaterConfig, uSkateConfig, uSkaterBoots, uSkaterBlades where uSkaterConfig.uSkaterUUID = uSkateConfig.uSkaterUUID and uSkaterConfig.uSkateComboIce = uSkateConfig.ID and uSkateConfig.uSkaterBootsID = uSkaterBoots.ID and uSkateConfig.uSkaterBladesID = uSkaterBlades.ID;'
    results = dbconnect(sql)
    return results
