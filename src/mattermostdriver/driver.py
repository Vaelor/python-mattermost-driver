import asyncio
import logging
import warnings

from .client import Client
from .websocket import Websocket
from .endpoints.brand import Brand
from .endpoints.channels import Channels
from .endpoints.cluster import Cluster
from .endpoints.commands import Commands
from .endpoints.compliance import Compliance
from .endpoints.files import Files
from .endpoints.ldap import LDAP
from .endpoints.oauth import OAuth
from .endpoints.posts import Posts
from .endpoints.preferences import Preferences
from .endpoints.saml import SAML
from .endpoints.system import System
from .endpoints.teams import Teams
from .endpoints.users import Users
from .endpoints.webhooks import Webhooks
from .endpoints.elasticsearch import Elasticsearch
from .endpoints.emoji import Emoji
from .endpoints.data_retention import DataRetention

log = logging.getLogger('mattermostdriver.api')
log.setLevel(logging.INFO)


class Driver:
	"""
	Contains the client, api and provides you with functions for
	login, logout and initializing a websocket connection.
	"""

	default_options = {
		'scheme': 'https',
		'url': 'localhost',
		'port': 8065,
		'basepath': '/api/v4',
		'verify': True,
		'timeout': 30,
		'login_id': None,
		'password': None,
		'token': None,
		'mfa_token': None
	}
	"""
	Required:
		Either
		- login_id
		- password
		Or
		- token (https://docs.mattermost.com/developer/personal-access-tokens.html)

	Optional:
		- scheme
		- url (though it would be a good idea to change that)
		- port
		- verify
		- timeout
		- mfa_token
	
	Should not be changed:
		- basepath - unlikeliy this would do any good
	"""

	def __init__(self, options=default_options, client_cls=Client):
		"""
		:param options: A dict with the values from `default_options`
		:type options: dict
		"""
		if options is None:
			options = self.default_options
		self.options = self.default_options.copy()
		self.options.update(options)
		self.driver = self.options
		self.client = client_cls(self.options)
		self._api = {
			'users': Users(self.client),
			'teams': Teams(self.client),
			'channels': Channels(self.client),
			'posts': Posts(self.client),
			'files': Files(self.client),
			'preferences': Preferences(self.client),
			'emoji': Emoji(self.client),
			'system': System(self.client),
			'webhooks': Webhooks(self.client),
			'commands': Commands(self.client),
			'compliance': Compliance(self.client),
			'cluster': Cluster(self.client),
			'brand': Brand(self.client),
			'oauth': OAuth(self.client),
			'saml': SAML(self.client),
			'ldap': LDAP(self.client),
			'elasticsearch': Elasticsearch(self.client),
			'data_retention': DataRetention(self.client),
		}
		self.websocket = None

	def init_websocket(self, event_handler, websocket_cls=Websocket):
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
		self.websocket = websocket_cls(self.options, self.client.token)
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.websocket.connect(event_handler))
		return loop

	def login(self):
		"""
		Logs the user in.

		The log in information is saved in the client:

		- userid
		- username
		- cookies

		:return: The raw response from the request
		"""
		if self.options['token']:
			self.client.token = self.options['token']
			result = self.users.get_user('me')
		else:
			result = self.users.login_user({
				'login_id': self.options['login_id'],
				'password': self.options['password'],
				'token': self.options['mfa_token']
			})
			if result.status_code == 200:
				self.client.token = result.headers['Token']
				self.client.cookies = result.cookies

		log.debug(result)

		if 'id' in result:
			self.client.userid = result['id']
		if 'username' in result:
			self.client.username = result['username']

		return result

	def logout(self):
		"""
		Log the user out.

		:return: The JSON response from the server
		"""
		self.client.token = ''
		self.client.userid = ''
		self.client.username = ''
		self.client.cookies = None
		return self.users.logout_user()

	@property
	def api(self):
		warnings.warn('Deprecated for 5.0.0. Use the endpoints directly instead.', DeprecationWarning)
		return self._api

	@property
	def users(self):
		return Users(self.client)

	@property
	def teams(self):
		return Teams(self.client)

	@property
	def channels(self):
		return Channels(self.client)

	@property
	def posts(self):
		return Posts(self.client)

	@property
	def files(self):
		return Files(self.client)

	@property
	def preferences(self):
		return Preferences(self.client)

	@property
	def emoji(self):
		return Emoji(self.client)

	@property
	def system(self):
		return System(self.client)

	@property
	def webhooks(self):
		return Webhooks(self.client)

	@property
	def compliance(self):
		return Compliance(self.client)

	@property
	def cluster(self):
		return Cluster(self.client)

	@property
	def brand(self):
		return Brand(self.client)

	@property
	def oauth(self):
		return OAuth(self.client)

	@property
	def saml(self):
		return SAML(self.client)

	@property
	def ldap(self):
		return LDAP(self.client)

	@property
	def elasticsearch(self):
		return Elasticsearch(self.client)

	@property
	def data_retention(self):
		return DataRetention(self.client)