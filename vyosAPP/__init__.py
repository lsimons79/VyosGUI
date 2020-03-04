import os

from flask import Flask,redirect

def create_app(test_config=None):
	#create and configure the application
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(SECRET_KEY='vyos')
	
	if test_config is None:
		#Load instance config if it exists (post deploy)
		app.config.from_pyfile('config.py', silent=True)
	else:
		#Load development config (pre deploy)
		app.config.from_mapping(test_config)

	#check if instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route('/hello')
	def hello():
		return 'Hello, World'

	#Applying blueprints to application
	from vyosAPP import login, system
	
	app.register_blueprint(login.bp)
	app.register_blueprint(system.bp)

	return app
	
