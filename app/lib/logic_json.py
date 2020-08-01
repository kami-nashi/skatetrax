import lib.logic_main as st
import json
import math

def maintClock(uSkaterUUID=None):
    vTUP = uSkaterUUID
    maint = st.uMantenanceV2(vTUP)
    dump = [maint[3],maint[4],maint[2]]
    jdump = json.dumps(dump, indent=4, default=float)
    return jdump

def budget(uSkaterUUID=None):
    vTUP = uSkaterUUID
    dump = st.addCostsAPI(uSkaterUUID)
    jdump = json.dumps(dump, indent=4, default=float)
    return jdump

def monthlyPie(uSkaterUUID=None):
    vTUP = uSkaterUUID
    cHours = st.monthlyCoachTime(uSkaterUUID)
    sHours = st.monthlyIceTime(uSkaterUUID)
    uHours = math.ceil(sHours[0]['monthly_ice']*4)/4-math.ceil(cHours[0]['monthly_coach']*4)/4
    mPVC = [uHours, math.ceil(cHours[0]['monthly_coach']*4)/4, float(sHours[0]['ice_cost'])]
    yIce = st.addHoursTotal(uSkaterUUID)[0]
    yCoach = st.addHoursTotal(uSkaterUUID)[1]
    dump = [ mPVC[0], mPVC[1],yIce, yCoach ]
    jdump = json.dumps(dump, indent=4, default=float)
    return jdump

def monthlyPieCost(uSkaterUUID=None):
    vTUP = uSkaterUUID
    ycIce = math.ceil(float(st.icetimeAdd(vTUP)[1])*4)/4
    ycCoach = math.ceil(float(st.coachtimeAdd2(vTUP)[0])*4)/4
    mcIce = math.ceil(float(st.monthlyIceTime(vTUP)[0]['ice_cost'])*4)/4
    mcCoach = math.ceil(float(st.monthlycoachtimeAdd2(vTUP)[0])*4)/4
    dump = [mcIce, mcCoach,ycIce,ycCoach]
    jdump = json.dumps(dump, indent=4, default=float)
    return jdump

def sessionsArea(uSkaterUUID=None):
    vTUP = (uSkaterUUID, uSkaterUUID)
    sql= "SELECT date_format(bam.date, '%%Y-%%m') as bDate, IFNULL(date_format(ice.date, '%%Y-%%m'), date_format(bam.date, '%%Y-%%m')) as iDate, IFNULL(sum(ice.ice_time/60), 0) as iTime, IFNULL(sum(ice.coach_time/60), 0) as cTime, IFNULL(ice.uSkaterUUID, %s) as uSuuid FROM (select * from ice_time where uSkaterUUID = %s) ice right JOIN baMonths bam ON date_format(bam.date, '%%Y-%%m') = date_format(ice.date, '%%Y-%%m') group by bam.date order by bam.date desc"
    results = st.dbconnect(sql, vTUP)
    dump = []
    for i in results:
            dump.append({'date': str(i['bDate']), 'ice_time': format(float(i['iTime']), '.2f'), 'coach_time': format(math.ceil(float(i['cTime'])*4)/4, '.2f'), 'uuid': i['uSuuid']})
    jdump = json.dumps(dump, indent=4, default=str)
    return jdump


def sessionsFull(uSkaterUUID=None):
    vTUP = (uSkaterUUID, uSkaterUUID)
    sql = 'select * from ice_time, coaches, locations, ice_type where ice_time.uSkaterUUID = %s and ice_time.coach_id = ice_time.coach_id and coaches.id = ice_time.coach_id and locations.id = ice_time.rink_id and ice_type.id = ice_time.skate_type and ice_time.date order by date desc'
    results = st.dbconnect(sql,vTUP)
    dump = []
    for i in results:
            dump.append({'id': i['id'], 'date': i['date'], 'ice_time': int(i['ice_time'])/60, 'ice_cost': i['ice_cost'],
                         'skate_type': i['skate_type'], 'coach_time': format(math.ceil(float(i['coach_time'])*4)/4, '.2f'), 'coach_id': i['coach_id'],
                         'rink_id': i['rink_id'], 'has_video': i['has_video'], 'has_notes': i['has_notes'],
                         'coach_fname': i['coach_fname'], 'coach_lname': i['coach_lname'],
                         'coach_rate': i['coach_rate'], 'location_id': i['location_id'],
                         'location_city': i['location_city'], 'location_state': i['location_state'], 'type': i['type']})
    jdump = json.dumps(dump, indent=4, default=str)
    return jdump

def sessionsBrief(uSkaterUUID=None):
    vTUP = (uSkaterUUID)
    sql = 'select * from ice_time, coaches, locations, ice_type where ice_time.uSkaterUUID = %s and ice_time.coach_id = ice_time.coach_id and coaches.id = ice_time.coach_id and locations.id = ice_time.rink_id and ice_type.id = ice_time.skate_type and ice_time.date > (NOW() - INTERVAL 14 DAY) ORDER BY date DESC'
    results = st.dbconnect(sql,vTUP)
    dump = []
    for i in results:
        dump.append({'id':i['id'],'date':i['date'],'ice_time':i['ice_time'],'ice_cost':i['ice_cost'],'skate_type':i['skate_type'],'coach_time':format(math.ceil(float(i['coach_time'])*4)/4, '.2f'),'coach_id':i['coach_id'],'rink_id':i['rink_id'],'has_video':i['has_video'],'has_notes':i['has_notes'],'coach_fname':i['coach_fname'],'coach_lname':i['coach_lname'],'coach_rate':i['coach_rate'],'location_id':i['location_id'],'location_city':i['location_city'],'location_state':i['location_state'],'type':i['type']})
    jdump = json.dumps(dump, indent=4, default=str)
    return jdump

def sessionModal():
    sqlCoach = 'select * from coaches'
    sqlRink = 'select * from locations'
    sqlType = 'select * from ice_type'
    rCoach = st.dbconnect(sqlCoach)
    rRink = st.dbconnect(sqlRink)
    rType = st.dbconnect(sqlType)
    results = [rCoach,rRink,rType]

    return results
