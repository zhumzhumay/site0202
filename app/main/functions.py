import sqlite3

from flask import flash
from flask_login import current_user
from flask_babel import _
from app import db
from app.main.forms import SugarForm
from datetime import timedelta,datetime
import pandas as pd
from app.models import SugarTable, InsulinTable, FoodTable

def priem(eat):
    if eat == '1':
        ch = 'Завтрак'
    elif eat == '2':
        ch = 'Обед'
    elif eat == '3':
        ch = 'Ужин'
    elif eat == '4':
        ch = 'Перекус'
    return ch

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

def kkal(g, ft, pt, ct):
    fi = 9.29
    pi = 4.1
    ci = 4.1
    fk = (g / 100) * fi * ft
    pk = (g / 100) * pi * pt
    ck = (g / 100) * ci * ct
    kkal = fk + pk + ck
    kkal = round(kkal,2)
    return kkal

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
    grams = form.grams.data
    time = form.time.data
    df = readdb('select * from food_datatable')
    index = form.food.data
    ind=int(index)
    eating = priem(form.eating.data)
    food = df.loc[ind,'food']
    fats = df.loc[ind, 'fats']
    carb = df.loc[ind, 'carbohydrates']
    pr = df.loc[ind, 'protein']
    Kkal = kkal(grams,fats,pr,carb)
    if time:
        note = FoodTable(food=food, kkal=Kkal, eating=eating, user_id=current_user.id, timestamp=time)
    else:
        note = FoodTable(food=food, kkal=Kkal, eating=eating,  user_id=current_user.id)
    db.session.add(note)
    db.session.commit()
    return flash(_('Your changes have been saved.'))

def maxkkal():
    user_id = current_user.id
    delta = timedelta(days=1)
    df = readdb('select user_id, kkal, timestamp from food_table')
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    df1 = dfl.timestamp
    ind = df1.index
    dfk = dfl.kkal
    df1 = pd.to_datetime(df1)
    maxd = df1.max()
    mind = maxd - delta
    list =[]
    c = 0
    for i in ind:
        a = df1[i]
        if a>= mind:
            list.append(i)
    for i in list:
        c = c + dfk[i]
    return c


def fordoc(user_id):
    # user_id=current_user.id
    sql_string = 'select * from followers'
    bd=readdb(sql_string)
    dfl = bd.loc[lambda df: df['follower_id'] == user_id, :]
    # docnote = dfl[['followed_id']]
    return dfl

def names (docb):
    docb = docb.followed_id
    rdb = readdb('select * from user')
    j=0
    pcntnote = []
    for i in docb:
        j = j+1
        username = rdb.loc[i, 'username']
        name = rdb.loc[i, 'full_name']
        dt = rdb.loc[i, 'diatype']
        age = rdb.loc[i, 'age']
        w = rdb.loc[i,'weight']
        k = (username, j, name, dt, age, w)
        pcntnote.append(k)
    return pcntnote

