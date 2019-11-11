# Woolacombe 1352 | Porthcawl 1449

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, redirect, url_for, request
from flask import render_template

api = __import__("api-accessor")


app = Flask(__name__)
scheduler = BackgroundScheduler() # initialise scheduler
scheduler.start() # start scheduler
atexit.register(lambda: scheduler.shutdown()) # kill when exiting app

# EXAMPLE SCHEDULER TASK
# def print_date_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#
# scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
# print(api.main(1352))

### Globals



@app.route('/')
def hello_world():
    message = "hello world"
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 3500, debug = True)
