import sqlite3

from flask import flash
from flask_login import current_user
from flask_babel import _
from app import db
from app.main.forms import SugarForm
from datetime import datetime
import pandas as pd
from app.models import SugarTable, FoodTable, InsulinTable


def eatf(eat):
    ch = 'no data'
    if eat == '1':
        ch = 'После завтрака'
    elif eat == '2':
        ch = 'После обеда'
    elif eat == '3':
        ch = 'После ужина'
    elif eat == '4':
        ch = 'Дополнительно'
    elif eat == '5':
        ch = 'При родах'
    elif eat == '0':
        ch = 'Натощак'
    return ch

def instypef(type):
    if type == '1':
        ih = 'Ультракороткий'
    elif type == '2':
        ih = 'Короткий'
    elif type == '3':
        ih = 'Левимир'
    elif type == '4':
        ih = 'Пролонгированный'
    return ih


def readdb(sql_string):
    DB_NAME = 'app.db'
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(sql_string, conn)
    return df

def sugarfunc(form):
    time = form.time.data
    eat = eatf(form.eat.data)
    if time:
        #timendate = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        note = SugarTable(eat=eat, user_id=current_user.id, mol=form.mol.data, timestamp=time)
    else:
        note = SugarTable(eat=eat, user_id=current_user.id, mol=form.mol.data)
    db.session.add(note)
    db.session.commit()
    return flash(_('Your changes have been saved.'))

def insfunc(form):
    time = form.time.data
    eat = eatf(form.eat.data)
    ins = instypef(form.ins.data)
    if time:
        # timendate = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        note = InsulinTable(eat=eat, insulin=ins, user_id=current_user.id, dose=form.mol.data, timestamp=time)
    else:
        note = InsulinTable(eat=eat,insulin=ins, user_id=current_user.id, dose=form.mol.data)
    db.session.add(note)
    db.session.commit()
    return flash(_('Your changes have been saved.'))

def foodfunc(form):
    time = form.time.data
    df = readdb('select * from food_datatable')
    index=form.eat.data
    ind=int(index)
    food = df.loc[ind,'food']
    fats = df.loc[ind, 'fats']
    carb = df.loc[ind, 'carbohydrates']
    pr = df.loc[ind, 'protein']
    if time:
        note = FoodTable(food=food, fats=fats, carbohydrates=carb, protein=pr, user_id=current_user.id, timestamp=time)
    else:
        note = FoodTable(food=food, fats=fats, carbohydrates=carb, protein=pr, user_id=current_user.id)
    db.session.add(note)
    db.session.commit()
    return flash(_('Your changes have been saved.'))

