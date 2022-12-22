from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Article %r' % self.id


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/name', methods=['GET', 'POST'])
def name():
    return "I'm Pavel!"


@app.route('/last_name/<string:name>/<int:id>')
def last_name(name, id):
    return f"Are you {name}, number - {id}?"


if __name__ == '__main__':
    app.run(debug=True)
