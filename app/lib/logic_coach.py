import lib.logic_main as st

def coachListStudents(uSkaterUUID=None):
    vTUP = uSkaterUUID,1
    sql = 'select * from uSkaterConfig where activeCoach = %s and uSkaterType = %s'
    results = st.dbconnect(sql,vTUP)
    return results
