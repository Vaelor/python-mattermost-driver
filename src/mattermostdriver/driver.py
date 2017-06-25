import json

import asyncio
import requests
import logging
import time

from src.client import Client
from src.endpoints.brand import Brand
from src.endpoints.channels import Channels
from src.endpoints.cluster import Cluster
from src.endpoints.commands import Commands
from src.endpoints.compliance import Compliance
from src.endpoints.files import Files
from src.endpoints.jobs import Jobs
from src.endpoints.ldap import LDAP
from src.endpoints.oauth import OAuth
from src.endpoints.posts import Posts
from src.endpoints.preferences import Preferences
from src.endpoints.saml import SAML
from src.endpoints.system import System
from src.endpoints.teams import Teams
from src.endpoints.users import Users
from src.endpoints.webhooks import Webhooks
from src.websocket import Websocket

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('mattermost.api')


class Driver:

	defaultOptions = {
		'scheme': 'https',
		'url': 'localhost',
		'port': 8065,
		'basepath': '/api/v4',
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
		self.routes = {}
		# TODO: Maybe this makes more sense
		# self.api = {
		# 	'users': Users(self.client)
		# }
		self.websocket = None

	def init_websocket(self, event_handler):
		self.websocket = Websocket(self.options, self.client.token)
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.websocket.connect(event_handler))
		return loop

	def login(self):
		result = self.users_api().login_user({
			'login_id': self.options['login_id'],
			'password': self.options['password'],
		})
		if result.status_code == 200:
			self.client.token = result.headers['Token']
		return result

	def logout(self):
		self.users_api().logout_user()

	def users_api(self):
		if 'users' not in self.routes:
			self.routes['users'] = Users(self.client)
		return self.routes['users']

	def teams_api(self):
		if 'teams' not in self.routes:
			self.routes['teams'] = Teams(self.client)
		return self.routes['teams']

	def channels_api(self):
		if 'channels' not in self.routes:
			self.routes['channels'] = Channels(self.client)
		return self.routes['channels']

	def posts_api(self):
		if 'posts' not in self.routes:
			self.routes['posts'] = Posts(self.client)
		return self.routes['posts']

	def files_api(self):
		if 'files' not in self.routes:
			self.routes['files'] = Files(self.client)
		return self.routes['files']

	def preferences_api(self):
		if 'preferences' not in self.routes:
			self.routes['preferences'] = Preferences(self.client)
		return self.routes['preferences']

	def webhooks_api(self):
		if 'webhooks' not in self.routes:
			self.routes['webhooks'] = Webhooks(self.client)
		return self.routes['webhooks']

	def commands_api(self):
		if 'commands' not in self.routes:
			self.routes['commands'] = Commands(self.client)
		return self.routes['commands']

	def system_api(self):
		if 'system' not in self.routes:
			self.routes['system'] = System(self.client)
		return self.routes['system']

	def compliance_api(self):
		if 'compliance' not in self.routes:
			self.routes['compliance'] = Compliance(self.client)
		return self.routes['compliance']

	def cluster_api(self):
		if 'cluster' not in self.routes:
			self.routes['cluster'] = Cluster(self.client)
		return self.routes['cluster']

	def brand_api(self):
		if 'brand' not in self.routes:
			self.routes['brand'] = Brand(self.client)
		return self.routes['brand']

	def oauth_api(self):
		if 'oauth' not in self.routes:
			self.routes['oauth'] = OAuth(self.client)
		return self.routes['oauth']

	def saml_api(self):
		if 'saml' not in self.routes:
			self.routes['saml'] = SAML(self.client)
		return self.routes['saml']

	def ldap_api(self):
		if 'ldap' not in self.routes:
			self.routes['ldap'] = LDAP(self.client)
		return self.routes['ldap']

	def jobs_api(self):
		if 'jobs' not in self.routes:
			self.routes['jobs'] = Jobs(self.client)
		return self.routes['jobs']
