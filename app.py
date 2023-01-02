from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///costs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_user = db.Column(db.Date, nullable=False)
    date_add = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Article {self.id}'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    info = db.session.query(Article).all()
    return render_template('index.html', info_all=info)


@app.route('/index/<int:id>')
def index_detail(id):
    info_id = Article.query.get(id)
    return render_template('index-detail.html', info_id=info_id)


@app.route('/article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        category = request.form['category']
        value = request.form['value']
        price = request.form['price']
        date = request.form['date'].replace('-', '.')
        print(f'Here = {date}')
        if date == '':
            date_user = datetime.utcnow()
        else:
            date_user = datetime.strptime(date, '%Y.%m.%d')
        article = Article(category=category, value=value, price=price, date_user=date_user)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            db.session.rollback()
            print("Всё пропало!!!")
            return redirect('/')
    else:
        return render_template('article.html')


@app.route('/name', methods=['GET', 'POST'])
def name():
    return "I'm Pavel!"


@app.route('/last_name/<string:name>/<int:id>')
def last_name(name, id):
    return f"Are you {name}, number - {id}?"

# if __name__ == '__main__':
#     app.run(debug=True)
