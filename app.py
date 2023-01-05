from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///costs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_secret_key'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)


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


class LoginForm(FlaskForm):
    username = StringField('Username',
                           description='Логин от 6 до 30 символов',
                           validators=[DataRequired(message='Эта строка не должна быть пустой.'),
                                       Length(min=6, max=30, message="Логин должен быть от 6 до 30 символов.")
                                       ]
                           )
    password = PasswordField('Password',
                             validators=[DataRequired(message='Эта строка не должна быть пустой.'),
                                         Length(min=6, max=30, message="Пароль должен быть от 6 до 30 символов.")
                                         ]
                             )
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/index')
@app.route('/')
def index():
    info = db.session.query(Article).all()
    return render_template('index.html', title='Главная страница', info_all=info)


@app.route('/index/<int:id>')
def index_detail(id):
    info_id = Article.query.get(id)
    return render_template('index-detail.html', title=f'{info_id.category} - {info_id.date_user}', info_id=info_id)


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


@app.route('/name', methods=['GET', 'POST'])
def name():
    return "I'm Pavel!"


@app.route('/last_name/<string:name>/<int:id>')
def last_name(name, id):
    return f"Are you {name}, number - {id}?"

# if __name__ == '__main__':
#     app.run(debug=True)
