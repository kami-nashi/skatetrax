import urllib.request, json

def getSkateMaster(uSkaterUUID):
    with urllib.request.urlopen("http://0.0.0.0:5021/api/v1/resources/skates/master/" + str(uSkaterUUID) ) as url:
        data = json.loads(url.read().decode())
    return data

def getSkateActive(uSkaterUUID):
    with urllib.request.urlopen("http://0.0.0.0:5021/api/v1/resources/skates/active/" + str(uSkaterUUID) ) as url:
        data = json.loads(url.read().decode())
    return data

def getSkateList(uSkaterUUID):
    with urllib.request.urlopen("http://0.0.0.0:5021/api/v1/resources/skates/list/" + str(uSkaterUUID) ) as url:
        data = json.loads(url.read().decode())
    return data

def getBootsList(uSkaterUUID):
    with urllib.request.urlopen("http://0.0.0.0:5021/api/v1/resources/skates/listBoots/" + str(uSkaterUUID) ) as url:
        data = json.loads(url.read().decode())
    return data

def getBladesList(uSkaterUUID):
    with urllib.request.urlopen("http://0.0.0.0:5021/api/v1/resources/skates/listBlades/" + str(uSkaterUUID) ) as url:
        data = json.loads(url.read().decode())
    return data
