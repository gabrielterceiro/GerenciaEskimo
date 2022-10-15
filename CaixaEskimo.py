import sqlite3
import datetime
import pandas as pd
import os
import re
import numpy as np
from IPython.display import display
import pdfplumber
import glob


#conectando no banco de dados
con = sqlite3.connect('D:\GerenciaEskimo\caixadb.db')

#criando um cursos
c = con.cursor()

#função para converter float para formato "R$0.000,00"
def toCurrency(value):
    value = float(value)
    value /= 100
    if value >= 0:
        currency = 'R${:,.2f}'.format(value)
    else:
        currency = '-R${:,.2f}'.format(value*-1)
    return currency

#função para inserir dados
def caixaInsert(vDate, vAbertura, vVendas_dinheiro, vVendas_cc, vVendas_cd, vVendas_pix, vVendas_ifood, vSangria, vSuprimento, vSub_total, vFechamento, vQuebra_caixa):
    try:
        c.execute('INSERT INTO tb_caixa (date, abertura, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood, sangria, suprimento, sub_total, fechamento, quebra_caixa) values(strftime(\'%s\', ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (vDate, vAbertura, vVendas_dinheiro, vVendas_cc, vVendas_cd, vVendas_pix, vVendas_ifood, vSangria, vSuprimento, vSub_total, vFechamento, vQuebra_caixa))
    except:
        input()
    con.commit()

#função para ler dias com quebra de caixa
def readQuebraCaixa():
    result = pd.read_sql_query('SELECT date as Data, quebra_caixa as "Quebra Caixa" from tb_caixa where quebra_caixa != 0 ORDER by date', con)
    result['Data'] = result['Data'].map(lambda dates: datetime.datetime.utcfromtimestamp(dates).strftime('%d-%m-%Y'))
    result['Quebra Caixa'] = result['Quebra Caixa'].map(lambda valor: toCurrency(valor))
    display(result)
    input('Aperte ENTER para recomeçar')

#função para ler e listar as datas com os totais de venda
def readTotalVendas():
    resultTotalVendas = pd.read_sql_query('SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM tb_caixa ORDER BY date', con)
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
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM tb_caixa'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    averageQuebra = np.average(resultQuebraCaixa['quebra_caixa'])
    return toCurrency(averageQuebra)

def avgQuebraCaixaQuandoTem():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM tb_caixa WHERE quebra_caixa != 0'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    return toCurrency(np.average(resultQuebraCaixa['quebra_caixa']))

def avgQuebraCaixaSobra():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM tb_caixa WHERE quebra_caixa > 0'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    averageQuebra = np.average(resultQuebraCaixa['quebra_caixa'])
    return toCurrency(averageQuebra)

def avgQuebraCaixaFalta():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM tb_caixa WHERE quebra_caixa < 0'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    averageQuebra = np.average(resultQuebraCaixa['quebra_caixa'])
    return toCurrency(averageQuebra)

def avgVendasComQuebra():
    consultaTotalVendas = 'SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM tb_caixa WHERE quebra_caixa != 0 ORDER BY date'
    resultTotalVendas = pd.read_sql_query(consultaTotalVendas, con)
    resultTotalVendas['Total'] = resultTotalVendas.loc[0:resultTotalVendas.shape[0], ['vendas_dinheiro', 'vendas_cc', 'vendas_cd', 'vendas_pix', 'vendas_ifood']].sum(axis = 1)
    resultTotalVendasLimpo = resultTotalVendas.drop(resultTotalVendas.columns[[0, 1, 2, 3, 4, 5]], axis = 1)
    averageTotal = np.average(resultTotalVendasLimpo['Total'])
    return toCurrency(averageTotal)

def avgVendas():
    consultaTotalVendas = 'SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM tb_caixa ORDER BY date'
    resultTotalVendas = pd.read_sql_query(consultaTotalVendas, con)
    for linha in resultTotalVendas.index:
        resultTotalVendas.loc[linha,'Total'] = resultTotalVendas.loc[linha,'vendas_dinheiro'] + resultTotalVendas.loc[linha,'vendas_cc'] + resultTotalVendas.loc[linha,'vendas_cd'] + resultTotalVendas.loc[linha,'vendas_pix'] + resultTotalVendas.loc[linha,'vendas_ifood']
    resultTotalVendasLimpo = resultTotalVendas.drop(resultTotalVendas.columns[[0, 1, 2, 3, 4, 5]], axis = 1)
    averageVendas = np.average(resultTotalVendasLimpo['Total'])
    return toCurrency(averageVendas)

def percentQuebra():
    consultaQuebraCaixaTotal = 'SELECT quebra_caixa FROM tb_caixa'
    consultaQuebraCaixaExclusivo = 'SELECT quebra_caixa FROM tb_caixa WHERE quebra_caixa != 0'
    resultTotal = pd.read_sql_query(consultaQuebraCaixaTotal, con)
    resultExclusivo = pd.read_sql_query(consultaQuebraCaixaExclusivo, con)
    percentual = (resultExclusivo.shape[0] / resultTotal.shape[0]) * 100
    percentual = '{:.2f}'.format(percentual)
    return (percentual + '%')

def avgVendasComQuebraEx():
    consultaTotalVendas = 'SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM tb_caixa WHERE quebra_caixa > 100 OR quebra_caixa < -100 ORDER BY date'
    resultTotalVendas = pd.read_sql_query(consultaTotalVendas, con)
    resultTotalVendas['Total'] = resultTotalVendas.loc[0:resultTotalVendas.shape[0], ['vendas_dinheiro', 'vendas_cc', 'vendas_cd', 'vendas_pix', 'vendas_ifood']].sum(axis = 1)
    resultTotalVendasLimpo = resultTotalVendas.drop(resultTotalVendas.columns[[0, 1, 2, 3, 4, 5]], axis = 1)
    averageTotal = np.average(resultTotalVendasLimpo['Total'])
    return toCurrency(averageTotal)

def percentQuebraEx():
    consultaQuebraCaixaTotal = 'SELECT quebra_caixa FROM tb_caixa'
    consultaQuebraCaixaExclusivo = 'SELECT quebra_caixa FROM tb_caixa WHERE quebra_caixa > 100 OR quebra_caixa < -100'
    resultTotal = pd.read_sql_query(consultaQuebraCaixaTotal, con)
    resultExclusivo = pd.read_sql_query(consultaQuebraCaixaExclusivo, con)
    percentual = (resultExclusivo.shape[0] / resultTotal.shape[0]) * 100
    percentual = '{:.2f}'.format(percentual)
    return (percentual + '%')

def replaceCommaToDot(input):
    output = input.replace(',', '.')
    return output

def prepareInputData(input):
    regExpressionF2 = re.compile(r'\d{1,}\.\d{2}\Z')
    regExpressionF1 = re.compile(r'\d{1,}\.\d{1}\Z')
    regExpressionF0 = re.compile(r'\d{1,}\Z')
    output = []
    input = replaceCommaToDot(input)
    if regExpressionF2.match(input):
        input = removeDot(input)
        output.append(input)
        output.append(True)
        return output
    elif regExpressionF1.match(input):
        input = removeDot(input)
        input += '0'
        output.append(input)
        output.append(True)
        return output
    elif regExpressionF0.match(input):
        input = removeDot(input)
        input += '00'
        output.append(input)
        output.append(True)
        return output
    elif input == '':
        input = '0'
        output.append(input)
        output.append(True)
        return output
    else:
        print('Número não é valido. Favor digitar nesta formatação xxx,xx ou xxx.xx')
        output.append('')
        output.append(False)
        return output
        
def removeDot(input):
    output = input.replace('.', '')
    output = output.replace(',', '')
    return output

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
            print("Incorrect data format, should be DD/MM/YYYY")

    while True:
        aberturaCaixa = input('Valor de abertura: ')
        resultado = prepareInputData(aberturaCaixa)
        if resultado[1]:
            aberturaCaixa = resultado[0]
            break

    while True:
        vendasDinheiroCaixa = input('Vendas em dinheiro: ')
        resultado = prepareInputData(vendasDinheiroCaixa)
        if resultado[1]:
            vendasDinheiroCaixa = resultado[0]
            break


    while True:
        vendasCartaoCredCaixa = input('Vendas em cartão crédito: ')
        resultado = prepareInputData(vendasCartaoCredCaixa)
        if resultado[1]:
            vendasCartaoCredCaixa = resultado[0]
            break
        
    while True:
        vendasCartaoDebCaixa = input('Vendas em cartão debito: ')
        resultado = prepareInputData(vendasCartaoDebCaixa)
        if resultado[1]:
            vendasCartaoDebCaixa = resultado[0]
            break
        

    while True:
        vendasPixCaixa = input('Vendas em pix: ')
        resultado = prepareInputData(vendasPixCaixa)
        if resultado[1]:
            vendasPixCaixa = resultado[0]
            break
        

    while True:
        vendasIfoodCaixa = input('Vendas em ifood: ')
        resultado = prepareInputData(vendasIfoodCaixa)
        if resultado[1]:
            vendasIfoodCaixa = resultado[0]
            break
        

    while True:
        sangriaCaixa = input('Sangria: ')
        resultado = prepareInputData(sangriaCaixa)
        if resultado[1]:
            sangriaCaixa = resultado[0]
            break
        

    while True:
        suprimentoCaixa = input('Suprimento: ')
        resultado = prepareInputData(suprimentoCaixa)
        if resultado[1]:
            suprimentoCaixa = resultado[0]
            break
        

    subTotalCaixa = str(int(aberturaCaixa) + int(vendasDinheiroCaixa) - int(sangriaCaixa) + int(suprimentoCaixa))

    while True:
        fechamentoCaixa = input('Fechamento: ')
        resultado = prepareInputData(fechamentoCaixa)
        if resultado[1]:
            fechamentoCaixa = resultado[0]
            break
        


    quebraCaixa = str(int(fechamentoCaixa) - int(subTotalCaixa))

    clearConsole()
    print('Data: %s' % (dataCaixa))
    print('%s Abertura' % (toCurrency(aberturaCaixa)))
    print('%s Vendas - Dinheiro' % (toCurrency(vendasDinheiroCaixa)))
    print('%s Sangria' % (toCurrency(sangriaCaixa)))
    print('%s Suprimento' % (toCurrency(suprimentoCaixa)))
    print('%s SubTotal' % (toCurrency(subTotalCaixa)))
    print('%s Fechamento' % (toCurrency(fechamentoCaixa)))
    print('%s Quebra de Caixa' % (toCurrency(quebraCaixa)))
    print('Cartão Débito %s' % (toCurrency(vendasCartaoDebCaixa)))
    print('Cartão Crédito %s' % (toCurrency(vendasCartaoCredCaixa)))
    print('Pix %s' % (toCurrency(vendasPixCaixa)))
    print('iFood %s' % (toCurrency(vendasIfoodCaixa)))

    while True:
        confirm = input('Confirma os valores? (Y/N) ')
        if confirm == 'y':
            dataCaixa = convertDtFormat(dataCaixa)
            caixaInsert(dataCaixa, aberturaCaixa, vendasDinheiroCaixa, vendasCartaoCredCaixa, vendasCartaoDebCaixa, vendasPixCaixa, vendasIfoodCaixa, sangriaCaixa, suprimentoCaixa, subTotalCaixa, fechamentoCaixa, quebraCaixa)
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


def insertCaixaWithPdf():
    listaArquivos = glob.glob('Incluir/*.pdf')

    for file in listaArquivos:
        with pdfplumber.open(file) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()

        if text:
            os.remove(file)


        dateCaixaRe = re.compile(r'\w{4} \w{2} \w{5}[:] (.*)')
        aberturaCaixaRe = re.compile(r'(\d{0,3}[.]{0,}\d{1,3}[,]\d{2})\D{2} \b[A]\w{7}\b')
        vendasDinheiroRe = re.compile(r'\b[A-Z]{8}\b (\d{0,3}[.]{0,}\d{1,3}[,]\d{2})')
        vendasCcRe = re.compile(r'\b[A-Z]{6} [A-Z]{7}\b (\d{0,3}[.]{0,}\d{1,3}[,]\d{2})')
        vendasCdRe = re.compile(r'\b[A-Z]{6} [A-Z]{6}\b (\d{0,3}[.]{0,}\d{1,3}[,]\d{2})')
        vendasPixRe = re.compile(r'\b[A-Z]{3}\b (\d{0,3}[.]{0,}\d{1,3}[,]\d{2})')
        vendasIfoodRe = re.compile(r'\b[I][A-Z]{4}\b (\d{0,3}[.]{0,}\d{1,3}[,]\d{2})')
        sangriaCaixaRe = re.compile(r'(\d{0,3}[.]{0,}\d{1,3}[,]\d{2})\D{2} \b[S]\w{6}\b')
        suprimentoCaixaRe = re.compile(r'(\d{0,3}[.]{0,}\d{1,3}[,]\d{2})\D{2} \b[S]\w{9}\b')
        fechamentoCaixaRe = re.compile(r'(\d{0,3}[.]{0,}\d{1,3}[,]\d{2})\D{2} [F]\w{9}')

        listaValores = {'data' : '',\
            'abertura' : '0',\
            'vendasDinheiro' : '0',\
            'vendasCc' : '0',\
            'vendasCd' : '0',\
            'vendasPix' : '0',\
            'vendasIfood' : '0',\
            'sangria' : '0',\
            'suprimento' : '0',\
            'fechamento' : '0'}
        for line in text.split('\n'):
            if dateCaixaRe.search(line):
                listaValores['data'] = dateCaixaRe.search(line).group(1)
            if aberturaCaixaRe.search(line):
                listaValores['abertura'] = aberturaCaixaRe.search(line).group(1)
            if vendasDinheiroRe.search(line):
                listaValores['vendasDinheiro'] = vendasDinheiroRe.search(line).group(1)
            if vendasCcRe.search(line):
                listaValores['vendasCc'] = vendasCcRe.search(line).group(1)
            if vendasCdRe.search(line):
                listaValores['vendasCd'] = vendasCdRe.search(line).group(1)
            if vendasPixRe.search(line):
                listaValores['vendasPix'] = vendasPixRe.search(line).group(1)
            if vendasIfoodRe.search(line):
                listaValores['vendasIfood'] = vendasIfoodRe.search(line).group(1)
            if sangriaCaixaRe.search(line):
                listaValores['sangria'] = sangriaCaixaRe.search(line).group(1)
            if suprimentoCaixaRe.search(line):
                listaValores['suprimento'] = suprimentoCaixaRe.search(line).group(1)
            if fechamentoCaixaRe.search(line):
                listaValores['fechamento'] = fechamentoCaixaRe.search(line).group(1)
    
        listaValores['data'] = convertDtFormat(listaValores['data'])
        listaValores['abertura'] = removeDot(listaValores['abertura'])
        listaValores['vendasDinheiro'] = removeDot(listaValores['vendasDinheiro'])
        listaValores['vendasCc'] = removeDot(listaValores['vendasCc'])
        listaValores['vendasCd'] = removeDot(listaValores['vendasCd'])
        listaValores['vendasPix'] = removeDot(listaValores['vendasPix'])
        listaValores['vendasIfood'] = removeDot(listaValores['vendasIfood'])
        listaValores['sangria'] = removeDot(listaValores['sangria'])
        listaValores['suprimento'] = removeDot(listaValores['suprimento'])
        subtotal = str(int(listaValores['abertura']) + int(listaValores['vendasDinheiro']) - int(listaValores['sangria']) + int(listaValores['suprimento']))
        listaValores['fechamento'] = removeDot(listaValores['fechamento'])
        quebraCaixa = str(int(listaValores['fechamento']) - int(subtotal))
        caixaInsert(listaValores['data'], listaValores['abertura'], listaValores['vendasDinheiro'], listaValores['vendasCc'], listaValores['vendasCd'], listaValores['vendasPix'], listaValores['vendasIfood'], listaValores['sangria'], listaValores['suprimento'], subtotal, listaValores['fechamento'], quebraCaixa)


def main():
    while True:
        clearConsole()
        print('1: Registro de caixa')
        print('2: Registro de caixa com arquivos')
        print('3: Dias com quebra de caixa')
        print('4: Vendas por dia')
        print('5: Estatísticas')
        print('6: Sair')
        
        try:
            option = int(input('Opção desejada: '))
        except:
            option = ''

        if option == 1:
            clearConsole()
            registroCaixa()
        elif option == 2:
            clearConsole()
            insertCaixaWithPdf()
        elif option == 3:
            clearConsole()
            readQuebraCaixa()
        elif option == 4:
            clearConsole()
            readTotalVendas()
        elif option == 5:
            printStatistics()
        elif option == 6:
            break
        else:
            print('opção inexistente')

    input('Pressione ENTER para sair')
    con.close()

if __name__ == '__main__':
    main()