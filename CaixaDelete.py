import Connectdb
import datetime
import Miscelaneous as misc
import sqlite3

con = Connectdb.connectdb.con
c = con.cursor()

def removeData():
    while True:
        dtRemove = input('Digite a data do caixa: ')
        try:
            datetime.datetime.strptime(dtRemove, '%d/%m/%Y')
            break
        except ValueError:
            print('Incorrect data format, should be DD/MM/YYYY')

    print(dtRemove)
    dtRemove = int(datetime.datetime.timestamp(misc.convertDtFormat(dtRemove)))
    print(dtRemove)
    try:
        sql = '''DELETE FROM tb_caixa WHERE date = ?'''
        c.execute(sql, (dtRemove,))
        con.commit()
        input()
    except sqlite3.Error as error:
        print('Não foi possível realizar a operação', error)
        input()
    
