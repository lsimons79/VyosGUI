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
	command = vyos.format('show interfaces')
	eth = [i for i in command if "eth" in i]
	int_split = []
	interface = []
	for i in range(len(eth)):
		int_split.append(str(eth[i]).split('ethernet')[1])
		interface.append(str(int_split[i]).split(' ')[1])
	vyos.exit()

	command2 = vyos.format2('show zone')
	name = [i for i in command2 if "Name:" in i]
	zone = []
	for i in range(len(name)):
		zone.append(str(name[i]).split('Name:')[1])

	vyos.exit()

	if request.method == 'POST':
		vyos = RouterMGMT('vyos', 'vyos')
		if 'commit1' in request.form:
			u_zname = request.form['zoneName']
			u_int = request.form['interface']
			e = None
			error = None

			try:
				vyos.zone(u_zname, u_int)
			except vymgmt.router.ConfigError as e:
				error = str(e)
				flash(error)
				return redirect(url_for('system.firewall'))

		elif 'save' in request.form:
			e = None
			error = None
			try:
				vyos.save()
			except vymgmt.router.ConfigError as e:

				error = str(e)
				flash(error)
				return redirect(url_for('system.firewall'))

	return render_template('firewall.html', int=interface, zone=zone)

@bp.route('/home')
def home():
	vyos2 = RouterMGMT('vyos', 'vyos')
	ps_hn=vyos2.format('show system host-name')
	hn=str(ps_hn[0]).split('host-name')[2]
	vyos2.exit()
	ps_dg=vyos2.format('show protocols static route 0.0.0.0/0 next-hop')
	dg=str(ps_dg[0]).split('next-hop ')[2]
	dg=str(dg).split(' ')[1]
	vyos2.exit()
	ps_ds=vyos2.format('show system name-server')
	ds=str(ps_ds[0]).split('name-server')[2]
	vyos2.exit()


	return render_template('home.html',cur_hn=hn, cur_dns=ds, cur_dg=dg)

