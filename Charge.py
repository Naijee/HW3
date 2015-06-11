import os, pprint, sqlite3
from collections import namedtuple

def open_database(path='Charge.db'):
	new = not os.path.exists(path)
	db = sqlite3.connect(path)
	if new:
		c = db.cursor()
		c.execute('CREATE TABLE spending (id INTEGER PRIMARY KEY, user TEXT, dollars INTEGER,Payments TEXT, memo TEXT)')
		add_spending(db, 'Alice', 10000 ,'Income', 'Surplus')
		add_spending(db, 'Bob', 10000 , 'Income','Surplus')
		db.commit()
	return db

def add_spending(db, user,dollars,payments, memo):
    db.cursor().execute('INSERT INTO spending (user, dollars, Payments, memo)'
                        ' VALUES (?, ?, ?, ?)', (user, dollars, payments, memo))
						
def del_spending(db, id):
    db.cursor().execute('DELETE FROM spending '
						'where id = ?;', (id,))

def update_spending(db, id):
    db.cursor().execute('UPDATE spending '
						'SET user = ? , dollars = ? , payments = ? , memo = ?  '
						'where id = ?;', (user, dollars, payments, memo , id))

def get_spendings_of(db, account):
    c = db.cursor()
    c.execute('SELECT * FROM spending WHERE user = ?'
              ' ORDER BY id', (account,))
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    return [Row(*row) for row in c.fetchall()]

#if __name__ == '__main__':
    #db = open_database()
    #pprint.pprint(get_spendings_of(db, 'brandon'))

def get_cost_of(db, id):
    c = db.cursor()
    c.execute('SELECT * FROM spending WHERE id = ?'
              ' ORDER BY id', (id,))
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    return [Row(*row) for row in c.fetchall()]