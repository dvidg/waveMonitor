from flask import Flask, redirect, url_for, request
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    message = "hello world"
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 3500, debug = True)
