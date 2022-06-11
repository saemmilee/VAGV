import pymysql

class Database():
    def __init__(self):
        self.db= pymysql.connect(host='192.168.137.77', #localhost
                                  user='root',
                                  password='root',
                                  db='flask_db',
                                  charset='utf8')
        self.cursor= self.db.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        self.db.commit()

    def executeOne(self, query):
        self.cursor.execute(query)
        row= self.cursor.fetchone()
        return row

    def executeAll(self, query):
        self.cursor.execute(query)
        row= self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
        
    def close(self):
        self.db.close()
