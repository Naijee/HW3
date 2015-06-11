import Charge, uuid
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)
#import flask_tlsauth as tlsauth
from OpenSSL import SSL

app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (username, password) in [('Bob', 'bbbb'), ('Alice', 'aaaa')]:
            session['username'] = username
            session['csrf_token'] = uuid.uuid4().hex
            return redirect(url_for('index'))
    return render_template('login.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    spendings = Charge.get_spendings_of(Charge.open_database(), username)
    return render_template('index2.html', spendings=spendings, username=username,
                           flash_messages=get_flashed_messages())

@app.route('/add_cost', methods=['GET', 'POST'])
def pay():
	username = session.get('username')
	if not username:
		return redirect(url_for('login'))
    #account = request.form.get('account', '').strip()
	dollars = request.form.get('dollars', '').strip()
	Payments = request.form.get('Payments', '').strip()
	memo = request.form.get('memo', '').strip()
	complaint = None
	if request.method == 'POST':
		if request.form.get('csrf_token') != session['csrf_token']:
			abort(403)
		if  dollars and dollars.isdigit() and memo:
			db = Charge.open_database()
			Charge.add_spending(db, username, dollars,Payments, memo)
			db.commit()
			#flash('Payment successful')
			return redirect(url_for('index'))
		complaint = ('Dollars must be an integer' if not dollars.isdigit()
                     else 'Please fill in all three fields')
	return render_template('add_cost.html', complaint=complaint, Payments=Payments,
                           dollars=dollars, memo=memo,
                           csrf_token=session['csrf_token'])

@app.route('/edit_cost/<id>', methods=['GET', 'POST'])
def Edit(id=id):
	username = session.get('username')
	if not username:
		return redirect(url_for('login'))
	Cost = Charge.get_cost_of(Charge.open_database(), id)
	dollars = request.form.get('dollars', '').strip()
	Payments = request.form.get('Payments', '').strip()
	memo = request.form.get('memo', '').strip()
	if request.method == 'POST':
		if request.form.get('csrf_token') != session['csrf_token']:
			abort(403)
		if  dollars and dollars.isdigit() and memo:
			db = Charge.open_database()
			Charge.update_spending(db, username, dollars,Payments, memo , id)
			db.commit()
			#flash('Payment successful')
			return redirect(url_for('index'))
		complaint = ('Dollars must be an integer' if not dollars.isdigit()
						else 'Please fill in all three fields')
	#return id
	return render_template('edit_cost.html', Cost=Cost,id=id,
                           csrf_token=session['csrf_token'])
	
if __name__ == '__main__':
	app.debug = True
	context=('www.crt','www.key')
	app.run(ssl_context=context)