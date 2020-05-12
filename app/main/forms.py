from flask import request
from flask_wtf import FlaskForm, widgets
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField, FloatField, BooleanField
from wtforms.fields.html5 import DateTimeLocalField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, Email
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
    weight = StringField(_l('Weight'))                                                        #new
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
    time=DateTimeLocalField(label='Время приема пищи',format='%Y-%m-%dT%H:%M')
    mol = DecimalField(label='ммоль/л', default=5, validators=[DataRequired()])
    #submit = SubmitField(u'sugar')

class FoodForm(FlaskForm):
    food = SelectField()
    eating = SelectField(u'Прием пищи', choices=[('1','Ужин'), ('2','Обед'), ('3','Завтрак'),('4','Перекус')], validators=[DataRequired()])
    time = DateTimeLocalField(label='Время приема пищи', format='%Y-%m-%dT%H:%M')
    grams = IntegerField(label='г', default=200, validators=[DataRequired()])
    #submit = SubmitField('Submit')
    def __init__(self):
        super(FoodForm, self).__init__()
        self.food.choices = [(c.index, c.food) for c in FoodDatatable.query.all()]

class InsulinForm(FlaskForm):
    eat = SelectField(u'Прием пищи', choices=ch, validators=[DataRequired()])
    time=DateTimeLocalField(label='Время приема пищи',format='%Y-%m-%dT%H:%M')
    dose = IntegerField(label='ед.', default=5, validators=[DataRequired()])
    ins = SelectField(u'Инсулин', choices=[('1', 'Ультракороткий'),
                                              ('2', 'Короткий'), ('3', 'Левимир'),
                                              ('4', 'Пролонгированный')], validators=[DataRequired()])

