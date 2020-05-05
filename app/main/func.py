
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates
import pylab
from datetime import datetime
def plotf(df, user_id):

    matplotlib.style.use('ggplot')

    # # подставьте ссылку на ваш файл или полный путь к файлу на вашем компьютере...
    # url = 'D:/diplom/site02.8.02.20/table.xlsx'
    #
    # df = pd.read_excel(url, names=['mol', 'timestamp'], index_col=[1], decimal=',',
    #                  parse_dates=True, dayfirst=True)
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    # df1 = dfl[['timestamp', 'mol']]
    df1 = dfl[['mol']]
    df2=dfl[['timestamp']]
    # df1.dropna(inplace=True)
    # df2.dropna(inplace=True)
    # gfg1 = pd.DataFrame(df1['mol'])
    # gfg2 = pd.DataFrame(df2['timestamp'])
    # ar1=gfg1.to_numpy()

    # df1.plot()
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    df2_float= [datetime.strptime(i, time_format) for i in df2['timestamp']]
    # # ar2_float = matplotlib.dates.date2num(ar2)
    ax = pylab.subplot(1, 1, 1)


    # pylab.plot_date(df2_float, df1, fmt="b-")
    # # plt.ylabel('ммоль/л')
    # pylab.savefig('D:/diplom/site02.8.02.20/out.png')
    plt.plot(df2_float,df1)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=25)
    plt.savefig('D:/diplom/site02.8.02.20/out.png')
    # plt.show()
    return df1

def readdb(sql_string):
    DB_NAME = 'app.db'
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(sql_string, conn)
    return df

def writexls(df, user_id):
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    writer = pd.ExcelWriter('table.xlsx')
    dfl.to_excel(writer)
    writer.save()
    return dfl



def eatf(eat):
    ch = 'no data'
    if eat == '1':
        ch = 'После завтрака'
    elif eat == '2': \
            ch = 'После обеда'
    elif eat == '3':
        ch = 'После ужина'
    elif eat == '4':
        ch = 'Дополнительно'
    elif eat == '5':
        ch = 'При родах'
    elif eat == '6':
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

