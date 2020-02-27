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

	def save(self):
		self.router.configure()
		self.router.save()
		self.router.exit()

vyos = None
