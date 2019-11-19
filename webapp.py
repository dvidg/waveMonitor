# Woolacombe 1352 | Porthcawl 1449

import time
import datetime
import atexit
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from flask import Flask, redirect, url_for, request
from flask import render_template
from flask_socketio import SocketIO
from flask import send_from_directory


### Imported Files
msw_api  = __import__("msw-api")
tide_api = __import__("tide-api")


### Flask Definitions
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

### Globals
msw_dict  = {}
tide_dict = {}
apiTime = 15
w = ["1352", "0535"] # Woolacombe
p = ["1449", "0512"] # Porthcawl

### Functions
def getSwellData(s):
	msw_dict.clear()
	msw_dict = msw_api.getData(t)

def getTideData(t):
	tide_dict.clear()
	tide_dict = tide_api.getData(s)

def getSwellDataNow()
	return msw_dict[int(time.time())]

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

### Sockets
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
									'favicon.ico',mimetype='image/vnd.microsoft.icon')

@socketio.on('tideData')
def swellData(methods=['GET', 'POST']):
	tideJSON = getSwellDataNow()
	socketio.emit('returnTideData', tideJSON, callback=messageReceived)

@socketio.on('swellData')
def swellData(methods=['GET', 'POST']):
	try:
		swellJSON = getSwellDataNow()
	except:
		f= open("keyError.txt","a")
		f.write("%s %s\n\n" % int(time.time()),datetime.datetime.now())
		f.close()
		print("key error %s %s" % int(time.time()),datetime.datetime.now())
	
	socketio.emit('returnSwellData', swellJSON, callback=messageReceived)

@app.route('/')
def homepage():
    message = "hello world"
    return render_template('index.html', message=message)


### Receiving WebSocket Messages ###
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
		print("user connected")
		socketio.emit('my response', "test", callback=messageReceived)

if __name__ == '__main__':
		getInitialData(p)
		getInitialData(w)		


		scheduler = BackgroundScheduler() # initialise scheduler
		#scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
		scheduler.add_job(getApiData,trigger="interval",args=[p[0], msw_dict, msw_api],seconds=apiTime*60)
		#scheduler.add_job(getData,trigger="interval",seconds=1)
		scheduler.start() # start scheduler
		atexit.register(lambda: scheduler.shutdown()) # kill when exiting app
		socketio.run(app, host = "0.0.0.0", port = 3000, debug = True)	
		# 3500 desired port | 3000 react port

