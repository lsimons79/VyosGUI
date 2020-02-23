import vymgmt

class RouterMGMT:

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.router = vymgmt.Router('127.0.0.1', self.username, password=self.password, port=22)
		self.router.login()
		 
	def system(self, u_host, u_dns, u_gateway):
		hostname = f'system hostname {u_host}'
		dns = f'system name-server {u_dns}'
		gateway = f'protocols static route 0.0.0.0/0 next-hop {u_gateway}'
		self.router.configure()
		self.router.set(hostname)
		self.router.set(dns)
		self.router.set(gateway)
		self.router.commit()
		self.router.save()


vyos = None
