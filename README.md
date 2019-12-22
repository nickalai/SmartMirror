# SE-330 Fall2019: Smart Mirror
Created by: Nick, Nikolai, Bryce, John, Omar  
## PIP Installs Required:
Preface the following packages with "pip install":
```
requests

pytz

newsapi-python

--upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## APIs Used:
[OpenWeatherMap](https://openweathermap.org/)

[Quotes.rest](quotes.rest/qod)

[NewsApi](https://newsapi.org/)

[Google Calendar](https://developers.google.com/calendar)

## Flask Setup
To setup development server locally:

```
cd se330Fall2019-SmartMirror
export FLASK_APP=DashboardRoute.py
export FLASK_DEBUG=1
```

To run:

```
flask run
```
