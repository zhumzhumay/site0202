import sqlite3
# import matplotlib.pyplot as plt
# import matplotlib
# import matplotlib.dates
from flask import flash
from flask_login import current_user
from flask_babel import _
from app import db
#from app.main.forms import SugarForm
from datetime import timedelta, datetime
import pandas as pd
from app.models import SugarTable, InsulinTable, FoodTable, Message, User, Sport


def BMI(form):
    m = form.weight.data
    h = form.height.data
    bmi = (m / (h * h)) * 10000
    return bmi


def sprtf(sport):
    ch = 'no data'
    if sport == '1':
        ch = 'Сон'
    elif sport == '2':
        ch = 'Ходьба'
    elif sport == '3':
        ch = 'Зарядка'
    elif sport == '4':
        ch = 'Спорт'
    elif sport == '5':
        ch = 'Уборка в квартире'
    elif sport == '6':
        ch = 'Работа в огороде'
    return ch


def dtype(diatype):
    ch = current_user.diatype
    if diatype == '1':
        ch = 'I типа'
    elif diatype == '2':
        ch = 'II типа'
    elif diatype == '3':
        ch = 'гестационный'
    return ch


def curdtype():
    diatype = current_user.diatype
    if diatype == 'I типа':
        ch = '1'
    elif diatype == 'II типа':
        ch = '2'
    elif diatype == 'гестационный':
        ch = '3'
    return ch


def priem(eat):
    ch = 'no data'
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
    ch = 'no data'
    if type == '1':
        ch = 'Ультракороткий'
    elif type == '2':
        ch = 'Короткий'
    elif type == '3':
        ch = 'Левимир'
    elif type == '4':
        ch = 'Пролонгированный'
    return ch


def readdb(sql_string):
    DB_NAME = 'app.db'
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(sql_string, conn)
    return df


def howtime(days, minutes, table, maxt):
    user_id = current_user.id
    delta = timedelta(days=days, minutes=minutes)
    df = readdb(table)
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    df1 = dfl.timestamp
    df1 = pd.to_datetime(df1)
    ind = df1.index
    if maxt != 0:
        maxd = maxt
    else:
        maxd = df1.max()

    mind = maxd - delta
    list = []
    for i in ind:
        a = df1[i]
        if maxd >= a >= mind:
            list.append(i)
    return list, dfl


def junkfood():
    user_id = current_user.id
    df = readdb('select * from sugar_table')
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    dfs = dfl.BG
    ind = dfs.index
    timelist = []
    for i in ind:
        a = dfs[i]
        if a >= current_user.sugarlevel:
            time = df.loc[i, 'timestamp']
            timelist.append(time)
    timedf = pd.DataFrame(timelist)
    timedf = pd.to_datetime(timedf[0])  # 0-column
    ind = timedf.index
    list1 = []
    for i in ind:
        a = timedf[i]
        list1.append(a)
    timedf = pd.DataFrame(list1)
    timedf = pd.to_datetime(timedf[0])  # 0-column
    junklist = []
    for i in timedf:
        list2, dfus = howtime(0, 60, 'select * from food_table', i)
        dffood = dfus.food
        for j in list2:
            f = dffood[j]
            junklist.append(f)
    list3 = []
    for food in junklist:
        c = junklist.count(food)
        k = (food, c)
        list3.append(k)
    junklist = list(set(list3))
    return junklist


def kkal(g, ft, pt, ct):
    fi = 9.29
    pi = 4.1
    ci = 4.1
    fk = (g / 100) * fi * ft
    pk = (g / 100) * pi * pt
    ck = (g / 100) * ci * ct
    kkal = fk + pk + ck
    kkal = round(kkal, 2)
    return kkal


def makegraph(table1, user_id):
    df = readdb(table1)
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    return dfl


def send_attention(body):
    user_id = current_user.id
    df = readdb('select * from followers')
    followed = df.loc[df['follower_id'] == user_id, 'followed_id']
    user = User.query.get(followed)
    msg = Message(author=current_user, recipient=user,
                  body=body)
    flash(_(body))
    db.session.add(msg)
    db.session.commit()


def sugarlim():
    if current_user.sugar != None:
        sugarlevel = current_user.sugarlevel
    else:
        sugarlevel = 9
    list, dfl = howtime(7, 0, 'select user_id, BG, timestamp from sugar_table', 0)
    dfm = dfl.BG
    c = 0
    for i in list:
        if sugarlevel <= dfm[i]:
            c = c + 1
    return c


def sugarfoodtime(time):
    user_id = current_user.id
    df = readdb('select timestamp, user_id from food_table')
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    df1 = dfl.timestamp
    df1 = pd.to_datetime(df1)
    stime = pd.to_datetime(time)
    ftime = df1.max()
    deltat = stime - ftime
    deltat = str(deltat)[7:-7]
    return deltat


def sugarfunc(form):
    time = form.time.data
    eat = eatf(form.eat.data)
    ml = form.BG.data
    mol = round(ml, 3)

    if time:
        taeating = sugarfoodtime(time)
        # timendate = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        note = SugarTable(eat=eat, user_id=current_user.id, BG=mol, time_after_eating=taeating, timestamp=time)
    else:
        taeating = sugarfoodtime(datetime.now())
        note = SugarTable(eat=eat, user_id=current_user.id, BG=mol, time_after_eating=taeating)
    db.session.add(note)
    db.session.commit()
    mol1 = sugarlim()
    if (mol >= 9) or (mol1 >= 2):
        send_attention('Уровень гликемии превышен')
    else:
        flash(_('Ваша запись сохранена'))


def insfunc(form):
    time = form.time.data
    eat = eatf(form.eat.data)
    ins = instypef(form.ins.data)
    dose = form.dose.data
    if time:
        # timendate = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        note = InsulinTable(eat=eat, insulin=ins, user_id=current_user.id, dose=dose, timestamp=time)
    else:
        note = InsulinTable(eat=eat, insulin=ins, user_id=current_user.id, dose=dose)
    db.session.add(note)
    db.session.commit()
    return flash(_('Ваша запись сохранена'))


def foodsame(user_id):
    dfe = readdb('select * from food_table')
    dft = dfe.loc[lambda df: df['user_id'] == user_id, :]
    dft1 = dft.tail(1)
    indf = dft1.food
    for i in indf:
        fname = i
    df = readdb('select * from food_datatable')
    dfname = df.loc[lambda df: df['food'] == fname, :]
    for i in dfname.index:
        ind = i
    fats = df.loc[ind, 'fats']
    carb = df.loc[ind, 'carbohydrates']
    valcat = df.loc[ind, 'category']
    dfl = df.loc[lambda df: df['category'] == valcat, :]
    for i in dfl:
        indx = dfl.index
    list = []
    j = 0
    for i in indx:
        morcarb = df.loc[i, 'carbohydrates']
        morfats = df.loc[i, 'fats']
        pr = df.loc[i, 'protein']
        if (morcarb < carb) and (morfats < fats):
            j = j + 1
            eat = df.loc[i, 'food']
            k = (j, eat, pr, morfats, morcarb)
            list.append(k)
    return list


def foodfunc(form):
    grams = form.grams.data
    time = form.time.data
    df = readdb('select * from food_datatable')
    index = form.food.data
    ind = int(index)
    eating = priem(form.eating.data)
    food = df.loc[ind, 'food']
    fats = df.loc[ind, 'fats']
    carb = df.loc[ind, 'carbohydrates']
    pr = df.loc[ind, 'protein']
    kl = kkal(grams, fats, pr, carb)
    Kkal = round(kl, 3)
    cr = (grams / 100) * carb
    carbs = round(cr, 3)
    if time:
        note = FoodTable(food=food, kkal=Kkal, eating=eating, carbohydrates=carbs, user_id=current_user.id,
                         timestamp=time)
    else:
        note = FoodTable(food=food, kkal=Kkal, eating=eating, carbohydrates=carbs, user_id=current_user.id)
    db.session.add(note)
    db.session.commit()
    junklist = junkfood()
    f = False
    for jfood, j in junklist:
        if j >= 3 and jfood == food: f = True
    if f == True:
        flash(_('Выбранный продукт приводит к повышению уровня глюкозы, постарайтесь уменьшить его потребление'))
    else:
        flash(_('Ваша запись сохранена'))

    q = kkallim()
    c = carblim()
    qlim = current_user.kkal
    clim = current_user.carbohydrates_level
    if q <= qlim or c <= clim:
        if q <= qlim and c <= clim:
            send_attention('Значение потребленных калорий и углеводов ниже базовой потребности')
        else:
            if q <= qlim:
                send_attention('Значение потребленных калорий ниже базовой потребности')
            if c <= clim:
                send_attention('Значение потребленных углеводов ниже базовой потребности')
    return ind


def sportfunc(form):
    time = form.time.data
    sport = sprtf(form.sport.data)
    sporttime = form.sporttime.data
    if time:
        # timendate = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        note = Sport(sport=sport, time=sporttime, user_id=current_user.id, timestamp=time)
    else:
        note = Sport(sport=sport, time=sporttime, user_id=current_user.id)
    db.session.add(note)
    db.session.commit()
    return flash(_('Ваша запись сохранена'))


def kkallim():
    list, dfl = howtime(21, 0, 'select * from food_table', 0)
    dfk = dfl.kkal
    c = 0
    for i in list:
        c = c + dfk[i]
    return c


def carblim():
    list, dfl = howtime(1, 0, 'select * from food_table', 0)
    dfk = dfl.carbohydrates
    c = 0
    for i in list:
        c = c + dfk[i]
    return c


def fordoc(user_id):
    # user_id=current_user.id
    sql_string = 'select * from followers'
    bd = readdb(sql_string)
    dfl = bd.loc[lambda bd: bd['follower_id'] == user_id, :]
    # docnote = dfl[['followed_id']]
    # dfl2=dfl.loc[:,['index','food']]
    return dfl


def names(docb):
    docb1 = docb.followed_id
    rdb = readdb('select * from user')
    j = 0
    pcntnote = []
    for i in docb1:
        j = j + 1
        i = i - 1
        # prom = rdb.loc[lambda rdb: rdb['id'] == i, :]
        username = rdb.loc[i, 'username']
        name = rdb.loc[i, 'full_name']
        dt = rdb.loc[i, 'diatype']
        age = rdb.loc[i, 'age']
        w = rdb.loc[i, 'BMI']
        k = (username, j, name, dt, age, w)
        pcntnote.append(k)
    return pcntnote


def folvalid(user):
    docb = fordoc(current_user.id)
    docb1 = docb.followed_id
    user_id = user.id
    j = 0
    for i in docb1:
        i = i - 1
        if i == user_id:
            j = j + 1
    if j != 1:
        flash('Данный пользователь не является вашим пациентом')
    return j  # must be 1


def normdates(df):
    b = []
    for i in df:
        p = str(i)[2:-10]
        b.append(p)
    return b
# def plotfunc(df, colmn, user_id):
#     matplotlib.style.use('ggplot')
#     matplotlib.use('Agg')
#
#     # # подставьте ссылку на ваш файл или полный путь к файлу на вашем компьютере...
#     # url = 'D:/diplom/site02.8.02.20/table.xlsx'
#     # df = pd.read_excel(url, names=['mol', 'timestamp'], index_col=[1], decimal=',',
#     #                  parse_dates=True, dayfirst=True)
#     plt.cla()
#     dfl = df.loc[lambda df: df['user_id'] == user_id, :]
#     # df1 = dfl[['timestamp', 'mol']]
#     df1 = dfl[[colmn]]
#     df2=dfl[['timestamp']]
#     time_format = '%Y-%m-%d %H:%M:%S.%f'
#     df2_float= [datetime.strptime(i, time_format) for i in df2['timestamp']]
#     df2size=len(df2_float)
#     # df2step=1
#     # df2minsize=df2size-5 #scale
#     # xmin=df2_float[df2minsize]
#     # xmax=max(df2_float)
#
#     ax =plt.subplot(1, 1, 1)
#     # pylab.plot_date(df2_float, df1, fmt="b-")
#     # # plt.ylabel('ммоль/л')
#     # pylab.savefig('D:/diplom/site02.8.02.20/out.png')
#     plt.figure(figsize=(17,8),dpi=500)
#     a = plt.plot_date(df2_float,df1)
#     plt.setp(ax.xaxis.get_majorticklabels(), rotation=25)
#     # plt.xlim(xmin,xmax)
#     plt.savefig('app/savedfiles/out.png')
#     # plt.show()
#     return a
