from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime
from sqlalchemy import func
from login import LoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///costs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_secret_key'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_user = db.Column(db.Date, nullable=False)
    date_add = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Article {self.id} - {self.category} - {self.price}'


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    cash_receipts = db.Column(db.Integer, nullable=False)
    date_user = db.Column(db.Date, nullable=False)
    date_add = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Income {self.id} - {self.category} - {self.price}'


with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/index')
@app.route('/', methods=['POST', 'GET'])
def index():
    info = Article.query.order_by(Article.date_user.desc()).limit(10).all()  # db.session.query(Article).all()
    total_price = db.session.query(func.sum(Article.price)).all()
    price_of_day = round((total_price[0][0] / ((datetime.now() - datetime(2023, 1, 1)).days + 1)), 2)

    info_add = Income.query.order_by(Income.date_user.desc()).limit(10).all()
    total_price_add = db.session.query(func.sum(Income.cash_receipts)).all()
    price_of_day_add = round((total_price_add[0][0] / ((datetime.now() - datetime(2023, 1, 1)).days + 1)), 2)

    if request.method == 'POST':
        category = request.form['category_filter']
        filter_category = db.session.query(Article).filter(Article.category == category).all()
        return render_template('index.html', title='Главная страница',
                               info_all=info,
                               info_add=info_add,
                               total_price=total_price[0][0],
                               total_price_add=total_price_add[0][0],
                               price_of_day=price_of_day,
                               price_of_day_add=price_of_day_add,
                               date_str=datetime(2023, 1, 1),
                               date_fin=datetime.now(),
                               filter_category=filter_category,
                               category=category
                               )

    return render_template('index.html', title='Главная страница',
                           info_all=info,
                           info_add=info_add,
                           total_price=total_price[0][0],
                           total_price_add=total_price_add[0][0],
                           price_of_day=price_of_day,
                           price_of_day_add=price_of_day_add,
                           date_str=datetime(2023, 1, 1),
                           date_fin=datetime.now()
                           )


@app.route('/index/<int:id>')
def index_detail(id):
    info_id = Article.query.get(id)
    return render_template('index-detail.html', title=f'{info_id.category} - {info_id.date_user}', info_id=info_id)


@app.route('/all_table')
def all_table():
    all_info = Article.query.order_by(Article.date_user.desc()).all()
    return render_template('all_table.html', title='Вся база', all_info=all_info)


@app.route('/article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        category = request.form['category']
        value = request.form['value']
        price = request.form['price']
        date = request.form['date'].replace('-', '.')
        if date == '':
            date_user = datetime.utcnow()
        else:
            date_user = datetime.strptime(date, '%Y.%m.%d')
        article = Article(category=category, value=value, price=price, date_user=date_user)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            print("Всё пропало!!!")
            return redirect(url_for('index'))
    else:
        return render_template('article.html', title='Добавить расходы')


@app.route('/add_article', methods=['POST', 'GET'])
def add_article():
    if request.method == 'POST':
        category = request.form['category']
        value = request.form['value']
        cash_receipts = request.form['cash_receipts']
        date = request.form['date'].replace('-', '.')
        if date == '':
            date_user = datetime.utcnow()
        else:
            date_user = datetime.strptime(date, '%Y.%m.%d')
        income = Income(category=category, value=value, cash_receipts=cash_receipts, date_user=date_user)
        try:
            db.session.add(income)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            print("Всё пропало!!!")
            return redirect(url_for('index'))
    else:
        return render_template('add_article.html', title='Добавить')


@app.route('/list')
def list_cnl():
    return render_template('list_control.html', title='Список')



# if __name__ == '__main__':
#     app.run(debug=True)
