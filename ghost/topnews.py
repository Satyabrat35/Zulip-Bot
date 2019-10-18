import requests
api_key = '49e6ddb018f8482ca8a1720084ab49f5'

def getTopNews(topic):
    news = {}
    url = "https://newsapi.org/v2/everything?q={}&from=2019-10-16&sortBy=publishedAt&apiKey={}".format(topic,api_key)
    results = requests.get(url)
    data = results.json()
    j=0
    for i in range(10):
        #print(data["articles"][i]["title"])
        dct = {'title': data["articles"][j]["title"], 'desc':data["articles"][i]["description"]}
        news[i] = dct
        j+=1
        
    return news
            
