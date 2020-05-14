from app import db
from flask import request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField, FloatField, BooleanField
from wtforms.fields.html5 import DateTimeLocalField, DecimalField, IntegerField, widgets, SearchField
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange,Email
from flask_babel import _, lazy_gettext as _l
import datetime

from app.models import User, FoodDatatable
from decimal import ROUND_HALF_UP, ROUND_FLOOR

#import cgi               #new

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    weight = IntegerField(_l('Вес'))
    kkal = DecimalField(label='Базовая потребность в ККал',widget=widgets.NumberInput(max=1500, min=50, step=1), validators=[DataRequired()])
    mol =  DecimalField(label='Целевой уровень гликемии, ммоль/л',widget=widgets.NumberInput(max=20, min=1, step=0.1), validators=[DataRequired()])
    carb =  DecimalField(label='Критический уровень углеводов, г',widget=widgets.NumberInput(max=500, min=1, step=0.1), validators=[DataRequired()])
    dtype = SelectField(u'Тип диабета', choices=[('1', 'диабет I типа'),
                                       ('2', 'диабет II типа'), ('3', 'гестационный')
                                       ], validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))



class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

ch =[('0', 'Натощак'), ('1', 'После завтрака'),
                                              ('2', 'После обеда'), ('3', 'После ужина'),
                                              ('4', 'Дополнительно'), ('5', 'При родах')]
class SugarForm(FlaskForm):
    eat = SelectField(u'Прием пищи', choices=ch, validators=[DataRequired()])
    time=DateTimeLocalField(label='Время',format='%Y-%m-%dT%H:%M')
    mol = DecimalField(label='Уровень сахара, ммоль/л', default=5, widget=widgets.NumberInput(max=20, min=1, step=0.1), validators=[DataRequired()])
    submit = SubmitField(u'sugar')

class FoodForm(FlaskForm):
    food = SelectField(u'Продукт')
    # food2 = SearchField()
    eating = SelectField(u'Прием пищи', choices=[('1','Ужин'), ('2','Обед'), ('3','Завтрак'),('4','Перекус')], validators=[DataRequired()])
    time = DateTimeLocalField(label='Время', format='%Y-%m-%dT%H:%M')
    grams = IntegerField(label='вес, г', default=200, widget=widgets.NumberInput(min=1, max=600, step=1), validators=[DataRequired()])
    submit = SubmitField('food')
    def __init__(self):
        super(FoodForm, self).__init__()
        self.food.choices = [(c.index, c.food) for c in FoodDatatable.query.all()]
        # self.food2.choices = [(c.index, c.food) for c in FoodDatatable.query.all()]




class InsulinForm(FlaskForm):
    eat = SelectField(u'Прием пищи', choices=ch, validators=[DataRequired()])
    time=DateTimeLocalField(label='Время',format='%Y-%m-%dT%H:%M')
    ins = SelectField(u'Инсулин', choices=[('1', 'Ультракороткий'),
                                              ('2', 'Короткий'), ('3', 'Левимир'),
                                              ('4', 'Пролонгированный')], validators=[DataRequired()])
    dose = IntegerField(label='ед.', default=5,widget=widgets.NumberInput(min=1, max=40, step=1), validators=[DataRequired()])
    submit = SubmitField('insulin')



    #SELECT * FROM table WHERE field LIKE '%whatever%'
    #\u0025а\u0025
    #cur = db.query("table", "column", "column like ?", new String[] {"%а%"}, null, null, null);
    #"select string from stringtable where string like ? and type = ?",('%'+searchstr+'%', type))
    # df = readdb('SELECT food FROM food_datatable WHERE food LIKE ? and type=?', ('%'KFC'%', type))
    ##df = readdb('SELECT food FROM food_datatable WHERE food LIKE ?', ('%'+KFC+'%'))

    #cur.execute('SELECT * FROM user WHERE username LIKE '%sus%'')
    # cur.execute('SELECT * FROM user WHERE username LIKE ?', ('%' + sus + '%'))
    #{%goal%}".format(kappa=column, goal=kword)