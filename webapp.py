# Woolacombe 1352 | Porthcawl 1449

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from flask import Flask, redirect, url_for, request
from flask import render_template
from flask_socketio import SocketIO

api = __import__("api-accessor")


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

### Globals
data_dict = {}
apiTime = 15

### Functions
def getApiData(id):
	data_dict.clear()
	data_dict.update(api.main(id))

def pushData():
	#print(data_dict[int(time.time())])
	try:
		socketio.emit('waveData', "here2", callback=messageReceived)
	except:
		print("server starting")

def listener(event):
	if event.exception:
		print("failed to get data")

@app.route('/')
def homepage():
    message = "hello world"
    return render_template('index.html', message=message)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

### Receiving WebSocket Messages ###
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    getApiData(1352)
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
		getApiData(1352)
		scheduler = BackgroundScheduler() # initialise scheduler
		scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
		scheduler.add_job(getApiData,trigger="interval",args=[1352],seconds=apiTime*60*60)
		scheduler.add_job(pushData,trigger="interval",seconds=1)
		scheduler.start() # start scheduler
		atexit.register(lambda: scheduler.shutdown()) # kill when exiting app
		socketio.run(app, host = "0.0.0.0", port = 3000, debug = True)	
		# 3500 desired port | 3000 react port

