import functools
from .vyCNTRL import RouterMGMT, vyos 
import pexpect

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

bp = Blueprint('system', __name__, url_prefix='/system')

@bp.route('/settings', methods=('GET', 'POST'))
def settings():
	if request.method == 'POST':
		hostname = request.form['hostname']
		name_server = request.form['dns']
		gateway_address = request.form['gateway']
 
		try:
			vyos.
		except pexpect.pxssh.ExceptionPxssh as e:
			error_state = True
			error = str(e)
			return error

		if error_state is False:
			session.clear()
			session['user_id'] = user
			return redirect(url_for('system'))

		e = error
		flash(e) 

	return render_template('system.html')
