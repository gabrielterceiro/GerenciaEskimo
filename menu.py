import CaixaInsert
import Estatisticas
import Miscelaneous as misc
import QuebraCaixa
import TotalVendas
import CaixaDelete
import Graficos

def menu():
    while True:
            misc.clearConsole()
            print('1: Registro de caixa')
            print('2: Dias com quebra de caixa')
            print('3: Vendas por dia')
            print('4: Estatísticas')
            print('5: Remover Registro')
            print('6: Graficos')
            print('7: Sair')
            
            try:
                option = int(input('Opção desejada: '))
            except:
                option = ''

            if option == 1:
                misc.clearConsole()
                while True:
                    registerOption = input('Gostaria de Registrar caixa (M)anualmente ou com (A)rquivo?\n')
                    if registerOption == 'm' or registerOption == 'M':
                        CaixaInsert.registroCaixa()
                        break
                    elif registerOption =='a' or registerOption == 'A':
                        CaixaInsert.insertCaixaWithPdf()
                        break
                    else:
                        print('Opção inválida') 
            elif option == 2:
                misc.clearConsole()
                QuebraCaixa.ifFilter()
            elif option == 3:
                misc.clearConsole()
                print(TotalVendas.ifFilter().to_markdown())
                input()
            elif option == 4:
                misc.clearConsole()
                Estatisticas.printStatistics()
            elif option == 5:
                misc.clearConsole()
                CaixaDelete.removeData()
            elif option == 6:
                misc.clearConsole()
                Graficos.vendas_por_dia()
            elif option == 7:
                break
            else:
                print('opção inexistente')

    input('Pressione ENTER para sair')