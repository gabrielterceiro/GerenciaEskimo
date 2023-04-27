import sqlite3

class connectdb:
    #conectando no banco de dados
    con = sqlite3.connect('.\caixadb.db')