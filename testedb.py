from pickle import FALSE
import sqlite3
import datetime
from turtle import shape
from unittest import result
import pandas as pd
import os
import logging
import numpy as np
from IPython.display import display
import re

con = sqlite3.connect('caixadb.db')

c = con.cursor()

tabela = pd.read_sql_query('select abertura, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood, sangria, suprimento, sub_total, fechamento, quebra_caixa FROM caixa_tb ORDER BY id', con)
display(tabela)


teste0 = re.compile(r'\d{3}\.\d{2}')
teste1 = re.compile(r'\d{2}\.\d{2}')
teste2 = re.compile(r'\d{4}\.\d{2}')
teste3 = re.compile(r'\d{3}\.\d{1}')
teste4 = re.compile(r'\d{2}\.\d{1}')
teste5 = re.compile(r'\d{4}\.\d{1}')
teste6 = re.compile(r'\d{1}\.\d{2}')
teste7 = re.compile(r'\d{1}\.\d{1}')

tabela['abertura'] = tabela['abertura'].map(lambda x: str(x))
lista_abertura = []

for line in tabela['abertura']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    lista_abertura.append(int(line))
tabela['abertura'] = lista_abertura

tabela['vendas_dinheiro'] = tabela['vendas_dinheiro'].map(lambda x: str(x))
lista_vendas_dinheiro = []

for line in tabela['vendas_dinheiro']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    lista_vendas_dinheiro.append(int(line))
tabela['vendas_dinheiro'] = lista_vendas_dinheiro

tabela['vendas_cc'] = tabela['vendas_cc'].map(lambda x: str(x))
lista_vendas_cc = []

for line in tabela['vendas_cc']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    lista_vendas_cc.append(int(line))
tabela['vendas_cc'] = lista_vendas_cc

tabela['vendas_cd'] = tabela['vendas_cd'].map(lambda x: str(x))
lista_vendas_cd = []

for line in tabela['vendas_cd']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    lista_vendas_cd.append(int(line))
tabela['vendas_cd'] = lista_vendas_cd

tabela['vendas_pix'] = tabela['vendas_pix'].map(lambda x: str(x))
lista_vendas_pix = []

for line in tabela['vendas_pix']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    lista_vendas_pix.append(int(line))
tabela['vendas_pix'] = lista_vendas_pix

tabela['vendas_ifood'] = tabela['vendas_ifood'].map(lambda x: str(x))
lista_vendas_ifood = []

for line in tabela['vendas_ifood']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    lista_vendas_ifood.append(int(line))
tabela['vendas_ifood'] = lista_vendas_ifood

tabela['sangria'] = tabela['sangria'].map(lambda x: str(x))
lista_sangria = []

for line in tabela['sangria']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    lista_sangria.append(int(line))
tabela['sangria'] = lista_sangria

tabela['suprimento'] = tabela['suprimento'].map(lambda x: str(x))
lista_suprimento = []

for line in tabela['suprimento']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    lista_suprimento.append(int(line))
tabela['suprimento'] = lista_suprimento

tabela['sub_total'] = tabela['sub_total'].map(lambda x: str(x))
lista_sub_total = []

for line in tabela['sub_total']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    lista_sub_total.append(int(line))
tabela['sub_total'] = lista_sub_total

tabela['fechamento'] = tabela['fechamento'].map(lambda x: str(x))
lista_fechamento = []

for line in tabela['fechamento']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    lista_fechamento.append(int(line))
tabela['fechamento'] = lista_fechamento

tabela['quebra_caixa'] = tabela['quebra_caixa'].map(lambda x: str(x))
lista_quebra_caixa = []

for line in tabela['quebra_caixa']:
    if teste0.match(line):
        line = line.replace('.', '')
    elif teste1.match(line):
        line = line.replace('.', '')
    elif teste2.match(line):
        line = line.replace('.', '')
    elif teste3.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste4.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste5.match(line):
        line += '0'
        line = line.replace('.', '')
    elif teste6.match(line):
        line = line.replace('.', '')
    elif teste7.match(line):
        line += '0'
        line = line.replace('.', '')
    else:
        line = '0'
    lista_quebra_caixa.append(int(line))
tabela['quebra_caixa'] = lista_quebra_caixa

tabela.to_sql('tb_caixa', con, if_exists='append', index=False)