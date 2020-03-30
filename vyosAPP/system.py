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
				flash(error)
				return redirect(url_for('system.settings'))

		elif 'save' in request.form:
			e = None
			error = None
			try:
				vyos.save()
			except vymgmt.router.ConfigError as e:

				error = str(e)
				flash(error)
				return redirect(url_for('system.settings'))

	return render_template('system.html')

@bp.route('/firewall', methods=('GET', 'POST'))
def firewall():

	vyos = RouterMGMT('vyos', 'vyos')
	int = vyos.run('show interfaces ethernet')
	interface=str(int[0]).split('ethernet')[2]
	vyos.exit()


#       if request.method == 'POST':
#		vyos = RouterMGMT('vyos', 'vyos')
#		if 'commit' in request.form:
#			u_x = request.form['x']
#			u_x = request.form['x']
#			u_x = request.form['x']
#			e = None
#			error = None
#
#			try:
#				vyos.(x)
#				vyos.(x)
#				vyos.(x) 
#			except vymgmt.router.ConfigError as e:
#				error = str(e)
#				flash(error)
#				return redirect(url_for('system.settings'))

#               elif 'save' in request.form:
#			e = None
#			error = None
#			try:
#				vyos.save()
#			except vymgmt.router.ConfigError as e:

#				error = str(e)
#				flash(error)
#				return redirect(url_for('system.firewall'))
#
	return render_template('firewall.html', int=int)

@bp.route('/home')
def home():
	vyos2 = RouterMGMT('vyos', 'vyos')
	ps_hn=vyos2.run('show system host-name')
	hn=str(ps_hn[0]).split('host-name')[2]
	vyos2.exit()
	ps_dg=vyos2.run('show protocols static route 0.0.0.0/0 next-hop')
	dg=str(ps_dg[0]).split('next-hop')[2]
	vyos2.exit()
	ps_ds=vyos2.run('show system name-server')
	ds=str(ps_ds[0]).split('name-server')[2]
	vyos2.exit()


	return render_template('home.html',cur_hn=hn, cur_dns=ds, cur_dg=dg)

