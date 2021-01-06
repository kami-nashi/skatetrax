import lib.logic_main as st
import requests
import json


def userSend(userJSON):
    server_ip = 'http://127.0.0.1:5002/test'
    headers = {'Content-Type': 'application/json'}
    server_return = requests.post(server_ip,headers=headers,data=json.dumps(userJSON))
    return

def gatherNewUser():
    # uSkaterConfig Section
    uSkaterUUID = ''        # generate & secure first
    uSkaterFname = ''       # required
    uSkaterLname = ''       # required
    uSkaterUFSAid = ''      # default null
    uSkateComboIce = ''     # default to 1
    uSkateComboOff = ''     # default to 2
    uSkaterCity = ''        # required
    uSkaterState = ''       # required
    uSkaterMaintPref = ''   # defaults to 21
    uSkaterType = ''        # required; 1 = skater, 2=coach, 3=student, 4=parent
    activeCoach = ''        # default 0
    # '1', 'Ashley', 'Young', '1670965', '3', '2', 'Fayetteville', 'NC', '21', '1', '3'

    # uSkateConfig Section (PIC & Figure)
    uSkaterUUID = ''        # use secured UUID from uSkaterConfig
    uSkaterBladesID = ''    # required, default to 1
    uSkaterBootsID  = ''    # required, default to 1
    sType = ''              # required, default to 1
    sActive = ''            # required, default to 1
    aSkateConfigID = ''     # ID of config, default 1
    # '1', '1', '1', '1', '0', '1'
    uSkaterUUID = ''        # use secured UUID from uSkaterConfig
    uSkaterBladesID = ''    # required, default to 2
    uSkaterBootsID  = ''    # required, default to 2
    sType = ''              # required, default to 2
    sActive = ''            # required, default to 1
    aSkateConfigID = ''     # ID of config, default 2

    # uSkaterBoots Section (PIC & Figure)
    bootsName = ''          # default to generic
    bootsModel = ''         # default to generic
    bootsSize = ''          # default to 0
    bootsPurchDate = ''     # default to 0000-00-00
    bootsPurchAmount = ''   # default to 0.00
    uSkaterUUID = ''        # use secured UUID from uSkaterConfig
    bootID = ''             # default 1
    #Riedell', 'Diamond 133', '12 Wide', '2015-11-27', '236.00', '1', '1'
    bootsName = ''          # default to generic
    bootsModel = ''         # default to generic
    bootsSize = ''          # default to 0
    bootsPurchDate = ''     # default to 0000-00-00
    bootsPurchAmount = ''   # default to 0.00
    uSkaterUUID = ''        # use secured UUID from uSkaterConfig
    bootID = ''             # default 2

    # uSkaterBlades Section (PIC & Figure)
    BladesName = ''         # default to generic
    BladesModel = ''        # default to generic
    BladesSize = ''         # default to 0
    BladesPurchDate = ''    # default to 0000-00-00
    BladesPurchAmount = ''  # default to 0.00
    uSkaterUUID = ''        # use secured UUID from uSkaterConfig
    bladeID = ''            # default 1
    #Riedell', 'Diamond 133', '12 Wide', '2015-11-27', '236.00', '1', '1'
    BladesName = ''         # default to generic
    BladesModel = ''        # default to generic
    BladesSize = ''         # default to 0
    BladesPurchDate = ''    # default to 0000-00-00
    BladesPurchAmount = ''  # default to 0.00
    uSkaterUUID = ''        # use secured UUID from uSkaterConfig
    bladeID = ''            # default 2

    # aUserInfo Section
    uSkaterUUID = ''        # use secured UUID from uSkaterConfig
    uLoginID = ''           #
    uHash = ''              #
    # '1', 'sparkles', 'password1'


    return

def createNewUser():
    dbp_newUser = dbinsert()

    return
