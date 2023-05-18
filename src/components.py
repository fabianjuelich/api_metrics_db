import requests_html
import sqlite3

class Components:
    
    def __init__(self):
        self.session = requests_html.HTMLSession()
        self.database = Database()

    def get_symbols(self, index):
        self.response = self.session.get(f'https://finance.yahoo.com/quote/%5E{index}/components')
        self.components = self.response.html.find('table.W\(100\%\) > tbody:nth-child(2)')[0].text.split(chr(0x0A))
        self.number_columns = len(self.database.cursor.execute('PRAGMA table_info(components)').fetchall())
        self.number_rows = int(len(self.components)/self.number_columns)

        i = 0
        rows = []
        for row in range(self.number_rows):
            tmp = []
            for column in range(self.number_columns):
                tmp.append(self.components[i])
                i+=1
            rows.append(tmp)
        self.database.insert_db(rows)

        components_list = self.database.cursor.execute('SELECT symbol FROM components').fetchall()
        return [component[0] for component in components_list]

class Database:

    def __init__(self):
        self.connection = sqlite3.connect(':memory:')    
        self.cursor = self.connection.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute('''
        CREATE TABLE components (
            symbol TEXT PRIMARY KEY,
            company_name TEXT,
            last_price REAL,
            change REAL,
            percentage_change REAL,
            volume REAL
        )
        ''')

    def insert_db(self, rows):
        self.cursor.executemany('''
        INSERT INTO components VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        ''', rows)
