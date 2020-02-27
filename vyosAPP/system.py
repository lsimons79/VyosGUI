import functools
from .vyCNTRL import RouterMGMT
import vymgmt

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

bp = Blueprint('system', __name__, url_prefix='/system')

@bp.route('/settings', methods=('GET', 'POST'))
def settings():
	if request.method == 'POST':
		vyos = RouterMGMT('vyos', 'vyos')
		if 'commit' in request.form:
			u_host = request.form['hostname']
			u_dns = request.form['dns']
			u_gateway = request.form['gateway']
			e = None
			error = None
 
			try:
				vyos.hostname(u_host)
				vyos.nameserver(u_dns)
				vyos.gateway(u_gateway) 
			except vymgmt.router.ConfigError as e:
				error = str(e)
				return error

			e = error
			flash(e) 

		elif 'save' in request.form:
			e = None
			error = None
			try:
				vyos.save()
			except vymgmt.router.ConfigError as e:

				error = str(e)
				return error

			e = error
			flash(e)
		
	return render_template('system.html')


@bp.route('/logout')
def logout(vyos):
	session.clear()
	vyos.logout()
	return redirect(url_for('auth'))
