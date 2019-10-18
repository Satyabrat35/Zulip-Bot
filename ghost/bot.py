import pprint
import zulip
import sys
import re
import json
import httplib2
import os
import math
import threading
from topnews import News
from meet import grouping
from pnr import getpnr
from jobs import getjobs
from currency import fetch_currency_exchange_rate
from weather import get_weather
from translate import translate_message

BOT_MAIL = "ghost-bot@zulipchat.com"

class Ghost(object):
    """
    We are Ghosts .. we are everywhere
    """

    def __init__(self):
        self.client = zulip.Client(config_file="~/.zuliprc")
        self.subscribe_all()
        self.news = News()

    def subscribe_all(self):
        json = self.client.get_streams()["streams"]
        streams = [{"name": stream["name"]} for stream in json]
        self.client.add_subscriptions(streams)
    
    def process(self, msg):
        message_id = msg["id"]
        content  = msg["content"].split()
        sender_email = msg["sender_email"]
        
        stream_name = msg["display_recipient"]
        
        #print(content)
        #print(content[0],content[1])
        #if sender_email == BOT_MAIL:
        #    return
        if content[0].lower() == "@**ghost**":
            message = ""
            #print("yes")
            if content[1].lower() == "hello" or content[1].lower() == "hi":
                message = "Hola"
            elif content[1].lower() == "news":
                try:
                    news = self.news.getTopNews()
                    for item in news:
                        message += "**"+item.title+"**"
                        message += '\n'
                        message += item.des
                        message += '\n\n'
                except:
                    message = "No news as of now ... try something like football"
            elif content[1].lower() == "meetup":
                name = ""
                for i in range(2,len(content)-1):
                    name += content[i]
                    name += " "
                name += content[len(content)-1]
                #print(name)
                
                dicti = grouping(name)
                message += "Name: " + dicti["Name"] + '\n'
                message += "Organizer: " + dicti["Organizer"] + '\n'
                message += "City: " + dicti["City"] + '\n'
                message += "Next Event: " + dicti["Upcoming Event"]["Event Name"] + '\n'
                message += "RSVP: " + str(dicti["Upcoming Event"]["RSVP"]) + '\n'
                message += "Time: " + dicti["Upcoming Event"]["Time"] + '\n'
                message += "Link: " + dicti["Link"] + '\n'

            elif content[1].lower() == "pnr":
                num = int(content[2])
                try:
                    message = getpnr(num)
                except:
                    message = "Connection Error"
            
            elif content[1].lower() == "translate":
                try:
                    message = content[2:]
                    message = " ".join(message)
                    
                    message = translate_message(message)
                except:
                    message = "Error in format"

            elif content[1].lower() == "jobs":
                try:
                    message = getjobs()
                except:
                    message = "Connection Error"

            elif content[1].lower() == "currency":
                if len(content) == 3 and content[2].lower() != "":
                   
                    currency = fetch_currency_exchange_rate("", content[2].upper())
                    message += "**Showing all currency conversions for 1 {}:**\n".format(content[2].upper())
                    for curr in currency['rates']:
                        message += "1 {} = ".format(content[2].upper()) + "{}".format(format(currency['rates'][curr], '.2f')) + " {}\n".format(curr)
                    message += "Last Updated: *{}*".format(currency['date'])
                elif len(content) == 5 and content[2].lower() != "" and content[4].lower() != "":
                   
                    currency = fetch_currency_exchange_rate(content[2].upper(), content[4].upper())
                    message += "1 {} = ".format(content[4].upper()) + "{}".format(format(currency['rates'][content[2].upper()], '.2f')) + " {}\n".format(content[4].upper())
                    message += "Last Updated: *{}*".format(currency['date'])
                else:
                    message = "Please ask the query in correct format."
            
            elif content[1].lower() == "weather":
                try:
                    if len(content) > 2 and content[2].lower() != "":
                        
                        weather = get_weather(content[2].lower())
                        if str(weather['cod']) != "404":
                            message += "**Weather report for {}**\n".format(content[2].lower())
                            message += "Climate: **{}**\n".format(str(weather['weather'][0]['description']))
                            message += "Temperature: **{}**\n".format(str(weather['main']['temp']) + "° C")
                            message += "Pressure: **{}**\n".format(str(weather['main']['pressure']) + " hPa")
                            message += "Humidity: **{}**\n".format(str(weather['main']['humidity']) + "%")
                            message += "Wind Speed: **{}**".format(str(weather['wind']['speed']) + " $$m/s^2$$")
                        else:
                            message = "City not found!\nabc"
                    else:
                        message = "Please add a location name."
                except:
                    message = "Something went wrong"
                
            else:
                message += "Show top 10 news : **Ghost news**\n"
                message += "Show MeetUp group details and next event status"

            self.client.send_message({
                "type": "stream",
                "to": stream_name,
                "subject": msg["subject"],
                "content": message
            })

def main():
    gh = Ghost()
    gh.client.call_on_each_message(gh.process)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Adios fellas")
        sys.exit(0)