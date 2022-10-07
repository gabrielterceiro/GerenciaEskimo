import sqlite3
import datetime

#conectando no banco de dados
con = sqlite3.connect('caixadb.db')

#criando um cursos
c = con.cursor()

#função para inserir dados
def dataInsert(vDate, vAbertura, vVendas_dinheiro, vVendas_cc, vVendas_cd, vVendas_pix, vVendas_ifood, vSangria, vSuprimento, vSub_total, vFechamento, vQuebra_caixa):
    c.execute('INSERT INTO caixa_tb (date, abertura, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood, sangria, suprimento, sub_total, fechamento, quebra_caixa) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (vDate, vAbertura, vVendas_dinheiro, vVendas_cc, vVendas_cd, vVendas_pix, vVendas_ifood, vSangria, vSuprimento, vSub_total, vFechamento, vQuebra_caixa))
    con.commit()

#funcão para ler dados
def dataRead():
    c.execute('SELECT * from caixa_tb')
    for linha in c.fetchall():
        print(linha)

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
    try:
        val = float(aberturaCaixa)
        break;
    except ValueError:
        print('This is not a valid number. Please enter a valid number.')

while True:
    vendasDinheiroCaixa = input('Vendas em dinheiro: ')
    try:
        val = float(vendasDinheiroCaixa)
        break;
    except ValueError:
        print('This is not a valid number. Please enter a valid number.')

while True:
    vendasCartaoCredCaixa = input('Vendas em cartão crédito: ')
    try:
        val = float(vendasCartaoCredCaixa)
        break;
    except ValueError:
        print('This is not a valid number. Please enter a valid number.')

while True:
    vendasCartaoDebCaixa = input('Vendas em cartão debito: ')
    try:
        val = float(vendasCartaoDebCaixa)
        break;
    except ValueError:
        print('This is not a valid number. Please enter a valid number.')

while True:
    vendasPixCaixa = input('Vendas em pix: ')
    try:
        val = float(vendasPixCaixa)
        break;
    except ValueError:
        print('This is not a valid number. Please enter a valid number.')

while True:
    vendasIfoodCaixa = input('Vendas em ifood: ')
    try:
        val = float(vendasIfoodCaixa)
        break;
    except ValueError:
        print('This is not a valid number. Please enter a valid number.')

while True:
    sangriaCaixa = input('Sangria: ')
    try:
        val = float(sangriaCaixa)
        break;
    except ValueError:
        print('This is not a valid number. Please enter a valid number.')

while True:
    suprimentoCaixa = input('Suprimento: ')
    try:
        val = float(suprimentoCaixa)
        break;
    except ValueError:
        print('This is not a valid number. Please enter a valid number.')

subTotalCaixa = float(aberturaCaixa) + float(vendasDinheiroCaixa) - float(sangriaCaixa) + float(suprimentoCaixa)

while True:
    fechamentoCaixa = input('Fechamento: ')
    try:
        val = float(fechamentoCaixa)
        break;
    except ValueError:
        print('This is not a valid number. Please enter a valid number.')

quebraCaixa = float(subTotalCaixa) - float(fechamentoCaixa)

dataInsert(dataCaixa, aberturaCaixa, vendasDinheiroCaixa, vendasCartaoCredCaixa, vendasCartaoDebCaixa, vendasPixCaixa, vendasIfoodCaixa, sangriaCaixa, suprimentoCaixa, subTotalCaixa, fechamentoCaixa, quebraCaixa)
dataRead()
