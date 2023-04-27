from tkinter import *
import CaixaInsert
import Estatisticas
import Miscelaneous as misc
import QuebraCaixa
import TotalVendas
import CaixaDelete
import Graficos

def menu():
    root = Tk()

    #Labels
    #Label(root, width=30, anchor='w',text="Registro de Caixa").grid(row = 0,column = 1)
    #Label(root, width=30, anchor='w',text="Dias com Quebra de caixa").grid(row = 1, column = 1)
    #Label(root, width=30, anchor='w',text="Vendas por Dia").grid(row = 2, column = 1)
    #Label(root, width=30, anchor='w',text="Estatísticas").grid(row = 3, column = 1)
    #Label(root, width=30, anchor='w',text="Remover Registro").grid(row = 4, column = 1)
    #Label(root, width=30, anchor='w',text="Gráficos").grid(row = 5, column = 1)

    #Text input
    #Entry(root, width=50, borderwidth=5).grid(row = 0, column=1)
    #Entry(root, width=50, borderwidth=5).grid(row = 1, column=1)

    def caixaManual():
        CaixaInsert.registroCaixa()

    def caixaArquivo():
        CaixaInsert.insertCaixaWithPdf()

    def vendasDia():
        print(TotalVendas.ifFilter().to_markdown())

    def quebraCaixa():
        QuebraCaixa.ifFilter()

    def estatisticas():
        Estatisticas.printStatistics()

    def deleteCaixa():
        CaixaDelete.removeData()
    
    def graficos():
        Graficos.vendas_por_dia()

    def insertCaixa():
        windowInsert = Tk()
        Button(windowInsert, width=15, text='Manual', command=caixaManual).grid(row=0, column=0, padx=10)
        Button(windowInsert, width=15, text='Arquivos', command=caixaArquivo).grid(row=0, column=1, padx=10)

    #Button
    Button(root, width=15, text="Registro de caixa", command = insertCaixa).grid(row=0, column=0, padx = 2, pady = 2)
    Button(root, width=15, text="Quebra de caixa", command=quebraCaixa).grid(row=1, column=0, padx = 2, pady = 2)
    Button(root, width=15, text="Vendas por dia", command=vendasDia).grid(row=2, column=0, padx = 2, pady = 2)
    Button(root, width=15, text="Estatísticas", command=estatisticas).grid(row=3, column=0, padx = 2, pady = 2)
    Button(root, width=15, text="Remover Registro", command=deleteCaixa).grid(row=4, column=0, padx = 2, pady = 2)
    Button(root, width=15, text="Graficos", command=graficos).grid(row=5, column=0, padx = 2, pady = 2)
    Button(root, width=15, text="Sair", command=root.quit).grid(row=6, column=0, padx = 2, pady = 10)

    root.mainloop()