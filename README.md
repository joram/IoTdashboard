# IOTdashboard
a generic dashboard for multiple IOT projects.
I'm running a copy here <http://iot.serenity.oram.ca> it's still under active development, so data may be deleted at any point.

## Setup
These instructions are based on my environment (Ubuntu 16.04)

###Install the python libraries:
This probably should be done in a virtual env.
```
pip install -r requirements.txt
```

###Create `settings.py`
It should contain the following variables set in it:
```
SECRET_KEY = "..."  # a random constant key for your server
GOOGLE_CLIENT_ID = "....apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "..."
```
Google Oauth credentials created at <https://console.developers.google.com/projectselector/apis/library>

*Note:* The authorized return uri should be to <your_domain>/google_authorized


### Run the server
Run
```
python ./server.py
```
then visit it at <http://localhost:5000>

## Project status:
 currently this is just draggable bootstrap panels.

## Todo's:
  - configurable panels
  - panel content types:
    - single line graph
    - video feed
    - multi-line graph
    - bar graph
  - rest API with API keys