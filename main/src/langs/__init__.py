import sqlite3

class Lang:
    def __init__(self, code):
        self.code = code

    def get_vocab(self, for_lang='eng'):
        con = sqlite3.connect('data/langs.sqlite')
        cur = con.cursor()
        vocabs = [{'w': a[0], 't': a[1]} for a in cur.execute('SELECT ' + self.code + ', ' + for_lang + ' FROM ' + self.code + ';')]
        con.close()
        return vocabs