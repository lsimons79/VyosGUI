import functools
import vymgmt
import pexpect

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('/authlog', methods=('GET', 'POST'))
def auth():
	vyos = None
	if request.method == 'POST':
		user_name = request.form['username']
		user_pass = request.form['password']
		vyos = vymgmt.Router('127.0.0.1', user_name, password=user_pass, port=22)
		error_state = False
		user = 1
		e = None
 
		try:
			vyos.login()
		except pexpect.pxssh.ExceptionPxssh as e:
			error_state = True
			error = str(e)
			return error

		if error_state is False:
			session.clear()
			session['user_id'] = user
			return redirect(url_for('hello'))

		e = error
		flash(e) 

	return render_template('auth.html')

@bp.before_app_request
def check_login_status():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = 'vyos'

@bp.route('/logout')
def logout(vyos):
	session.clear()
	vyos.logout()
	return redirect(url_for('auth'))

def check_user_login():
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth'))

		return view(**kwargs)
	
	return wrapped_view
