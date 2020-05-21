import pandas as pd
import sqlite3

from app import db

conn = sqlite3.connect('app.db')

df = pd.read_excel("eatdb.xlsx", encoding="ISO-8859-1")





df.to_sql('food_datatable',conn, if_exists='replace')
conn.execute("SELECT * FROM food_datatable").fetchall()

conn.commit()
