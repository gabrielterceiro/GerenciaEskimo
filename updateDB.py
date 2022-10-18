import Connectdb
import pandas as pd
import sqlite3
import datetime

con = Connectdb.connectdb.con

def convertDtFormat(unformattedDt):
    day = unformattedDt[0] + unformattedDt[1]
    month = unformattedDt[3] + unformattedDt[4]
    year = unformattedDt[6] + unformattedDt[7] + unformattedDt[8] + unformattedDt[9]
    formattedDt = datetime.datetime(int(year), int(month), int(day))
    #formattedDt = year + '-' + month + '-' + day
    return formattedDt

df_dts = pd.read_sql_query('Select date from tb_caixa',con)

df_dts['date'] = df_dts['date'].map(lambda dates: datetime.datetime.utcfromtimestamp(dates).strftime('%d-%m-%Y'))
print(df_dts.to_markdown())
df_dts['date'] = df_dts['date'].map(lambda dates: convertDtFormat(dates))
df_dts['date'] = df_dts['date'].map(lambda dates: int(datetime.datetime.timestamp(dates)))
print(df_dts.to_string())