# Woolacombe 1352 | Porthcawl 1449   (swell)
# Woolacombe 0535 | Porthcawl 0512   (tide)

import time
import datetime
import atexit
import os
import subprocess

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
def moveLogs():
	subprocess.call(['./moveLogs.sh'])
	print("moved logs")

def getWaveData(s):
	wave_dict.clear()
	wave_dict.update(wave_api.getData(s))

def getTideData(t):
	tide_list.clear()
	tide_list.append(tide_api.getData(t))

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
	socketio.emit('returnTideData', tide_list, callback=messageReceived)

@socketio.on('waveData')
def waveData(methods=['GET', 'POST']):
	try:
		waveJSON = getWaveDataNow()
	except:
		dateNow = datetime.datetime.now()
		timeNow = datetime.datetime.now().replace(second=0,microsecond=0)
		fileName= "dictErrors/" + dateNow.strftime("%Y%m%d_%H%M%S")[:-2]+".txt"

		#Write relevant dict
		g	= open(fileName,"w+")
		g.write(waveDict)
		g.close()

		#Write Key Error
		errorString = "Key: {0} File: {1}".format(timeNow,dateNow)
		f = open("keyError.txt","a")		
		f.write(errorString)
		f.close()
		print(errorString)
		
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
		scheduler.add_job(getTideData,trigger="interval",args=["0512"],seconds=apiTime*4*12*60)
		scheduler.add_job(moveLogs,trigger="interval",seconds=24*60*60)
		scheduler.start() # start scheduler
		atexit.register(lambda: scheduler.shutdown()) # kill when exiting app

		# Sockets / Flask Run
		socketio.run(app, host = "0.0.0.0", port = 3500, debug = True) # 3500 desired port | 3000 react port

