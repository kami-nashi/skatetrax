import lib.logic_main as st

################################################################################
# Pull all skater info from the uSkaterConfig tables for coaches
def uCoachInfo(AuthSkaterUUID):
    vTUP = (AuthSkaterUUID)
    #sql = 'select * from uSkaterConfig where uSkaterUUID = %s'
    sql = 'select * from uSkaterConfig where uSkaterConfig.uSkaterUUID = %s'
    results = st.dbconnect(sql,vTUP)
    return results

################################################################################

def coachListStudents(uSkaterUUID=None):
    vTUP = uSkaterUUID,1
    sql = 'select * from uSkaterConfig where activeCoach = %s and uSkaterType = %s'
    results = st.dbconnect(sql,vTUP)
    return results

def coachStudentHours(uSkaterUUID=None):
    vTUP = uSkaterUUID,1
    sql = 'select * from uSkaterConfig where activeCoach = %s and uSkaterType = %s'
    results = st.dbconnect(sql,vTUP)
    return results

def studentVideos(uSkaterUUID=None):
    vTUP = (uSkaterUUID)
    if uSkaterUUID == 0:
        print('welp. its empty')
    else:
        vTUP = (uSkaterUUID)
        sql = "SELECT * FROM j_videos WHERE uSkaterUUID = %s ORDER BY date desc"
    results = st.dbconnect(sql,vTUP)
    return results
