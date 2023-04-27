import pdfplumber
import re
import pandas as pd
import Connectdb
import datetime
import glob
import os

con = Connectdb.connectdb.con
c = con.cursor()

df_caixas = pd.read_sql_query('SELECT * FROM tb_caixinha', con)

#função para inserir dados
def sales_insert(dt_sale, cd_prod, qt_prod, vl_prod):
    try:
        c.execute('INSERT INTO tb_venda (dt_venda, cd_prod, qt_prod, vl_prod) values(?, ?, ?, ?)', (dt_sale, cd_prod, qt_prod, vl_prod))
    except Exception as e:
        input(e)

    con.commit()

list_arquivos = glob.glob('Incluir/RelatoriosVendas/*.pdf')
for file in list_arquivos:
    print(f'Importandos dados do arquivo: {file}')
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    
    if text:
        print(f'Removendo arquivo {file}')
        os.remove(file)

    new_dt_re = re.compile(r'^([D][at]{3}) (.*)') 
    new_sale_re = re.compile(r'\d+ [\w\s]+ (\d+) (.*) ([\d,]+\d{2}) [0] ([\d,]+\d{2})')

    lst_sale = []

    for line in text.split('\n'):
        if new_dt_re.match(line):
            dt_string, dt_sales = line.split()
            dt_sales = int(datetime.datetime.timestamp(datetime.datetime.strptime(dt_sales, '%d/%m/%Y')))

        line = new_sale_re.search(line)
        if line:
            cd_prod = line.group(1)
            qt_prod = line.group(3)[:-3]
            vl_prod = int(line.group(4).replace(',', ''))
            if int(cd_prod) in df_caixas['cd_caixinha'].to_list():
                cd_prod = int(df_caixas.loc[df_caixas['cd_caixinha'] == int(cd_prod)]['cd_picole'])
                qt_prod = int(df_caixas.loc[df_caixas['cd_picole'] == int(cd_prod)]['qt_picole']) * int(qt_prod)
            lst_sale.append([dt_sales, cd_prod, qt_prod, vl_prod])

    df_vendas = pd.DataFrame(lst_sale, columns=['dt_venda', 'cd_prod', 'qt_prod', 'vl_prod'])
    df_vendas.to_sql('tb_venda', con, if_exists='append', index=False)