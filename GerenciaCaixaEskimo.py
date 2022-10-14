import sqlite3
import datetime
from unittest import result
import pandas as pd
import os
import logging
import numpy as np
from IPython.display import display


#conectando no banco de dados
con = sqlite3.connect('D:\GerenciaEskimo\caixadb.db')

#criando um cursos
c = con.cursor()

#função para converter float para formato "R$0.000,00"
def toCurrency(value):
    if value >= 0:
        currency = 'R${:,.2f}'.format(value)
    else:
        currency = '-R${:,.2f}'.format(value*-1)
    return currency

#função para inserir dados
def caixaInsert(vDate, vAbertura, vVendas_dinheiro, vVendas_cc, vVendas_cd, vVendas_pix, vVendas_ifood, vSangria, vSuprimento, vSub_total, vFechamento, vQuebra_caixa):
    try:
        c.execute('INSERT INTO caixa_tb (date, abertura, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood, sangria, suprimento, sub_total, fechamento, quebra_caixa) values(strftime(\'%s\', ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (vDate, vAbertura, vVendas_dinheiro, vVendas_cc, vVendas_cd, vVendas_pix, vVendas_ifood, vSangria, vSuprimento, vSub_total, vFechamento, vQuebra_caixa))
    except:
        logging.exception('message')
        input()
    con.commit()

#função para ler dias com quebra de caixa
def readQuebraCaixa():
    result = pd.read_sql_query('SELECT date as Data, quebra_caixa as "Quebra Caixa" from caixa_tb where quebra_caixa != 0 ORDER by date', con)
    result['Data'] = result['Data'].map(lambda dates: datetime.datetime.utcfromtimestamp(dates).strftime('%d-%m-%Y'))
    result['Quebra Caixa'] = result['Quebra Caixa'].map(lambda valor: toCurrency(valor))
    display(result)
    input('Aperte ENTER para recomeçar')

#função para ler e listar as datas com os totais de venda
def readTotalVendas():
    resultTotalVendas = pd.read_sql_query('SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM caixa_tb ORDER BY date', con)
    resultTotalVendas['Total'] = resultTotalVendas.loc[0:resultTotalVendas.shape[0], ['vendas_dinheiro', 'vendas_cc', 'vendas_cd', 'vendas_pix', 'vendas_ifood']].sum(axis = 1)
    resultTotalVendasLimpo = resultTotalVendas.drop(resultTotalVendas.columns[[1, 2, 3, 4, 5]], axis = 1)
    resultTotalVendasLimpo['Data'] = resultTotalVendasLimpo['Data'].map(lambda dates: datetime.datetime.utcfromtimestamp(dates).strftime('%d-%m-%Y'))
    resultTotalVendasLimpo['Total'] = resultTotalVendasLimpo['Total'].map(lambda valor: toCurrency(valor))
    display(resultTotalVendasLimpo)
    input()

#função paa converter data dd/mm/yyyy para yyyy-mm-dd
def convertDtFormat(unformattedDt):
    day = unformattedDt[0] + unformattedDt[1]
    month = unformattedDt[3] + unformattedDt[4]
    year = unformattedDt[6] + unformattedDt[7] + unformattedDt[8] + unformattedDt[9]
    formattedDt = year + '-' + month + '-' + day
    return formattedDt

#função para pegar a media das quebras de caixa
def avgQuebraCaixa():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM caixa_tb'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    averageQuebra = np.average(resultQuebraCaixa['quebra_caixa'])
    return toCurrency(averageQuebra)

def avgQuebraCaixaQuandoTem():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM caixa_tb WHERE quebra_caixa != 0'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    return toCurrency(np.average(resultQuebraCaixa['quebra_caixa']))

def avgQuebraCaixaSobra():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM caixa_tb WHERE quebra_caixa > 0'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    averageQuebra = np.average(resultQuebraCaixa['quebra_caixa'])
    return toCurrency(averageQuebra)

def avgQuebraCaixaFalta():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM caixa_tb WHERE quebra_caixa < 0'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    averageQuebra = np.average(resultQuebraCaixa['quebra_caixa'])
    return toCurrency(averageQuebra)

def avgVendasComQuebra():
    consultaTotalVendas = 'SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM caixa_tb WHERE quebra_caixa != 0 ORDER BY date'
    resultTotalVendas = pd.read_sql_query(consultaTotalVendas, con)
    resultTotalVendas['Total'] = resultTotalVendas.loc[0:resultTotalVendas.shape[0], ['vendas_dinheiro', 'vendas_cc', 'vendas_cd', 'vendas_pix', 'vendas_ifood']].sum(axis = 1)
    resultTotalVendasLimpo = resultTotalVendas.drop(resultTotalVendas.columns[[0, 1, 2, 3, 4, 5]], axis = 1)
    averageTotal = np.average(resultTotalVendasLimpo['Total'])
    return toCurrency(averageTotal)

def avgVendas():
    consultaTotalVendas = 'SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM caixa_tb ORDER BY date'
    resultTotalVendas = pd.read_sql_query(consultaTotalVendas, con)
    for linha in resultTotalVendas.index:
        resultTotalVendas.loc[linha,'Total'] = resultTotalVendas.loc[linha,'vendas_dinheiro'] + resultTotalVendas.loc[linha,'vendas_cc'] + resultTotalVendas.loc[linha,'vendas_cd'] + resultTotalVendas.loc[linha,'vendas_pix'] + resultTotalVendas.loc[linha,'vendas_ifood']
    resultTotalVendasLimpo = resultTotalVendas.drop(resultTotalVendas.columns[[0, 1, 2, 3, 4, 5]], axis = 1)
    averageVendas = np.average(resultTotalVendasLimpo['Total'])
    return toCurrency(averageVendas)

def percentQuebra():
    consultaQuebraCaixaTotal = 'SELECT quebra_caixa FROM caixa_tb'
    consultaQuebraCaixaExclusivo = 'SELECT quebra_caixa FROM caixa_tb WHERE quebra_caixa != 0'
    resultTotal = pd.read_sql_query(consultaQuebraCaixaTotal, con)
    resultExclusivo = pd.read_sql_query(consultaQuebraCaixaExclusivo, con)
    percentual = (resultExclusivo.shape[0] / resultTotal.shape[0]) * 100
    percentual = '{:.2f}'.format(percentual)
    return (percentual + '%')

def avgVendasComQuebraEx():
    consultaTotalVendas = 'SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM caixa_tb WHERE quebra_caixa > 1 OR quebra_caixa < -1 ORDER BY date'
    resultTotalVendas = pd.read_sql_query(consultaTotalVendas, con)
    resultTotalVendas['Total'] = resultTotalVendas.loc[0:resultTotalVendas.shape[0], ['vendas_dinheiro', 'vendas_cc', 'vendas_cd', 'vendas_pix', 'vendas_ifood']].sum(axis = 1)
    resultTotalVendasLimpo = resultTotalVendas.drop(resultTotalVendas.columns[[0, 1, 2, 3, 4, 5]], axis = 1)
    averageTotal = np.average(resultTotalVendasLimpo['Total'])
    return toCurrency(averageTotal)

def percentQuebraEx():
    consultaQuebraCaixaTotal = 'SELECT quebra_caixa FROM caixa_tb'
    consultaQuebraCaixaExclusivo = 'SELECT quebra_caixa FROM caixa_tb WHERE quebra_caixa > 1 OR quebra_caixa < -1'
    resultTotal = pd.read_sql_query(consultaQuebraCaixaTotal, con)
    resultExclusivo = pd.read_sql_query(consultaQuebraCaixaExclusivo, con)
    percentual = (resultExclusivo.shape[0] / resultTotal.shape[0]) * 100
    percentual = '{:.2f}'.format(percentual)
    return (percentual + '%')

#função para registrar um caixa no banco de dados
def registroCaixa():
    print('Registro de Caixa da Eskimó Sorvetes')
    print('-'*100)

    while True:
        dataCaixa = input('Digite a data do caixa: ')
        try:
            datetime.datetime.strptime(dataCaixa, '%d/%m/%Y')
            break;
        except ValueError:
            print("Incorrect data format, should be DD-MM-YYYY")

    while True:
        aberturaCaixa = input('Valor de abertura: ')
        if ',' in aberturaCaixa:
            aberturaCaixa = aberturaCaixa.replace(',','.')
        elif aberturaCaixa == '':
            aberturaCaixa = '0'
        try:
            val = float(aberturaCaixa)
            break;
        except ValueError:
            print('This is not a valid number. Please enter a valid number.')

    while True:
        vendasDinheiroCaixa = input('Vendas em dinheiro: ')
        if ',' in vendasDinheiroCaixa:
            vendasDinheiroCaixa = vendasDinheiroCaixa.replace(',','.')
        elif vendasDinheiroCaixa == '':
            vendasDinheiroCaixa = '0'
        try:
            val = float(vendasDinheiroCaixa)
            break;
        except ValueError:
            print('This is not a valid number. Please enter a valid number.')

    while True:
        vendasCartaoCredCaixa = input('Vendas em cartão crédito: ')
        if ',' in vendasCartaoCredCaixa:
            vendasCartaoCredCaixa = vendasCartaoCredCaixa.replace(',','.')
        elif vendasCartaoCredCaixa == '':
            vendasCartaoCredCaixa = '0'
        try:
            val = float(vendasCartaoCredCaixa)
            break;
        except ValueError:
            print('This is not a valid number. Please enter a valid number.')

    while True:
        vendasCartaoDebCaixa = input('Vendas em cartão debito: ')
        if ',' in vendasCartaoDebCaixa:
            vendasCartaoDebCaixa = vendasCartaoDebCaixa.replace(',','.')
        elif vendasCartaoDebCaixa == '':
            vendasCartaoDebCaixa = '0'
        try:
            val = float(vendasCartaoDebCaixa)
            break;
        except ValueError:
            print('This is not a valid number. Please enter a valid number.')

    while True:
        vendasPixCaixa = input('Vendas em pix: ')
        if ',' in vendasPixCaixa:
            vendasPixCaixa = vendasPixCaixa.replace(',','.')
        elif vendasPixCaixa == '':
            vendasPixCaixa = '0'
        try:
            val = float(vendasPixCaixa)
            break;
        except ValueError:
            print('This is not a valid number. Please enter a valid number.')

    while True:
        vendasIfoodCaixa = input('Vendas em ifood: ')
        if ',' in vendasIfoodCaixa:
            vendasIfoodCaixa = vendasIfoodCaixa.replace(',','.')
        elif vendasIfoodCaixa == '':
            vendasIfoodCaixa = '0'
        try:
            val = float(vendasIfoodCaixa)
            break;
        except ValueError:
            print('This is not a valid number. Please enter a valid number.')

    while True:
        sangriaCaixa = input('Sangria: ')
        if ',' in sangriaCaixa:
            sangriaCaixa = sangriaCaixa.replace(',','.')
        elif sangriaCaixa == '':
            sangriaCaixa = '0'
        try:
            val = float(sangriaCaixa)
            break;
        except ValueError:
            print('This is not a valid number. Please enter a valid number.')

    while True:
        suprimentoCaixa = input('Suprimento: ')
        if ',' in suprimentoCaixa:
            suprimentoCaixa = suprimentoCaixa.replace(',','.')
        elif suprimentoCaixa == '':
            suprimentoCaixa = '0'
        try:
            val = float(suprimentoCaixa)
            break;
        except ValueError:
            print('This is not a valid number. Please enter a valid number.')

    subTotalCaixa = round(float(aberturaCaixa) + float(vendasDinheiroCaixa) - float(sangriaCaixa) + float(suprimentoCaixa), 2)

    while True:
        fechamentoCaixa = input('Fechamento: ')
        if ',' in fechamentoCaixa:
            fechamentoCaixa = fechamentoCaixa.replace(',','.')
        elif fechamentoCaixa == '':
            fechamentoCaixa = '0'
        try:
            val = float(fechamentoCaixa)
            break;
        except ValueError:
            print('This is not a valid number. Please enter a valid number.')


    quebraCaixa = round(float(fechamentoCaixa) - float(subTotalCaixa), 2)

    clearConsole()
    print('Data: %s' % (dataCaixa))
    print('%s Abertura' % (toCurrency(float(aberturaCaixa))))
    print('%s Vendas - Dinheiro' % (toCurrency(float(vendasDinheiroCaixa))))
    print('%s Sangria' % (toCurrency(float(sangriaCaixa))))
    print('%s Suprimento' % (toCurrency(float(suprimentoCaixa))))
    print('%s SubTotal' % (toCurrency(float(subTotalCaixa))))
    print('%s Fechamento' % (toCurrency(float(fechamentoCaixa))))
    print('%s Quebra de Caixa' % (toCurrency(float(quebraCaixa))))
    print('Cartão Débito %s' % (toCurrency(float(vendasCartaoDebCaixa))))
    print('Cartão Crédito %s' % (toCurrency(float(vendasCartaoCredCaixa))))
    print('Pix %s' % (toCurrency(float(vendasPixCaixa))))
    print('iFood %s' % (toCurrency(float(vendasIfoodCaixa))))

    while True:
        confirm = input('Confirma os valores? (Y/N) ')
        if confirm == 'y':
            dataCaixa = convertDtFormat(dataCaixa)
            caixaInsert(dataCaixa, aberturaCaixa, vendasDinheiroCaixa, vendasCartaoCredCaixa, vendasCartaoDebCaixa, vendasPixCaixa, vendasIfoodCaixa, sangriaCaixa, suprimentoCaixa, subTotalCaixa, fechamentoCaixa, quebraCaixa)
            #dataRead()
            input('Aperte ENTER para recomeçar')
            clearConsole()
            break;
        if confirm == 'n':
            print('Entrada cancelada, aperte ENTER para sair')
            clearConsole()
            break;

def printStatistics():
    clearConsole()
    print('Média de vendas por dia: %s' %(avgVendas()))
    print('-'*100)
    print('Quebras')
    print('Média das Quebras de caixa (total): %s                               Média de Sobra: %s' %(avgQuebraCaixa(), avgQuebraCaixaSobra()))
    print('Média das Quebras de caixa (quando há quebra): %s                    Média de Falta: %s' %(avgQuebraCaixaQuandoTem(), avgQuebraCaixaFalta()))
    print('Média do Total de vendas nos dias com Quebra de caixa: %s        Porcentagem de dias com Quebra de Caixa: %s' %(avgVendasComQuebra(), percentQuebra()))
    print('M. do T. de v. nos dias com Q. de c. maior que R$1,00: %s        Porc. de dia com Q. de c. maior que R$1,00: %s' %(avgVendasComQuebraEx(), percentQuebraEx()))
    input()

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clearConsole()
        print('1: Registro de caixa')
        print('2: Dias com quebra de caixa')
        print('3: Vendas por dia')
        print('4: Estatísticas')
        print('5: Sair')
        option = int(input('Opção desejada: '))

        if option == 1:
            clearConsole()
            registroCaixa()
        elif option == 2:
            clearConsole()
            readQuebraCaixa()
        elif option == 3:
            clearConsole()
            readTotalVendas()
        elif option == 4:
            printStatistics()
        elif option == 5:
            break;
        else:
            print('opção inexistente')

    input('Pressione ENTER para sair')
    con.close()

if __name__ == '__main__':
    main()