'''
Name: Nick Lai
Chapman email: lai137@mail.chapman.edu
Project: Smart Mirror
'''

## Google Calendar Imports ##
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os
import requests
import json
import datetime
import pytz
import logging

from newsapi import NewsApiClient

# Uses OpenWeatherMap API to fetch the weather based on zip code
def fetchWeatherInfo(zipCode, units):
    if zipCode == '':
        return None
    if units == 'f':
        weatherAPI_address = requests.get('http://api.openweathermap.org/data/2.5/weather?appid=bdd02b13f194675453653540b59bf1c9&zip=' + str(zipCode) + '&units=imperial').json()
    elif units == 'c':
        weatherAPI_address = requests.get('http://api.openweathermap.org/data/2.5/weather?appid=bdd02b13f194675453653540b59bf1c9&zip=' + str(zipCode) + '&units=metric').json()
    #if typed incorrectly or left blank, use default of Kelvin
    else:
        weatherAPI_address = requests.get('http://api.openweathermap.org/data/2.5/weather?appid=bdd02b13f194675453653540b59bf1c9&zip=' + str(zipCode)).json()
    weatherData = weatherAPI_address
    description = weatherData['weather'][0]['description']
    city = weatherData['name']
    country = weatherData['sys']['country']
    temperature = weatherData['main']['temp']
    formattedtemperature = ('City: ' + city + '<br>' + 'Country: ' + country + '<br>' + 'Temp: ' + str(temperature) + '<br>' + description + '<br><br>')

    return formattedtemperature

# Fetches the time for a given time zone and prints it out.
# A list of time zone codes can be found here: https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
def fetchTime(timeZone):
    if timeZone == '':
        return None
    strTimezone = timeZone
    timeZone = pytz.timezone(timeZone)
    selectedTZ_time = datetime.datetime.now(timeZone)
    format = '%m-%d-%Y <br> %H:%M:%S'
    return(strTimezone + '<br>' + selectedTZ_time.strftime(format)+ '<br><br>')



def fetchQod():
    api_result = requests.get('https://quotes.rest/qod')
    api_response = api_result.json()
    api_response = (api_response["contents"])
    api_response = (api_response["quotes"])
    quote = (api_response[0])
    author = (quote["author"])
    quote = (quote["quote"])
    fullQuote = (quote + '\n' + " - " + author)
    return fullQuote

# Uses https://newsapi.org/ API to fetch top 3 headlines by category
# Available categories: business, entertainment, health, science, sports, technology
def fetchNewsArticles(newsCategory):
    newsAPI_key = '641010ffdac14c46968d4a12b1a396cb'
    newsAPI_address = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=' + newsCategory + '&apiKey=' + newsAPI_key).json()
    newsData = newsAPI_address
    article1 = newsData['articles'][0]['title']
    article2 = newsData['articles'][1]['title']
    article3 = newsData['articles'][2]['title']
    formattedarticles = (article1 + '<br><br>' + article2 + '<br><br>' + article3)
    return formattedarticles

# Integrates Google Calendar API to fetch the user's agenda for the day
def fetchDailyAgenda():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    calendarAPI_key = 'AIzaSyCgzVpwa1hF-BlBJYZ2EEfK8eD4S-A1Gc0'
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return ('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        formattedevent = str(start + '<br>' + event['summary'])
        return(formattedevent)


# Console input to test above functions
'''
zipCode = int(input("Enter your zip code: "))
units = input("Enter 'f' or 'c': ")
fetchWeatherInfo(zipCode, units)
timeZone = input("Enter the time zone you wish to view: ")
fetchTime(timeZone)
fetchNewsArticles('business')
fetchDailyAgenda()
'''
