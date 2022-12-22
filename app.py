from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/name')
def name():
    return "I'm Pavel!"


@app.route('/last_name')
def last_name():
    return "Are you Erin?"


if __name__ == '__main__':
    app.run(debug=True)
