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
from .endpoints.reactions import Reactions
from .endpoints.saml import SAML
from .endpoints.system import System
from .endpoints.teams import Teams
from .endpoints.users import Users
from .endpoints.webhooks import Webhooks
from .endpoints.elasticsearch import Elasticsearch
from .endpoints.emoji import Emoji
from .endpoints.data_retention import DataRetention
from .endpoints.roles import Roles
from .endpoints.status import Status

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
		'mfa_token': None,
		'debug': False
	}
	"""
	Required options
		- url

	Either
		- login_id
		- password

	Or
		- token (https://docs.mattermost.com/developer/personal-access-tokens.html)

	Optional
		- scheme ('https')
		- port (8065)
		- verify (True)
		- timeout (30)
		- mfa_token (None)
		- debug (False)

	Should not be changed
		- basepath ('/api/v4') - unlikely this would do any good
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
		if self.options['debug']:
			log.setLevel(logging.DEBUG)
			log.warning('Careful!!\nSetting debug to True, will reveal your password in the log output if you do driver.login()!\nThis is NOT for production!')
		self.client = client_cls(self.options)
		self._api = {
			'users': Users(self.client),
			'teams': Teams(self.client),
			'channels': Channels(self.client),
			'posts': Posts(self.client),
			'files': Files(self.client),
			'preferences': Preferences(self.client),
			'status': Status(self.client),
			'emoji': Emoji(self.client),
			'reactions': Reactions(self.client),
			'system': System(self.client),
			'webhooks': Webhooks(self.client),
			'commands': Commands(self.client),
			'compliance': Compliance(self.client),
			'cluster': Cluster(self.client),
			'brand': Brand(self.client),
			'oauth': OAuth(self.client),
			'roles': Roles(self.client),
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

		Example of a really simple event_handler function

		.. code:: python

			@asyncio.coroutine
			def my_event_handler(message):
				print(message)


		:param event_handler: The function to handle the websocket events. Takes one argument.
		:type event_handler: Function(message)
		:return: The event loop
		"""
		self.websocket = websocket_cls(self.options, self.client.token)
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.websocket.connect(event_handler))
		return loop

	def login(self):
		"""
		Logs the user in.

		The log in information is saved in the client
			- userid
			- username
			- cookies

		:return: The raw response from the request
		"""
		if self.options['token']:
			self.client.token = self.options['token']
			result = self.users.get_user('me')
		else:
			response = self.users.login_user({
				'login_id': self.options['login_id'],
				'password': self.options['password'],
				'token': self.options['mfa_token']
			})
			if response.status_code == 200:
				self.client.token = response.headers['Token']
				self.client.cookies = response.cookies
			try:
				result = response.json()
			except ValueError:
				log.debug('Could not convert response to json, returning raw response')
				result = response

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
		result = self.users.logout_user()
		self.client.token = ''
		self.client.userid = ''
		self.client.username = ''
		self.client.cookies = None
		return result

	@property
	def api(self):
		"""
		.. deprecated:: 4.0.2

		Use the endpoints directly instead.

		:return: dictionary containing the endpoints
		:rtype: dict
		"""
		warnings.warn('Deprecated for 5.0.0. Use the endpoints directly instead.', DeprecationWarning)
		return self._api

	@property
	def users(self):
		"""
		Api endpoint for users

		:return: Instance of :class:`~endpoints.users.Users`
		"""
		return Users(self.client)

	@property
	def teams(self):
		"""
		Api endpoint for teams

		:return: Instance of :class:`~endpoints.teams.Teams`
		"""
		return Teams(self.client)

	@property
	def channels(self):
		"""
		Api endpoint for channels

		:return: Instance of :class:`~endpoints.channels.Channels`
		"""
		return Channels(self.client)

	@property
	def posts(self):
		"""
		Api endpoint for posts

		:return: Instance of :class:`~endpoints.posts.Posts`
		"""
		return Posts(self.client)

	@property
	def files(self):
		"""
		Api endpoint for files

		:return: Instance of :class:`~endpoints.files.Files`
		"""
		return Files(self.client)

	@property
	def preferences(self):
		"""
		Api endpoint for preferences

		:return: Instance of :class:`~endpoints.preferences.Preferences`
		"""
		return Preferences(self.client)

	@property
	def emoji(self):
		"""
		Api endpoint for emoji

		:return: Instance of :class:`~endpoints.emoji.Emoji`
		"""
		return Emoji(self.client)

	@property
	def reactions(self):
		"""
		Api endpoint for posts' reactions

		:return: Instance of :class:`~endpoints.reactions.Reactions`
		"""
		return Reactions(self.client)

	@property
	def system(self):
		"""
		Api endpoint for system

		:return: Instance of :class:`~endpoints.system.System`
		"""
		return System(self.client)

	@property
	def webhooks(self):
		"""
		Api endpoint for webhooks

		:return: Instance of :class:`~endpoints.webhooks.Webhooks`
		"""
		return Webhooks(self.client)

	@property
	def compliance(self):
		"""
		Api endpoint for compliance

		:return: Instance of :class:`~endpoints.compliance.Compliance`
		"""
		return Compliance(self.client)

	@property
	def cluster(self):
		"""
		Api endpoint for cluster

		:return: Instance of :class:`~endpoints.cluster.Cluster`
		"""
		return Cluster(self.client)

	@property
	def brand(self):
		"""
		Api endpoint for brand

		:return: Instance of :class:`~endpoints.brand.Brand`
		"""
		return Brand(self.client)

	@property
	def oauth(self):
		"""
		Api endpoint for oauth

		:return: Instance of :class:`~endpoints.oauth.OAuth`
		"""
		return OAuth(self.client)

	@property
	def saml(self):
		"""
		Api endpoint for saml

		:return: Instance of :class:`~endpoints.saml.SAML`
		"""
		return SAML(self.client)

	@property
	def ldap(self):
		"""
		Api endpoint for ldap

		:return: Instance of :class:`~endpoints.ldap.LDAP`
		"""
		return LDAP(self.client)

	@property
	def elasticsearch(self):
		"""
		Api endpoint for elasticsearch

		:return: Instance of :class:`~endpoints.elasticsearch.Elasticsearch`
		"""
		return Elasticsearch(self.client)

	@property
	def data_retention(self):
		"""
		Api endpoint for data_retention

		:return: Instance of :class:`~endpoints.data_retention.DataRetention`
		"""
		return DataRetention(self.client)
