import CaixaInsert
import Estatisticas
import Miscelaneous as misc
import QuebraCaixa
import TotalVendas
import CaixaDelete


def main():
    while True:
        misc.clearConsole()
        print('1: Registro de caixa')
        print('2: Registro de caixa com arquivos')
        print('3: Dias com quebra de caixa')
        print('4: Vendas por dia')
        print('5: Estatísticas')
        print('6: Remover Registro')
        print('7: Sair')
        
        try:
            option = int(input('Opção desejada: '))
        except:
            option = ''

        if option == 1:
            misc.clearConsole()
            CaixaInsert.registroCaixa()
        elif option == 2:
            misc.clearConsole()
            CaixaInsert.insertCaixaWithPdf()
        elif option == 3:
            misc.clearConsole()
            QuebraCaixa.ifFilter()
        elif option == 4:
            misc.clearConsole()
            TotalVendas.ifFilter()
        elif option == 5:
            misc.clearConsole()
            Estatisticas.printStatistics()
        elif option == 6:
            misc.clearConsole()
            CaixaDelete.removeData()
        elif option == 7:
            break
        else:
            print('opção inexistente')

    input('Pressione ENTER para sair')

if __name__ == '__main__':
    main()