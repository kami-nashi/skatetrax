import st_dbConf

currencyFormat = st_dbConf.currencyUSD.default

#def addCoachTime(AuthSkaterUUID):
#    coachTimeSlot = "select coach_time from coaches where "
#    if coachTimeSlot = 60:
#        coachInMinutes = coachTimeSlot/60
#    elif coachTimeSlot = 30:
#        coachInMinutes = (coachTimeSlot*2)60
#    else:
#        coachInMinutes = 0
        
        


def addTotals(AuthSkaterUUID):
    ice = icetimeAdd(AuthSkaterUUID)
    coach = coachtimeAdd2(AuthSkaterUUID)
    maint = uMantenanceV2(AuthSkaterUUID)
    cost = [ice[0],coach[0],maint[5]]
    return cost


def addCamp(AuthSkaterUUID):
    '''
    Get sum of all camp fees
    '''

    sql = '''
    SELECT sum(camp_cost) as campCost
    FROM skate_camp
    WHERE uSkaterUUID = %s
    '''

    results = st_dbConf.dbconnect(sql, AuthSkaterUUID)
    return currencyFormat(results[0]['campCost'])


def addClub(AuthSkaterUUID):
    '''
    Get sum of all club membership fees
    '''

    sql = '''
    SELECT sum(club_cost) as clubCost
    FROM club_membership
    WHERE uSkaterUUID = %s
    '''

    results = st_dbConf.dbconnect(sql, AuthSkaterUUID)
    return currencyFormat(results[0]['clubCost'])


def addCoachTimeCost(AuthSkaterUUID):
    '''
    Get sum of cost of time with coach
    '''

    sql = '''
    SELECT coach_time coach_id
    FROM ice_time
    WHERE uSkaterUUID = %s
    '''

    results = st_dbConf.dbconnect(sql, AuthSkaterUUID)
    return currencyFormat(results[0]['iceTime'])


def addEquip(AuthSkaterUUID):
    '''
    Get sum of equip table, blades table, and boots table for current skater
    '''

    equipCostQuery = '''
    SELECT sum(cost_actual) as costActual
    FROM equip_manifest
    WHERE uSkaterUUID = %s
    '''
    bootsCostQuery = '''
    SELECT sum(bootsPurchAmount) as bootsAmount
    FROM uSkaterBoots
    WHERE uSkaterUUID = %s
    '''
    bladesCostQuery = '''
    SELECT sum(bladesPurchAmount) as bladesAmount
    FROM uSkaterBlades
    WHERE uSkaterUUID = %s
    '''

    equipCostResults = st_dbConf.dbconnect(equipCostQuery, AuthSkaterUUID)[0]['costActual']
    bootsCostResults = st_dbConf.dbconnect(bootsCostQuery, AuthSkaterUUID)[0]['bootsAmount']
    bladesCostResults = st_dbConf.dbconnect(bladesCostQuery, AuthSkaterUUID)[0]['bladesAmount']

    results = float(currencyFormat(equipCostResults)) + float(currencyFormat(bootsCostResults)) + float(currencyFormat(bladesCostResults))

    return results


def addEventsC(AuthSkaterUUID):
    '''
    Get sum of all events of a skater
    '''

    sql = '''
    SELECT sum(e_cost) as eventCost
    FROM events_c
    WHERE uSkaterUUID = %s
    '''

    results = st_dbConf.dbconnect(sql, AuthSkaterUUID)
    return currencyFormat(results[0]['eventCost'])


def addEventsP(AuthSkaterUUID):
    '''
    Get sum of all performance fees
    '''

    sql = '''
    SELECT sum(e_cost) as eventCost
    FROM events_p
    WHERE uSkaterUUID = %s
    '''

    results = st_dbConf.dbconnect(sql, AuthSkaterUUID)
    return currencyFormat(results[0]['eventCost'])


def addEventsT(AuthSkaterUUID):
    '''
    Get sum of things in the T table.  not sure what this is anymore though
    '''

    sql = '''
    SELECT sum(e_cost) as eventCost
    FROM events_t
    WHERE uSkaterUUID = %s
    '''

    results = st_dbConf.dbconnect(sql, AuthSkaterUUID)
    return currencyFormat(results[0]['eventCost'])


def addIceTimeCost(AuthSkaterUUID):
    '''
    Get sum of all time on ice
    '''

    sql = '''
    SELECT sum(ice_time) as iceTime
    FROM ice_time
    WHERE uSkaterUUID = %s
    '''

    results = st_dbConf.dbconnect(sql, AuthSkaterUUID)
    return currencyFormat(results[0]['iceTime'])


def addSchool(AuthSkaterUUID):
    '''
    Get sum of the school fees
    '''

    sql = '''
    SELECT sum(class_cost) as classCost
    FROM class_skate_school
    WHERE uSkaterUUID = %s
    '''

    results = st_dbConf.dbconnect(sql, AuthSkaterUUID)
    return currencyFormat(results[0]['classCost'])


AuthSkaterUUID = 1
print(addEquip(AuthSkaterUUID), addSchool(AuthSkaterUUID), addCamp(AuthSkaterUUID), addClub(AuthSkaterUUID), addEventsC(AuthSkaterUUID), addEventsP(AuthSkaterUUID), addEventsT(AuthSkaterUUID))


def addCostsTotal(AuthSkaterUUID=None):
    # x = format(value, ',d')
    costMaint = uMantenanceV2(AuthSkaterUUID)
    costClub = addClub(AuthSkaterUUID)
    costClass = addSchool(AuthSkaterUUID)
    costEquip = addEquip(AuthSkaterUUID)
    costIce = icetimeAdd(AuthSkaterUUID)
    eventsC = addEventsC(AuthSkaterUUID)
    eventsP = addEventsP(AuthSkaterUUID)
    timeCoach = coachtimeAdd2(AuthSkaterUUID)
    total = (float(costEquip)+float(costMaint[5])+float(costClass)+float(eventsP)+float(costClub)+float(eventsC)+float(costIce[1])+float(timeCoach[0]))
    query = [costEquip,costMaint[5],costClass,eventsP,costClub,eventsC,costIce[1],timeCoach[0],total]
    return query


def addCostsAPI(AuthSkaterUUID=None):
    costCoaching = coachtimeAdd2(AuthSkaterUUID)
    costIcetime = icetimeAdd(AuthSkaterUUID)
    costEquip = addEquip(AuthSkaterUUID)
    costMaint = uMantenanceV2(AuthSkaterUUID)
    costComp = float(addEventsC(AuthSkaterUUID))
    costPerf = float(addEventsP(AuthSkaterUUID))
    costTest = float(addEventsT(AuthSkaterUUID))
    costMemb = float(addClub(AuthSkaterUUID))
    costClass = float(addSchool(AuthSkaterUUID))
    costCamp = float(addCamp(AuthSkaterUUID))
    addCostsTotal = (float(costCoaching[0])+float(costIcetime[1])+float(costEquip)+float(costMaint[5])+costComp+costPerf+costTest+costMemb+costClass+costCamp)
    query = [round(float(costCoaching[0]), 2),round(float(costIcetime[1]), 2),round(float(costEquip), 2),round(float(costMaint[5]), 2),round(costComp, 2),round(costPerf, 2),round(costTest, 2),round(costMemb, 2),round(costClass, 2),round(costCamp, 2),round(addCostsTotal, 2)]
    return query
