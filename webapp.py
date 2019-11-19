# Woolacombe 1352 | Porthcawl 1449   (swell)
# Woolacombe 0535 | Porthcawl 0512   (tide)

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
wave_api = __import__("msw-api")
tide_api = __import__("tide-api")


### Flask Definitions
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

### Globals
wave_dict = {}
tide_list = []
apiTime = 15

### Functions
def getWaveData(s):
	wave_dict.clear()
	wave_dict.update(wave_api.getData(s))

def getTideData(t):
	tide_list = tide_api.getData(t)
	return tide_list

def getWaveDataNow():
	return wave_dict[int(time.time())]

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

### Sockets
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
									'favicon.ico',mimetype='image/vnd.microsoft.icon')

@socketio.on('tideData')
def tideData(methods=['GET', 'POST']):
	tideJSON = getTideData()
	socketio.emit('returnTideData', tideJSON, callback=messageReceived)

@socketio.on('waveData')
def waveData(methods=['GET', 'POST']):
	try:
		waveJSON = getWaveDataNow()
	except:
		f= open("keyError.txt","a")
		f.write("%s %s\n\n" % int(time.time()),datetime.datetime.now())
		f.close()
		print("key error %s %s" % int(time.time()),datetime.datetime.now())
	socketio.emit('returnWaveData', waveJSON, callback=messageReceived)

@app.route('/')	# initial connection
def homepage():
    message = "hello world"
    return render_template('index.html', message=message)


### Receiving WebSocket Messages ###
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
		print("user connected")
		socketio.emit('my response', "test", callback=messageReceived)


### Main
if __name__ == '__main__':
		getWaveData("1449")
		getTideData("0512")

		# Scheduler
		scheduler = BackgroundScheduler() # initialise scheduler
		scheduler.add_job(getWaveData,trigger="interval",args=["1449"],seconds=apiTime*60)
		scheduler.add_job(getWaveData,trigger="interval",args=["1352"],seconds=apiTime*60+1)
		scheduler.add_job(getTideData,trigger="interval",args=["0512"],seconds=apiTime*4*12*60)
		scheduler.add_job(getTideData,trigger="interval",args=["0535"],seconds=apiTime*4*12*60+1)
		scheduler.start() # start scheduler
		atexit.register(lambda: scheduler.shutdown()) # kill when exiting app

		# Sockets / Flask Run
		socketio.run(app, host = "0.0.0.0", port = 3000, debug = True) # 3500 desired port | 3000 react port

