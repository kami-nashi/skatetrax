import lib.logic_main as st
import json
import math

def sessionsArea(uSkaterUUID):
    vTUP = uSkaterUUID
    sql = "SELECT MONTHNAME(date) as monthDate, SUM(ice_time/60) as sTime, SUM(coach_time/60) as cTime FROM ice_time where uSkaterUUID = %s GROUP BY YEAR(date), MONTH(date) ORDER BY DATE DESC LIMIT 12"
    results = st.dbconnect(sql,vTUP)
    dump = []
    for i in results:
            dump.append({'date': str(i['monthDate']), 'ice_time': int(i['sTime']), 'coach_time': format(math.ceil(float(i['cTime'])*4)/4, '.2f')})
    jdump = json.dumps(dump, indent=4, default=str)
    return jdump

def sessionsFull():
    sql = 'select * from ice_time, coaches, locations, ice_type where ice_time.coach_id = ice_time.coach_id and coaches.id = ice_time.coach_id and locations.id = ice_time.rink_id and ice_type.id = ice_time.skate_type and ice_time.date order by date desc'
    results = st.dbconnect(sql)
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

def sessionsBrief():
    sql = 'select * from ice_time, coaches, locations, ice_type where ice_time.coach_id = ice_time.coach_id and coaches.id = ice_time.coach_id and locations.id = ice_time.rink_id and ice_type.id = ice_time.skate_type and ice_time.date > (NOW() - INTERVAL 14 DAY) ORDER BY date DESC'
    results = st.dbconnect(sql)
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
