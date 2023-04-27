import pandas as pd
import numpy as np
import Connectdb
import Miscelaneous as misc

con = Connectdb.connectdb.con

#função para pegar a media das quebras de caixa
def avgQuebraCaixa():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM tb_caixa'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    averageQuebra = np.average(resultQuebraCaixa['quebra_caixa'])
    return misc.toCurrency(averageQuebra)

def avgQuebraCaixaQuandoTem():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM tb_caixa WHERE quebra_caixa != 0'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    return misc.toCurrency(np.average(resultQuebraCaixa['quebra_caixa']))

def avgQuebraCaixaSobra():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM tb_caixa WHERE quebra_caixa > 0'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    averageQuebra = np.average(resultQuebraCaixa['quebra_caixa'])
    return misc.toCurrency(averageQuebra)

def avgQuebraCaixaFalta():
    consultaQuebraCaixa = 'SELECT quebra_caixa FROM tb_caixa WHERE quebra_caixa < 0'
    resultQuebraCaixa = pd.read_sql_query(consultaQuebraCaixa, con)
    averageQuebra = np.average(resultQuebraCaixa['quebra_caixa'])
    return misc.toCurrency(averageQuebra)

def avgVendasComQuebra():
    consultaTotalVendas = 'SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM tb_caixa WHERE quebra_caixa != 0 ORDER BY date'
    resultTotalVendas = pd.read_sql_query(consultaTotalVendas, con)
    resultTotalVendas['Total'] = resultTotalVendas.loc[0:resultTotalVendas.shape[0], ['vendas_dinheiro', 'vendas_cc', 'vendas_cd', 'vendas_pix', 'vendas_ifood']].sum(axis = 1)
    resultTotalVendasLimpo = resultTotalVendas.drop(resultTotalVendas.columns[[0, 1, 2, 3, 4, 5]], axis = 1)
    averageTotal = np.average(resultTotalVendasLimpo['Total'])
    return misc.toCurrency(averageTotal)

def avgVendas():
    consultaTotalVendas = 'SELECT date as Data, vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM tb_caixa ORDER BY date'
    resultTotalVendas = pd.read_sql_query(consultaTotalVendas, con)
    for linha in resultTotalVendas.index:
        resultTotalVendas.loc[linha,'Total'] = resultTotalVendas.loc[linha,'vendas_dinheiro'] + resultTotalVendas.loc[linha,'vendas_cc'] + resultTotalVendas.loc[linha,'vendas_cd'] + resultTotalVendas.loc[linha,'vendas_pix'] + resultTotalVendas.loc[linha,'vendas_ifood']
    resultTotalVendasLimpo = resultTotalVendas.drop(resultTotalVendas.columns[[0, 1, 2, 3, 4, 5]], axis = 1)
    averageVendas = np.average(resultTotalVendasLimpo['Total'])
    return misc.toCurrency(averageVendas)

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
    return misc.toCurrency(averageTotal)

def percentQuebraEx():
    consultaQuebraCaixaTotal = 'SELECT quebra_caixa FROM tb_caixa'
    consultaQuebraCaixaExclusivo = 'SELECT quebra_caixa FROM tb_caixa WHERE quebra_caixa > 100 OR quebra_caixa < -100'
    resultTotal = pd.read_sql_query(consultaQuebraCaixaTotal, con)
    resultExclusivo = pd.read_sql_query(consultaQuebraCaixaExclusivo, con)
    percentual = (resultExclusivo.shape[0] / resultTotal.shape[0]) * 100
    percentual = '{:.2f}'.format(percentual)
    return (percentual + '%')

def totalVendas():
    resultTotalVendas = pd.read_sql_query('SELECT vendas_dinheiro, vendas_cc, vendas_cd, vendas_pix, vendas_ifood FROM tb_caixa ORDER BY date', con)
    resultTotalVendas['Total'] = resultTotalVendas.loc[0:resultTotalVendas.shape[0], ['vendas_dinheiro', 'vendas_cc', 'vendas_cd', 'vendas_pix', 'vendas_ifood']].sum(axis = 1)
    total = resultTotalVendas['Total'].sum()
    return misc.toCurrency(total)

def printStatistics():
    print('Média de vendas por dia: %s' %(avgVendas()))
    print('Total de vendas: %s' %(totalVendas()))
    print('-'*100)
    print('Quebras')
    print('Média das Quebras de caixa (total): %s                               Média de Sobra: %s' %(avgQuebraCaixa(), avgQuebraCaixaSobra()))
    print('Média das Quebras de caixa (quando há quebra): %s                    Média de Falta: %s' %(avgQuebraCaixaQuandoTem(), avgQuebraCaixaFalta()))
    print('Média do Total de vendas nos dias com Quebra de caixa: %s        Porcentagem de dias com Quebra de Caixa: %s' %(avgVendasComQuebra(), percentQuebra()))
    print('M. do T. de v. nos dias com Q. de c. maior que R$1,00: %s        Porc. de dia com Q. de c. maior que R$1,00: %s' %(avgVendasComQuebraEx(), percentQuebraEx()))
    input()
    misc.clearConsole()
