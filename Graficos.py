import TotalVendas
import pandas as pd
from matplotlib import pyplot as plt
import Miscelaneous as misc

plt.rcParams["figure.figsize"] = [10, 6]

def vendas_por_dia():
    df = TotalVendas.ifFilter()
    df['Vendas'] = df['Vendas'].map(lambda x: (misc.currency_to_number(x))/100)
    df.drop(df.tail(1).index, inplace=True)
    ax = df.plot(x = 'Data', y = 'Vendas', linewidth=2.0, kind = 'bar')
    plt.show()