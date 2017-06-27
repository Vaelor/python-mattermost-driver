import asyncio
import logging

from .client import Client
from .websocket import Websocket
from .endpoints.brand import Brand
from .endpoints.channels import Channels
from .endpoints.cluster import Cluster
from .endpoints.commands import Commands
from .endpoints.compliance import Compliance
from .endpoints.files import Files
from .endpoints.jobs import Jobs
from .endpoints.ldap import LDAP
from .endpoints.oauth import OAuth
from .endpoints.posts import Posts
from .endpoints.preferences import Preferences
from .endpoints.saml import SAML
from .endpoints.system import System
from .endpoints.teams import Teams
from .endpoints.users import Users
from .endpoints.webhooks import Webhooks

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('mattermostdriver.api')


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
		self.api = {
			'users': Users(self.client),
			'teams': Teams(self.client),
			'channels': Channels(self.client),
			'posts': Posts(self.client),
			'files': Files(self.client),
			'preferences': Preferences(self.client),
			'system': System(self.client),
			'webhooks': Webhooks(self.client),
			'commands': Commands(self.client),
			'compliance': Compliance(self.client),
			'cluster': Cluster(self.client),
			'brand': Brand(self.client),
			'oauth': OAuth(self.client),
			'saml': SAML(self.client),
			'ldap': LDAP(self.client),
			'jobs': Jobs(self.client),
		}
		self.websocket = None

	def init_websocket(self, event_handler):
		"""
		Will initialize the websocket connection to the mattermost server.
		This should be run after login(), because the websocket needs to make
		an authentification.
		See https://api.mattermost.com/v4/#tag/WebSocket for which
		websocket events mattermost sends.

		:param event_handler: The function to handle the websocket events.
		:type event_handler: Function
		:return: The event loop
		"""
		self.websocket = Websocket(self.options, self.client.token)
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.websocket.connect(event_handler))
		return loop

	def login(self):
		"""
		Log the user in.
		The log in information is saved in the client.
		- userid
		- username
		- cookies
		:return: The raw response from the request
		"""
		result = self.api['users'].login_user({
			'login_id': self.options['login_id'],
			'password': self.options['password'],
		})
		log.debug(result)
		if result.status_code == 200:
			self.client.token = result.headers['Token']
			self.client.cookies = result.cookies
			if 'id' in result:
				self.client.userid = result['id']
			if 'username' in result:
				self.client.username = result['username']
		return result

	def logout(self):
		self.api['users'].logout_user()
