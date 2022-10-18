import os
import datetime

def toCurrency(value):
    value = float(value)
    value /= 100
    if value >= 0:
        currency = 'R${:,.2f}'.format(value)
    else:
        currency = '-R${:,.2f}'.format(value*-1)
    return currency

def replaceCommaToDot(input):
    output = input.replace(',', '.')
    return output

def removeDot(input):
    output = input.replace('.', '')
    output = output.replace(',', '')
    return output

#função paa converter data dd/mm/yyyy para yyyy-mm-dd
def convertDtFormat(unformattedDt):
    '''day = unformattedDt[0] + unformattedDt[1]
    month = unformattedDt[3] + unformattedDt[4]
    year = unformattedDt[6] + unformattedDt[7] + unformattedDt[8] + unformattedDt[9]
    formattedDt = datetime.datetime(int(year), int(month), int(day))'''
    formattedDt = datetime.datetime.strptime(unformattedDt, '%d/%m/%Y')
    
    return formattedDt

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')