import urllib.request, json

def getSkateMaster(uSkaterUUID):
    with urllib.request.urlopen("http://0.0.0.0:5021/api/v1/resources/skates/master/" + str(uSkaterUUID) ) as url:
        data = json.loads(url.read().decode())
    return data
