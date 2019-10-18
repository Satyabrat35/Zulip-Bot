import requests
username = 'erik35'
api_key = 'f35aba3b32a905deb2555b545c8220c17b235ea9'

def eventz():
    url = "https://clist.by/api/v1/contest/?username={}&api_key={}".format(username,api_key)
    req = requests.get(url)
    if req.status_code == 200:
        lst = req.json()
        message = ""
        for i in range(77,88):
            message += "**Event: **" + lst['objects'][i]['event'] + '\n' + "**Link: **" + lst['objects'][i]['href'] + '\n\n'

        return message
    else:
        message = "Check connections"
        return message    