import datetime
import Miscelaneous as misc
import pandas as pd
from Connectdb import connectdb

con = connectdb.con

def ifFilter():
    
    while True:
        seeIfFilter = input('Gostaria de filtrar as datas? (Y/N) ')
        if seeIfFilter == 'y':
            while True:
                inicial = input('Data inicial: ')
                try:
                    datetime.datetime.strptime(inicial, '%d/%m/%Y')
                    break
                except ValueError:
                    print("Incorrect data format, should be DD/MM/YYYY")
            while True:
                final = input('Data final: ')
                try:
                    datetime.datetime.strptime(final, '%d/%m/%Y')
                    break
                except ValueError:
                    print("Incorrect data format, should be DD/MM/YYYY")
            readQuebraCaixa(inicial, final)
            break       
        if seeIfFilter == 'n':
            readQuebraCaixa()
            break

#função para ler dias com quebra de caixa
def readQuebraCaixa(*args):
    if len(args) == 0:
        result = pd.read_sql_query('SELECT date as Data, quebra_caixa as "Quebra Caixa" from tb_caixa where quebra_caixa != 0 ORDER by date', con)
    if len(args) == 2:
        result = pd.read_sql_query('SELECT date as Data, quebra_caixa as "Quebra Caixa" from tb_caixa WHERE date >= strftime(\'%s\', ?) AND date <= strftime(\'%s\', ?) AND quebra_caixa != 0 ORDER BY date', con, params=(misc.convertDtFormat(args[0]), misc.convertDtFormat(args[1])))
    #result = pd.read_sql_query('SELECT date as Data, quebra_caixa as "Quebra Caixa" from tb_caixa where quebra_caixa != 0 ORDER by date', con)
    result['Data'] = result['Data'].map(lambda dates: datetime.datetime.utcfromtimestamp(dates).strftime('%d-%m-%Y'))
    result['Quebra Caixa'] = result['Quebra Caixa'].map(lambda valor: misc.toCurrency(valor))
    print(result.to_markdown())
    input('Aperte ENTER para recomeçar')
    misc.clearConsole()