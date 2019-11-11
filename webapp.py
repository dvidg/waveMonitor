# Woolacombe 1352 | Porthcawl 1449

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from flask import Flask, redirect, url_for, request
from flask import render_template

api = __import__("api-accessor")


app = Flask(__name__)


### Globals
data_dict = {}
apiTime = 15

### Functions
def getApiData(id):
	print("getting data")
	data_dict.update(api.main(id))

def listener(event):
	if not event.exception:
		print("successfully got data")
		print(len(data_dict.keys()))

@app.route('/')
def hello_world():
    message = "hello world"
    return render_template('index.html', message=message)

if __name__ == '__main__':
		scheduler = BackgroundScheduler() # initialise scheduler
		scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
		scheduler.add_job(func=getApiData,trigger="interval",args=[1352],seconds=apiTime*60*60)
		scheduler.start() # start scheduler
		atexit.register(lambda: scheduler.shutdown()) # kill when exiting app
		app.run(host = "0.0.0.0", port = 3500, debug = True)	

		print("successfully started server")
		for job in cron.get_jobs():
			job.modify(next_run_time=datetime.now())


