import Miscelaneous as misc
import Connectdb
import re
import datetime
import glob
import pdfplumber
import os


con = Connectdb.connectdb.con
c = con.cursor()

#função para inserir dados
def caixaInsert(vDate, vAbertura, vVendas_dinheiro, vVendas_cc, vVendas_cd, vVendas_pix, vVendas_ifood, vSangria, vSuprimento, vSub_total, vFechamento, vQuebra_caixa):
    try:
        c.execute('INSERT INTO tb_caixa (date, abertura, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood, sangria, suprimento, sub_total, fechamento, quebra_caixa) values(strftime(\'%s\', ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (vDate, vAbertura, vVendas_dinheiro, vVendas_cc, vVendas_cd, vVendas_pix, vVendas_ifood, vSangria, vSuprimento, vSub_total, vFechamento, vQuebra_caixa))
    except:
        input()
    con.commit()

def prepareInputData(input):
    regExpressionF2 = re.compile(r'\d{1,}\.\d{2}\Z')
    regExpressionF1 = re.compile(r'\d{1,}\.\d{1}\Z')
    regExpressionF0 = re.compile(r'\d{1,}\Z')
    output = []
    input = misc.replaceCommaToDot(input)
    if regExpressionF2.match(input):
        input = misc.removeDot(input)
        output.append(input)
        output.append(True)
        return output
    elif regExpressionF1.match(input):
        input = misc.removeDot(input)
        input += '0'
        output.append(input)
        output.append(True)
        return output
    elif regExpressionF0.match(input):
        input = misc.removeDot(input)
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

    misc.clearConsole()
    print('Data: %s' % (dataCaixa))
    print('%s Abertura' % (misc.toCurrency(aberturaCaixa)))
    print('%s Vendas - Dinheiro' % (misc.toCurrency(vendasDinheiroCaixa)))
    print('%s Sangria' % (misc.toCurrency(sangriaCaixa)))
    print('%s Suprimento' % (misc.toCurrency(suprimentoCaixa)))
    print('%s SubTotal' % (misc.toCurrency(subTotalCaixa)))
    print('%s Fechamento' % (misc.toCurrency(fechamentoCaixa)))
    print('%s Quebra de Caixa' % (misc.toCurrency(quebraCaixa)))
    print('Cartão Débito %s' % (misc.toCurrency(vendasCartaoDebCaixa)))
    print('Cartão Crédito %s' % (misc.toCurrency(vendasCartaoCredCaixa)))
    print('Pix %s' % (misc.toCurrency(vendasPixCaixa)))
    print('iFood %s' % (misc.toCurrency(vendasIfoodCaixa)))

    while True:
        confirm = input('Confirma os valores? (Y/N) ')
        if confirm == 'y':
            dataCaixa = misc.convertDtFormat(dataCaixa)
            caixaInsert(dataCaixa, aberturaCaixa, vendasDinheiroCaixa, vendasCartaoCredCaixa, vendasCartaoDebCaixa, vendasPixCaixa, vendasIfoodCaixa, sangriaCaixa, suprimentoCaixa, subTotalCaixa, fechamentoCaixa, quebraCaixa)
            input('Aperte ENTER para recomeçar')
            misc.clearConsole()
            break
        if confirm == 'n':
            print('Entrada cancelada, aperte ENTER para sair')
            misc.clearConsole()
            break

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
    
        listaValores['data'] = misc.convertDtFormat(listaValores['data'])
        listaValores['abertura'] = misc.removeDot(listaValores['abertura'])
        listaValores['vendasDinheiro'] = misc.removeDot(listaValores['vendasDinheiro'])
        listaValores['vendasCc'] = misc.removeDot(listaValores['vendasCc'])
        listaValores['vendasCd'] = misc.removeDot(listaValores['vendasCd'])
        listaValores['vendasPix'] = misc.removeDot(listaValores['vendasPix'])
        listaValores['vendasIfood'] = misc.removeDot(listaValores['vendasIfood'])
        listaValores['sangria'] = misc.removeDot(listaValores['sangria'])
        listaValores['suprimento'] = misc.removeDot(listaValores['suprimento'])
        subtotal = str(int(listaValores['abertura']) + int(listaValores['vendasDinheiro']) - int(listaValores['sangria']) + int(listaValores['suprimento']))
        listaValores['fechamento'] = misc.removeDot(listaValores['fechamento'])
        quebraCaixa = str(int(listaValores['fechamento']) - int(subtotal))
        caixaInsert(listaValores['data'], listaValores['abertura'], listaValores['vendasDinheiro'], listaValores['vendasCc'], listaValores['vendasCd'], listaValores['vendasPix'], listaValores['vendasIfood'], listaValores['sangria'], listaValores['suprimento'], subtotal, listaValores['fechamento'], quebraCaixa)
