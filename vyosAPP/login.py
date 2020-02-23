import functools
from .vyCNTRL import RouterMGMT, vyos
import pexpect

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('/authlog', methods=('GET', 'POST'))
def auth():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		error_state = False
		user = 1
		e = None
 
		try:
			vyos = RouterMGMT(username, password)
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
