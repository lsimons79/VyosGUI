import vymgmt

class RouterMGMT:

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.router = vymgmt.Router('127.0.0.1', self.username, password=self.password, port=22)
		self.router.login()
		 
	def hostname(self, u_host):
		hostname = f'system host-name {u_host}'
		self.router.configure()
		self.router.delete('system host-name')
		self.router.set(hostname)
		self.router.commit()
		self.router.exit(force=True)
		
	def nameserver(self, u_dns):
		dns = f'system name-server {u_dns}'
		self.router.configure()
		self.router.delete('system name-server')
		self.router.set(dns)
		self.router.commit()
		self.router.exit(force=True)

	def gateway(self, u_gate):
		gateway = f'protocols static route 0.0.0.0/0 next-hop {u_gate}'
		self.router.configure()
		self.router.delete('protocols static route')
		self.router.set(gateway)
		self.router.commit()
		self.router.exit(force=True)

	def zone(self, u_zname, u_int):
		zname = f'zone-policy zone {u_zname} interface {u_int}'
		self.router.configure()
		self.router.set(zname)
		self.router.commit()
		self.router.exit(force=True)
        
	def link(self, u_zone1, u_zone2, u_lname):
		drop = f'firewall name {u_lname} default-action drop'
		log = f'firewall name {u_lname} enable-default-log'
		lname = f'zone-policy zone {u_zone1} from {u_zone2} firewall name {u_lname}'
		self.router.configure()
		self.router.set(drop)
		self.router.set(log)
		self.router.set(lname)
		self.router.commit()
		self.router.exit(force=True)

	def established(self, u_name):
		action = f'firewall name {u_name} rule 1 action accept'
		state = f'firewall name {u_name} rule 1 state established enable'
		self.router.configure()
		self.router.set(action)
		self.router.set(state)
		self.router.commit()
		self.router.exit(force=True)

	def rule(self, u_name, u_rule, u_action, u_port, u_protocol, u_address, u_direction):
		action = f'firewall name {u_name} rule {u_rule} action {u_action}'
		port = f'firewall name {u_name} rule {u_rule} {u_direction} port {u_port}'
		protocol = f'firewall name {u_name} rule {u_rule} protocol {u_protocl}'
		address = f'firewall name {u_name} rule {u_rule} {u_direction} address {u_address}'
		self.router.configure()
		self.router.set(action)
		if {u_port}:
			self.router.set(port)
		if {u_protocol}:
			self.router.set(protocol)
		if {u_address}:
			self.router.set(address)
		self.router.commit()
		self.router.exit(force=True)


	def setint(self, u_int, u_address):
		u_cmd = f'interfaces ethernet {u_int} address {u_address}'
		self.router.configure()
		self.router.set(u_cmd)
		self.router.commit()
		self.router.exit(force=True)

	def save(self):
		self.router.configure()
		self.router.save()
		self.router.exit()

	def format(self, command):
		self.router.configure()
		split_cmd = str(self.router.run_conf_mode_command(command)).split('[m')
		return split_cmd

	def exit(self):
		self.router.exit()
		
vyos = None
