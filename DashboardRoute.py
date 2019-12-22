from flask import Flask, request, render_template, session, after_this_request
import requests
from SmartMirror import fetchWeatherInfo, fetchTime, fetchQod, fetchNewsArticles, fetchDailyAgenda
import logging


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#Renders the dashboard home screen
@app.route("/")
def loadPage():
    return render_template('dashboard.html')

@app.route("/getQuote", methods=['GET','POST'])
def getQuote():
    logging.info('Fetching Quote of the Day')
    quote = fetchQod()
    print(quote)
    logging.info('Finished Fetching Quote of the Day')
    return render_template('dashboard.html', quote=quote)

#Gets zipcode or city name from dashboard, completes an API call to return the temperature in farenheit
@app.route("/getWeather", methods=['POST'])
def getWeather():
    logging.info('Fetching Weather Information')
    zipcode = request.form['cityForm']
    zipcode1 = request.form['zipcode1']
    zipcode2 = request.form['zipcode2']
    zipcode3 = request.form['zipcode3']
    units = request.form['unit']
    print(zipcode1)
    print(zipcode2)
    print(zipcode3)
    session["zipcode"]=zipcode1
    print(units)
    weatherInfo = fetchWeatherInfo(zipcode, units)
    weatherInfo1 = fetchWeatherInfo(zipcode1, units)
    weatherInfo2 = fetchWeatherInfo(zipcode2, units)
    weatherInfo3 = fetchWeatherInfo(zipcode3, units)
    '''
    params = {
         'access_key': '7b9dcfb1b6e3293fcbcefb9012e0e5fa',
         'query': city,
         'units': 'f'
    }
    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    api_response = (api_response["current"])
    api_response = (api_response["temperature"])
    api_response = (str(api_response))
    '''
    #print(api_response)
    if "None" or "C" in str(weatherInfo1):
        weatherInfo1 = str(weatherInfo1).replace("None","")
        weatherInfo1 = str(weatherInfo1).replace("C","")
    else:
        print("all good")
    if "None" or "C" in str(weatherInfo2):
        weatherInfo2 = str(weatherInfo2).replace("None","")
        weatherInfo2 = str(weatherInfo2).replace("C","")
    else:
        print("all good")
    if "None" or "C" in str(weatherInfo2):
        weatherInfo3 = str(weatherInfo3).replace("None","")
        weatherInfo3 = str(weatherInfo3).replace("C","")
    else:
        print("all good")
    session["weatherInfo"] = weatherInfo
    session["weatherInfo1"]=weatherInfo1
    session["weatherInfo2"]=weatherInfo2
    session["weatherInfo3"]=weatherInfo3

    logging.info('Finished Fetching Weather Information')
    return render_template('dashboard.html')

@app.route("/getTimezone", methods=['GET','POST'])
def getTimezone():
    logging.info('Fetching Time Zone')
    timezone1 = request.form['timezone1']
    timezone2 = request.form['timezone2']
    timezone3 = request.form['timezone3']
    timezone4 = request.form['timezone4']
    if "None" or "nothing" in str(timezone1):
        timezone1 = str(timezone1).replace("None","")
        timezone1 = str(timezone1).replace("nothing","")
    else:
        print("all good")
    if "None" or "nothing" in str(timezone2):
        timezone2 = str(timezone2).replace("None","")
        timezone2 = str(timezone2).replace("nothing","")
    else:
        print("all good")
    if "None" or "nothing" in str(timezone3):
        timezone3 = str(timezone3).replace("None","")
        timezone3 = str(timezone3).replace("nothing","")
    else:
        print("all good")
    if "None" or "nothing" in str(timezone4):
        timezone4 = str(timezone4).replace("None","")
        timezone4 = str(timezone4).replace("nothing","")
    else:
        print("all good")
    print(timezone1)
    print(timezone2)
    print(timezone3)
    print(timezone4)
    timezone1 = fetchTime(timezone1)
    timezone2 = fetchTime(timezone2)
    timezone3 = fetchTime(timezone3)
    timezone4 = fetchTime(timezone4)
    session["timezone1"]=timezone1
    session["timezone2"]=timezone2
    session["timezone3"]=timezone3
    session["timezone4"]=timezone4
    logging.info('Finished Fetching Time Zone')
    return render_template('dashboard.html')

@app.route('/getNewsCategory', methods=['POST'])
def getNewsCategory():
    logging.info('Fetching News Article')
    category = request.form['category']
    print(category)
    session["category"]=category
    logging.info('Finished Fetching News Article')
    return render_template('dashboard.html')

@app.route('/editMirror', methods=['GET','POST'])
def editMirror():
    category=session.get("category",None)
    news = fetchNewsArticles(category)
    weatherInfo=session.get("weatherInfo")
    timezone=session.get("timezone",None)
    calendar = session.get("calendar")
    quote = fetchQod()
    return render_template('editmirror.html', weatherInfo=weatherInfo, news=news, timezone=timezone, quote=quote, calendar=calendar)

@app.route('/mirrorPage', methods=['GET', 'POST'])
def mirrorPage():
    category=session.get("category",None)
    news = fetchNewsArticles(category)
    weatherInfo = session.get("weatherInfo")
    weatherInfo1=session.get("weatherInfo1")
    weatherInfo2=session.get("weatherInfo2")
    weatherInfo3=session.get("weatherInfo3")
    timezone1=session.get("timezone1",None)
    timezone2=session.get("timezone2",None)
    timezone3=session.get("timezone3",None)
    timezone4=session.get("timezone4",None)
    logging.info('Fetching Mirror Info')
    quote = fetchQod()
    calendar = session.get("calendar")
    logging.info('Finished Fetching Mirror Info')
    return render_template('MirrorUI.html', weatherInfo = weatherInfo, weatherInfo1=weatherInfo1, weatherInfo2=weatherInfo2, weatherInfo3=weatherInfo3, news=news,quote=quote, timezone1=timezone1, timezone2=timezone2, timezone3=timezone3, timezone4=timezone4, calendar=calendar)

@app.route('/googleCalendar', methods=['GET','POST'])
def googleCalendar():
    #fetchDailyAgenda()
    calendar = fetchDailyAgenda()
    print(calendar)
    session["calendar"]=calendar
    return render_template('dashboard.html')


def openFile():
    file = open('mirror.log', 'w')
    logging.basicConfig(filename='mirror.log', filemode='w')
    logging.info('Application Startup')
    return file

def closeFile(file):
    logging.info('Application Termination')
    file.close()

if __name__ == '__main__':
    file = openFile()
    app.run(debug = True)
    closeFile(file)
