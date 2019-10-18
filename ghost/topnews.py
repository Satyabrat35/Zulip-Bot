import requests

class Item:
    def __init__(self,title,des):
        self.title = title
        self.des = des

class News():
    def getTopNews(self):
        news = []
        results = requests.get('https://newsapi.org/v2/everything?q=football&from=2019-10-16&sortBy=publishedAt&apiKey=49e6ddb018f8482ca8a1720084ab49f5')
        data = results.json()
        for i in range(10):
            #print(data["articles"][i]["title"])
            news.append(Item(data["articles"][i]["title"],data["articles"][i]["description"]))
        return news
            
if __name__ == "__main__":
    n = News()
    r = n.getTopNews()
    print(r)