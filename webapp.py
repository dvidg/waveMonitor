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

api = __import__("api-accessor")


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

### Globals
data_dict = {}
apiTime = 15

### Functions
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
									'favicon.ico',mimetype='image/vnd.microsoft.icon')

def getApiData(id):
	data_dict.clear()
	data_dict.update(api.main(id))
	print("updated data dict")

@socketio.on('getData')
def getData(methods=['GET', 'POST']):
	try:
		json = data_dict[int(time.time())]
	except:
		f= open("keyError.txt","a")
		f.write("%s %s\n\n" % int(time.time()), int(datetime.datetime.now()))
		f.close()
		print("key error")
	
	socketio.emit('returnData', json, callback=messageReceived)

@app.route('/')
def homepage():
    message = "hello world"
    return render_template('index.html', message=message)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


### Receiving WebSocket Messages ###
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
		print("user connected")
		socketio.emit('my response', "test", callback=messageReceived)

if __name__ == '__main__':
		getApiData(1449)
		scheduler = BackgroundScheduler() # initialise scheduler
		#scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
		scheduler.add_job(getApiData,trigger="interval",args=[1352],seconds=apiTime*60)
		#scheduler.add_job(getData,trigger="interval",seconds=1)
		scheduler.start() # start scheduler
		atexit.register(lambda: scheduler.shutdown()) # kill when exiting app
		socketio.run(app, host = "0.0.0.0", port = 3000, debug = True)	
		# 3500 desired port | 3000 react port

