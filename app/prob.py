import pandas as pd
import sqlite3

# from sqlalchemy import create_engine
#from pyensae.sql import import_flatfile_into_database

# import_flatfile_into_database('app.db', 'eatdb.xlsx', add_key='eatdb', encoding='ISO-8859-1')
# from app import db
# engine = create_engine('sqlite:///app.db')
from app import db

conn = sqlite3.connect('app.db')

df = pd.read_excel("eatdb.xlsx", encoding="ISO-8859-1")




#print(df)
df.to_sql('food_datatable',conn, if_exists='replace')
conn.execute("SELECT * FROM food_datatable").fetchall()
# engine.execute("SELECT * FROM food_data").fetchall()
#db.session.commit()
# for table, df1 in df1.items():
#     df1.to_sql(table, conn)
conn.commit()
#     conn.close()