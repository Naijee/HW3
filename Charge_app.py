import Charge
from jinja2 import Environment, PackageLoader
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)

app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'
get = Environment(loader=PackageLoader(__name__, 'templates')).get_template

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (username, password) in [('Alice', 'aaaa'), ('Bob', 'bbbb')]:
            response = redirect(url_for('index'))
            response.set_cookie('username', username)
            return response
    return get('login.html').render(username=username)

@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.set_cookie('username', '')
    return response

@app.route('/')
def index():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login'))
    spendings = Charge.get_spendings_of(Charge.open_database(), username)
    return get('index2.html').render(spendings=spendings, username=username,
        flash_messages=request.args.getlist('flash'))

@app.route('/add_cost', methods=['GET', 'POST'])
def add_cost():
	username = request.cookies.get('username')
	if not username:
		return redirect(url_for('login'))
    #account = request.form.get('account', '').strip()
	dollars = request.form.get('dollars', '').strip()
	Payments = request.form.get('Payments', '').strip()
	memo = request.form.get('memo', '').strip()
	complaint = None
	if request.method == 'POST':
		if dollars and dollars.isdigit() and memo:
			db = Charge.open_database()
			Charge.add_spending(db, username, dollars,Payments , memo)
			db.commit()
			return redirect(url_for('index', flash='Payment successful'))
		complaint = ('Dollars must be an integer' if not dollars.isdigit()
                     else 'Please fill in all three fields')
	return get('add_cost.html').render(complaint=complaint,dollars=dollars, memo=memo , Payments = Payments)
	


if __name__ == '__main__':
    app.debug = True
    app.run('192.168.5.1', debug=True, port=8100,ssl_context='adhoc')