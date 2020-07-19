import pymysql
import math
import configparser as conf
from collections import defaultdict

# sanitize know problem makers from user input strings
def stripper(str):
    chars = [';', '#', '--', '//', '/', '.', '!', '\s', '\S', '*', '?', '\t', '\n', '\r', '@', '\\', '\\\\', '"', "'", 'drop']
    if any((c in chars) for c in str):
        return True
    else:
        return False

def dbconnect(sql,vTUP=None):
   configParser = conf.RawConfigParser()
   configFilePath = r'/etc/skatetrax/settings.conf'
   configParser.read(configFilePath)

   host = configParser.get('dbconf', 'host')
   user = configParser.get('dbconf', 'user')
   password = configParser.get('dbconf', 'password')
   db = configParser.get('dbconf', 'db')

   con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
   cur = con.cursor()
   cur.execute(sql, vTUP)
   tables = cur.fetchall()
   cur.connection.commit()
   con.close()
   return tables

def dbinsert(sql,recordTuple):
   if not stripper(recordTuple):
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
def icetimeCurrent(uSkaterUUID):
    vTUP = uSkaterUUID
    sql = 'SELECT ice_time FROM ice_time WHERE uSkaterUUID = %s AND MONTH(CURDATE()) = MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type != 9 and MONTH(CURDATE()) = MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type != 10'
    results = dbconnect(sql, vTUP)
    current = int(0)
    for i in results:
        current += i['ice_time']
    # Math - convert minutes to hours
    ice_hours = current/60
    return ice_hours

# Sums ice hours from previous month
def icetimeLast(uSkaterUUID):
    sql = 'SELECT ice_time FROM ice_time WHERE uSkaterUUID = %s AND MONTH(CURDATE()) - 1= MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type != "9" or MONTH(CURDATE()) - 1= MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type != "10"'
    vTUP = uSkaterUUID
    results = dbconnect(sql,vTUP)
    current = int(0)
    for i in results:
        current += i['ice_time']
    # Math - convert minutes to hours
    ice_hours = current/60
    return ice_hours

# Sums inline hours of current month
def inlinetimeCurrent(uSkaterUUID):
    vTUP = (uSkaterUUID,uSkaterUUID)
    sql = 'SELECT ice_time FROM ice_time WHERE uSkaterUUID = %s AND MONTH(CURDATE()) = MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type = 9 or uSkaterUUID = %s AND MONTH(CURDATE()) = MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type = 10'
    results = dbconnect(sql,vTUP)
    current = int(0)
    for i in results:
        current += i['ice_time']
    # Math - convert minutes to hours
    ice_hours = current/60
    return ice_hours

# Sums inline hours from previous month
def inlinetimeLast(uSkaterUUID):
    vTUP = (uSkaterUUID,uSkaterUUID)
    sql = 'SELECT ice_time FROM ice_time WHERE uSkaterUUID = %s AND MONTH(CURDATE()) - 1= MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type = 9 or uSkaterUUID = %s AND MONTH(CURDATE()) - 1= MONTH(date) AND YEAR(CURDATE()) = YEAR(date) and skate_type = 10'
    results = dbconnect(sql,vTUP)
    current = int(0)
    for i in results:
        current += i['ice_time']
    # Math - convert minutes to hours
    ice_hours = current/60
    return ice_hours

# Sums total amount of hours on ice and cost of time on ice
def icetimeAdd(AuthSkaterUUID):
    ice = 0
    ice_cost = 0
    vTUP = (AuthSkaterUUID)
    sql = "SELECT * FROM ice_time WHERE uSkaterUUID = %s AND skate_type != '9' AND skate_type != '10'"
    results = dbconnect(sql, vTUP)
    for i in results:
        ice += i['ice_time']
        ice_cost += i['ice_cost']
    ice_time = ice / 60
    query = [ice_time,ice_cost]
    return query

def inlinetimeAdd(AuthSkaterUUID):
    ice = 0
    ice_cost = 0
    vTUP = (AuthSkaterUUID, vTUP)
    sql = "select * from ice_time where uSkaterUUID = %s AND skate_type = '9' or skate_type = '10'"
    results = dbconnect(sql)
    for i in results:
        ice += i['ice_time']
    ice_time = ice / 60
    query = ice_time
    return query

# Good luck figuring this one out. Sigh.
def coachtimeAdd2(AuthSkaterUUID):
    coachTime = 0
    coachRate = 0
    coachConversion = 0
    coachCost = 0
    coachMinutes = 0
    vTUP = (AuthSkaterUUID)
    sql = 'SELECT ice_time.*, coaches.* FROM ice_time, coaches WHERE ice_time.uSkaterUUID = %s AND ice_time.coach_id = coaches.id'
    results = dbconnect(sql, vTUP)
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

def monthlyIceTime(AuthSkaterUUID):
    vTUP = (AuthSkaterUUID)
    sql = "SELECT SUM(ice_time/60) AS monthly_ice FROM ice_time WHERE uSkaterUUID = %s AND date > (DATE_SUB(CURDATE(), INTERVAL 1 MONTH))"
    results = dbconnect(sql, vTUP)
    return results

def monthlyCoachTime(AuthSkaterUUID):
    vTUP = (AuthSkaterUUID)
    sql = "SELECT SUM(coach_time/60) AS monthly_coach FROM ice_time WHERE uSkaterUUID = %s AND date > (DATE_SUB(CURDATE(), INTERVAL 1 MONTH))"
    results = dbconnect(sql, vTUP)
    return results

###############################################################
#  Maintenance Stuff
###############################################################

def maintenance(AuthSkaterUUID):
    mHours = 0
    mCost = 0
    vTUP = AuthSkaterUUID
    sql = 'select * from maintenance WHERE uSkaterUUID = %s'
    results = dbconnect(sql,vTUP)
    for i in results:
        mHours += i['m_hours_on']
        mCost += i['m_cost']
    iceTimeTotal = icetimeAdd(AuthSkaterUUID)
    mOn = (float(iceTimeTotal[0])-float(mHours))
    mRemaining = 21 - mOn
    query = [mHours,mCost,mOn,mRemaining]
    return query

def maintTable(AuthSkaterUUID):
    vTUP = AuthSkaterUUID
    sql = 'select * from maintenance, locations where uSkaterUUID = %s AND maintenance.m_location = locations.id order by m_date desc'
    query = dbconnect(sql,vTUP)
    return query

def addTotals(AuthSkaterUUID):
    ice = icetimeAdd(AuthSkaterUUID)
    coach = coachtimeAdd2(AuthSkaterUUID)
    maint = maintenance(AuthSkaterUUID)
    cost = [ice[0],coach[0],maint[1]]
    return cost

def addEventsC(AuthSkaterUUID):
    cCost = 0
    vTUP = AuthSkaterUUID
    sql= 'SELECT * FROM events_c WHERE uSkaterUUID = %s'
    results = dbconnect(sql,vTUP)
    for i in results:
        cCost +=i['e_cost']
    return cCost

def addEventsP(AuthSkaterUUID):
    pCost = 0
    vTUP = AuthSkaterUUID
    sql = 'SELECT * FROM events_p WHERE uSkaterUUID = %s'
    results = dbconnect(sql,vTUP)
    for i in results:
        pCost += i['e_cost']
    return pCost

def addEquip(AuthSkaterUUID):
    eCost = 0
    vTUP = (AuthSkaterUUID,AuthSkaterUUID,AuthSkaterUUID)
    sql = 'SELECT equip_manifest.cost_actual FROM equip_manifest WHERE equip_manifest.uSkaterUUID = %s UNION ALL SELECT uSkaterBlades.bladesPurchAmount FROM uSkaterBlades WHERE uSkaterBlades.uSkaterUUID = %s UNION ALL SELECT uSkaterBoots.bootsPurchAmount FROM uSkaterBoots WHERE uSkaterBoots.uSkaterUUID = %s'
    sql1 = 'SELECT * FROM equip_manifest WHERE uSkaterUUID = %s '
    sql2 = 'SELECT * FROM uSkaterBlades WHERE uSkaterUUID = %s '
    sql3 = sql2 = 'SELECT * FROM uSkaterBoots WHERE uSkaterUUID = %s '
    results = dbconnect(sql,vTUP)
    for i in results:
        eCost += i['cost_actual']
    return eCost

def addClub(AuthSkaterUUID):
    cCost = 0
    vTUP = AuthSkaterUUID
    sql = 'SELECT * FROM club_membership WHERE uSkaterUUID = %s'
    results = dbconnect(sql,vTUP)
    for i in results:
        cCost += i['club_cost']
    return cCost

def addSchool(AuthSkaterUUID):
    classCost = 0
    vTUP = AuthSkaterUUID
    sql = 'SELECT * FROM class_skate_school WHERE uSkaterUUID = %s'
    results = dbconnect(sql,vTUP)
    for i in results:
        classCost += i['class_cost']
    return classCost

def addCostsTotal(AuthSkaterUUID):
    # x = format(value, ',d')
    costMaint = maintenance(AuthSkaterUUID)
    costClub = addClub(AuthSkaterUUID)
    costClass = addSchool(AuthSkaterUUID)
    costEquip = addEquip(AuthSkaterUUID)
    costIce = icetimeAdd(AuthSkaterUUID)
    eventsC = addEventsC(AuthSkaterUUID)
    eventsP = addEventsP(AuthSkaterUUID)
    timeCoach = coachtimeAdd2(AuthSkaterUUID)
    total = (float(costEquip)+float(costMaint[1])+float(costClass)+float(eventsP)+float(costClub)+float(eventsC)+float(costIce[1])+float(timeCoach[0]))
    query = [costEquip,costMaint[1],costClass,eventsP,costClub,eventsC,costIce[1],timeCoach[0],total]
    return query

def addHoursTotal(AuthSkaterUUID):
    hoursPract = icetimeAdd(AuthSkaterUUID)
    hoursCoach = coachtimeAdd2(AuthSkaterUUID)
    hoursDiff = round(hoursPract[0], 2)-math.ceil(hoursCoach[1]*4)/4

    results = [hoursDiff,math.ceil(hoursCoach[1]*4)/4,hoursPract]
    return results

def sessionsBrief(AuthSkaterUUID):
    vTUP = (AuthSkaterUUID)
    sql = 'select * from ice_time, coaches, locations, ice_type where uSkaterUUID = %s AND ice_time.coach_id = ice_time.coach_id and coaches.id = ice_time.coach_id and locations.id = ice_time.rink_id and ice_type.id = ice_time.skate_type and ice_time.date > (NOW() - INTERVAL 14 DAY) ORDER BY date DESC';
    results = dbconnect(sql, vTUP)
    return results

def sessionsFull(AuthSkaterUUID):
    vTUP = (AuthSkaterUUID)
    sql = 'select * from ice_time, coaches, locations, ice_type where uSkaterUUID = %s AND ice_time.coach_id = ice_time.coach_id and coaches.id = ice_time.coach_id and locations.id = ice_time.rink_id and ice_type.id = ice_time.skate_type and ice_time.date ORDER BY date DESC';
    results = dbconnect(sql, vTUP)
    return results
################################################################################################################
##						Calculate Punch Cards					      ##
################################################################################################################

def skateTotal(AuthSkaterUUID):
    skateTotal = 0
    punchTotal = 0
    punchesTotal = 0
    vTUP = (AuthSkaterUUID)
    sql = 'SELECT * FROM ice_time WHERE uSkaterUUID = %s AND skate_type = 8'
    results = dbconnect(sql,vTUP)
    for i in results:
        skateTotal += i['ice_time']
        punchDown = i['ice_time']/30
        punchesTotal += punchDown
    query = [skateTotal,punchesTotal]
    return query

def punchCard(AuthSkaterUUID):
    vTUP = (AuthSkaterUUID)
    sql = 'select distinct punch_location from ice_punch WHERE uSkaterUUID = %s'
    results = dbconnect(sql,vTUP)
    rData = {}
    rResults = []
    for i in results:
        pTime = 0
        pCost = 0
        rinkId = str(i['punch_location'])
        pSql = 'select * from ice_punch where uSkaterUUID = %s AND punch_location = %s'
        vTUP = (AuthSkaterUUID,rinkId)
        pResults = dbconnect(pSql,vTUP)
        for z in pResults:
            pTime += z['punch_time']
            pCost += z['punch_cost']
            iceSql = 'select * from ice_time, locations where uSkaterUUID = %s AND locations.id = ice_time.rink_id and skate_type = 8 and rink_id = %s'
        iResults = dbconnect(iceSql,vTUP)
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

def jVideos(AuthSkaterUUID,jv):
    vTUP = (AuthSkaterUUID,AuthSkaterUUID)
    if jv == 0:
        sql = 'SELECT ice_time.*, j_videos.* FROM ice_time, j_videos WHERE j_videos.uSkaterUUID = %s AND ice_time.uSkaterUUID = %s AND ice_time.has_video = 1 AND ice_time.date = j_videos.date order by ice_time.date desc'
    else:
        vTUP = (AuthSkaterUUID,str(jv))
        sql = "SELECT * FROM j_videos WHERE uSkaterUUID = %s AND date = %s"
    results = dbconnect(sql,vTUP)
    return results

def skaterOffBlades(AuthSkaterUUID):
    vTUP = AuthSkaterUUID
    sql = 'select uSkaterBoots.bootsName, uSkaterBoots.bootsModel, uSkaterBoots.bootsSize, uSkaterBlades.bladesName, uSkaterBlades.bladesSize, uSkaterBlades.bladesModel from uSkaterConfig, uSkateConfig, uSkaterBoots, uSkaterBlades where uSkaterConfig.uSkaterUUID = %s AND uSkaterConfig.uSkaterUUID = uSkateConfig.uSkaterUUID and uSkaterConfig.uSkateComboOff = uSkateConfig.ID and uSkateConfig.uSkaterBootsID = uSkaterBoots.ID and uSkateConfig.uSkaterBladesID = uSkaterBlades.ID;'
    results = dbconnect(sql,vTUP)
    return results

def skaterIceBlades(AuthSkaterUUID):
    vTUP = AuthSkaterUUID
    sql = 'select uSkaterBoots.bootsName, uSkaterBoots.bootsModel, uSkaterBoots.bootsSize, uSkaterBlades.bladesName, uSkaterBlades.bladesSize, uSkaterBlades.bladesModel from uSkaterConfig, uSkateConfig, uSkaterBoots, uSkaterBlades where uSkaterConfig.uSkaterUUID = %s AND uSkaterConfig.uSkaterUUID = uSkateConfig.uSkaterUUID and uSkaterConfig.uSkateComboIce = uSkateConfig.ID and uSkateConfig.uSkaterBootsID = uSkaterBoots.ID and uSkateConfig.uSkaterBladesID = uSkaterBlades.ID;'
    results = dbconnect(sql,vTUP)
    return results
