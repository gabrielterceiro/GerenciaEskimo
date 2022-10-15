from time import strftime
import pandas as pd
import datetime
import Miscelaneous as misc
from Connectdb import connectdb

con = connectdb.con
c = con.cursor()

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
            readTotalVendas(inicial, final)
            break       
        if seeIfFilter == 'n':
            readTotalVendas()
            break

#função para ler e listar as datas com os totais de venda
def readTotalVendas(*args):
    if len(args) == 0:
        resultTotalVendas = pd.read_sql_query('SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM tb_caixa ORDER BY date', con)
    if len(args) == 2:
        resultTotalVendas = pd.read_sql_query('SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM tb_caixa WHERE date >= strftime(\'%s\', ?) AND date <= strftime(\'%s\', ?) ORDER BY date', con, params=(misc.convertDtFormat(args[0]), misc.convertDtFormat(args[1])))
    resultTotalVendas['Vendas'] = resultTotalVendas.loc[0:resultTotalVendas.shape[0], ['vendas_dinheiro', 'vendas_cc', 'vendas_cd', 'vendas_pix', 'vendas_ifood']].sum(axis = 1)
    resultTotalVendas = resultTotalVendas.drop(resultTotalVendas.columns[[1, 2, 3, 4, 5]], axis = 1)
    resultTotalVendas['Data'] = resultTotalVendas['Data'].map(lambda dates: datetime.datetime.utcfromtimestamp(dates).strftime('%d-%m-%Y'))
    soma = 0
    for valor in resultTotalVendas['Vendas']:
        soma += valor
    resultTotalVendas.at['Total', 'Vendas'] = soma
    resultTotalVendas['Vendas'] = resultTotalVendas['Vendas'].map(lambda valor: misc.toCurrency(valor))
    print(resultTotalVendas.to_markdown())
    input()