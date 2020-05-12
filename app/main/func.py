from flask import flash
from flask_login import current_user
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates
import pylab
from datetime import datetime
import html
from flask_babel import _
from app import db



def plotfunc(df, colmn, user_id):
    matplotlib.style.use('ggplot')
    matplotlib.use('Agg')

    # # подставьте ссылку на ваш файл или полный путь к файлу на вашем компьютере...
    # url = 'D:/diplom/site02.8.02.20/table.xlsx'
    # df = pd.read_excel(url, names=['mol', 'timestamp'], index_col=[1], decimal=',',
    #                  parse_dates=True, dayfirst=True)
    plt.cla()
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    # df1 = dfl[['timestamp', 'mol']]
    df1 = dfl[[colmn]]
    df2=dfl[['timestamp']]
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    df2_float= [datetime.strptime(i, time_format) for i in df2['timestamp']]
    df2size=len(df2_float)
    # df2step=1
    # df2minsize=df2size-5 #scale
    # xmin=df2_float[df2minsize]
    # xmax=max(df2_float)

    ax =plt.subplot(1, 1, 1)
    # pylab.plot_date(df2_float, df1, fmt="b-")
    # # plt.ylabel('ммоль/л')
    # pylab.savefig('D:/diplom/site02.8.02.20/out.png')
    plt.figure(figsize=(17,8),dpi=500)
    plt.plot_date(df2_float,df1)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=25)
    # plt.xlim(xmin,xmax)


    plt.savefig('D:/diplom/site02.8.02.20/out.png')
    # plt.show()
    return 0


def writexls(df, user_id):
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    writer = pd.ExcelWriter('table.xlsx')
    dfl.to_excel(writer)
    writer.save()
    return dfl





# def sescommit(note, sql_string, colmn, user_id):
#     db.session.add(note)
#     db.session.commit()
#     table = readdb(sql_string)
#     writexls(table, user_id)
#     plotfunc(table, colmn, user_id)
#     flash(_('Your notes have been saved.'))

