from flask import request
from flask_wtf import FlaskForm, widgets
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Length, Email
from flask_babel import _, lazy_gettext as _l
from app.models import User
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


# class SugarForm(FlaskForm):
#     eat = SelectField(u'Прием пищи', choices=[('0', 'Натощак'), ('1', 'После завтрака'),
#                                               ('2', 'После обеда'), ('3', 'После ужина'),
#                                               ('4', 'Дополнительно'), ('5', 'При родах')])
#     submit = SubmitField(_l('Submit'))
#
#
# class RebootForm(FlaskForm):
#     all_selected = SelectMultipleField('Select All',  choices=[('0', 'Натощак'), ('1', 'После завтрака'),
#                                               ('2', 'После обеда'), ('3', 'После ужина'),
#                                               ('4', 'Дополнительно'), ('5', 'При родах')])
#     available = SelectMultipleField('Available',  choices=[('0', 'Натощак'), ('1', 'После завтрака'),
#                                               ('2', 'После обеда'), ('3', 'После ужина'),
#                                               ('4', 'Дополнительно'), ('5', 'При родах')])
#     availableNR = SelectMultipleField('Available Net Relays',  choices=[('0', 'Натощак'), ('1', 'После завтрака'),
#                                               ('2', 'После обеда'), ('3', 'После ужина'),
#                                               ('4', 'Дополнительно'), ('5', 'При родах')])
