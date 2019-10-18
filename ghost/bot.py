import pprint
import zulip
import sys
import re
import json
import httplib2
import os
import math
import threading
from topnews import getTopNews
from meet import grouping
from pnr import getpnr
from jobs import getjobs
from currency import fetch_currency_exchange_rate
from weather import get_weather
from joke import lame_jokes
from translate import translate_message
from hack import eventz

BOT_MAIL = "ghost-bot@zulipchat.com"

class Ghost(object):
    """
    We are Ghosts .. we are everywhere
    """

    def __init__(self):
        self.client = zulip.Client(config_file="~/.zuliprc")
        self.subscribe_all()

    def subscribe_all(self):
        json = self.client.get_streams()["streams"]
        streams = [{"name": stream["name"]} for stream in json]
        self.client.add_subscriptions(streams)
    
    def process(self, msg):
        content  = msg["content"].split()
        stream_name = msg["display_recipient"]
        
        
        if content[0].lower() == "@**ghost**":
            message = ""
            #print("yes")
            if content[1].lower() == "hello" or content[1].lower() == "hi":
                message = "Hola"
            elif content[1].lower() == "news":
                topic = content[2].lower()
                try:
                    news = getTopNews(topic)
                    for i in range(10):
                        message += "**"+news[i]['title']+"**"
                        message += '\n'
                        message += news[i]['desc']
                        message += '\n\n'
                except:
                    message = "No news as of now ... try something like football"

            elif content[1].lower() == "meetup":
                name = content[2:]
                #print(name)
                try:
                    dicti = grouping(name)
                    message += "**MeetUp Event Details" + '\n'
                    message += "Name: " + dicti["Name"] + '\n'
                    message += "Organizer: " + dicti["Organizer"] + '\n'
                    message += "City: " + dicti["City"] + '\n'
                    message += "Next Event: " + dicti["Upcoming Event"]["Event Name"] + '\n'
                    message += "RSVP: " + str(dicti["Upcoming Event"]["RSVP"]) + '\n'
                    message += "Time: " + dicti["Upcoming Event"]["Time"] + '\n'
                    message += "Link: " + dicti["Link"] + '\n'
                except:
                    message = "Try a valid group name :)"
                

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

            elif content[1].lower() == "joke":
                try:
                    message = lame_jokes()
                except:
                    message = "Not that lame though .. try something else"

            elif content[1].lower() == "weather":
                try:
                    if len(content) > 2 and content[2].lower() != "":
                        
                        weather = get_weather(content[2].lower())
                        if str(weather['cod']) != "404":
                            message += "**Weather status of {}**\n".format(content[2].lower())
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

            elif content[1].lower() == "contest":
                try:
                    message = eventz()
                except:
                    message = "Check connection"
            
            else:
                message += "Show news according to your choice : **Ghost news topic-name**\n"
                message += "Show MeetUp group details and next event status : **Ghost meetup group-name**\n"
                message += "Crack a joke ... even a lame one : **Ghost joke**\n"
                message += "Get the current currency conversion ratios : **Ghost currency currency-1 to currency-2** \nor **Ghost currency currency-1** \n"
                message += "Get a list of upcoming coding events: **Ghost contest**\n"
                message += "Get weather status of a location: **Ghost weather location\n"
                message += "Get a list of new job openings in your locality: **Ghost jobs**\n"
                message += "Translate a word or sentence to English: **Ghost translate word/sentence**\n"
                message += "Check your pnr status: **Ghost pnr pnr-number**\n"
                

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
        print("\nAdios fellas")
        sys.exit(0)