import json
import requests
import logging
import time

from src.client import Client
from src.endpoints.users import Users

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('mattermost.api')


class Driver:

	defaultOptions = {
		'scheme': 'https',
		'url': 'localhost',
		'basePath': '/api/v4',
		'verify': True,
		'timeout': 30,
		'login_id': None,
		'password': None,
	}

	def __init__(self, options):
		self.options = self.defaultOptions.copy()
		self.options.update(options)
		self.driver = self.options
		self.client = Client(self.options)

		self.routes = {
			# 'users': Users(self.client),
			# 'teams': Teams(self.client),
			# 'channels': Channels(self.client),
			# 'posts': Posts(self.client),
			# 'files': Files(self.client),
			# 'preferences': Preferences(self.client),
			# 'webhooks': Webhooks(self.client),
			# 'commands': Commands(self.client),
			# 'system': System(self.client),
			# 'compliance': Compliance(self.client),
			# 'cluster': Cluster(self.client),
			# 'brand': Brand(self.client),
			# 'oauth': Oauth(self.client),
			# 'saml': Saml(self.client),
			# 'ldap': Ldap(self.client),
			# 'jobs': Jobs(self.client),
		}

	def login(self):
		result = self.users().login_user({
			'login_id': self.options['login_id'],
			'password': self.options['password'],
		})
		if result.status_code == 200:
			self.client.token = result.headers['Token']
		return result

	def users_api(self):
		if 'users' not in self.routes:
			self.routes['users'] = Users(self.client)
		return self.routes['users']

"""
	def teams(self):
		return self.routes['teams']

	def channels(self):
		return self.routes['channels']

	def posts(self):
		return self.routes['posts']

	def files(self):
		return self.routes['files']

	def preferences(self):
		return self.routes['preferences']

	def webhooks(self):
		return self.routes['webhooks']

	def commands(self):
		return self.routes['commands']

	def system(self):
		return self.routes['system']

	def compliance(self):
		return self.routes['compliance']

	def cluster(self):
		return self.routes['cluster']

	def brand(self):
		return self.routes['brand']

	def oauth(self):
		return self.routes['oauth']

	def saml(self):
		return self.routes['saml']

	def ldap(self):
		return self.routes['ldap']

	def jobs(self):
		return self.routes['jobs']
"""
