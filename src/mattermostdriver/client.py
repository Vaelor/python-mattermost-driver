"""
Client for the driver, which holds information about the logged in user
and actually makes the requests to the mattermost server
"""

import logging
import requests

from .exceptions import (
	InvalidOrMissingParameters,
	NoAccessTokenProvided,
	NotEnoughPermissions,
	ResourceNotFound,
	MethodNotAllowed,
	ContentTooLarge,
	FeatureDisabled
)

log = logging.getLogger('mattermostdriver.websocket')
log.setLevel(logging.INFO)


class Client:
	def __init__(self, options):
		self._url = '{scheme:s}://{url:s}:{port:d}{basepath:s}'.format(
			scheme=options['scheme'],
			url=options['url'],
			port=options['port'],
			basepath=options['basepath']
		)
		self._scheme = options['scheme']
		self._basepath = options['basepath']
		self._port = options['port']
		self._verify = options['verify']
		if options['debug']:
			self.activate_verbose_logging()

		self._options = options
		self._token = ''
		self._cookies = None
		self._userid = ''
		self._username = ''

	@staticmethod
	def activate_verbose_logging(level=logging.DEBUG):
		log.setLevel(level)
		# http://docs.python-requests.org/en/master/api/#api-changes
		from http.client import HTTPConnection
		HTTPConnection.debuglevel = 1
		requests_log = logging.getLogger("requests.packages.urllib3")
		requests_log.setLevel(level)
		requests_log.propagate = True

	@property
	def userid(self):
		"""
		:return: The user id of the logged in user
		"""
		return self._userid

	@userid.setter
	def userid(self, user_id):
		self._userid = user_id

	@property
	def username(self):
		"""
		:return: The username of the logged in user. If none, returns an emtpy string.
		"""
		return self._username

	@username.setter
	def username(self, username):
		self._username = username

	@property
	def url(self):
		return self._url

	@property
	def cookies(self):
		"""
		:return: The cookie given on login
		"""
		return self._cookies

	@cookies.setter
	def cookies(self, cookies):
		self._cookies = cookies

	@property
	def token(self):
		"""
		:return: The token for the login
		"""
		return self._token

	@token.setter
	def token(self, t):
		self._token = t

	def auth_header(self):
		if self._token == '':
			return {}
		return {"Authorization": "Bearer {token:s}".format(token=self._token)}

	def make_request(self, method, endpoint, options=None, params=None, data=None, files=None, basepath=None):
		if options is None:
			options = {}
		if params is None:
			params = {}
		if data is None:
			data = {}
		if basepath:
			url = '{scheme:s}://{url:s}:{port:d}{basepath:s}'.format(
				scheme=self._options['scheme'],
				url=self._options['url'],
				port=self._options['port'],
				basepath=basepath
			)
		else:
			url = self.url
		method = method.lower()
		request = requests.get
		if method == 'post':
			request = requests.post
		elif method == 'put':
			request = requests.put
		elif method == 'delete':
			request = requests.delete

		response = request(
				url + endpoint,
				headers=self.auth_header(),
				verify=self._verify,
				json=options,
				params=params,
				data=data,
				files=files
			)
		try:
			response.raise_for_status()
		except requests.HTTPError as e:
			try:
				data = e.response.json()
				message = data.get('message', data)
			except ValueError:
				log.debug('Could not convert response to json')
				message = response.text
			log.error(message)
			if e.response.status_code == 400:
				raise InvalidOrMissingParameters(message)
			elif e.response.status_code == 401:
				raise NoAccessTokenProvided(message)
			elif e.response.status_code == 403:
				raise NotEnoughPermissions(message)
			elif e.response.status_code == 404:
				raise ResourceNotFound(message)
			elif e.response.status_code == 405:
				raise MethodNotAllowed(message)
			elif e.response.status_code == 413:
				raise ContentTooLarge(message)
			elif e.response.status_code == 501:
				raise FeatureDisabled(message)
			else:
				raise

		log.debug(response)
		return response

	def get(self, endpoint, options=None, params=None):
		response = self.make_request('get', endpoint, options=options, params=params)

		if response.headers['Content-Type'] != 'application/json':
			log.debug('Response is not application/json, returning raw response')
			return response

		try:
			return response.json()
		except ValueError:
			log.debug('Could not convert response to json, returning raw response')
			return response

	def post(self, endpoint, options=None, params=None, data=None, files=None):
		return self.make_request('post', endpoint, options=options, params=params, data=data, files=files).json()

	def put(self, endpoint, options=None, params=None, data=None):
		return self.make_request('put', endpoint, options=options, params=params, data=data).json()

	def delete(self, endpoint, options=None, params=None, data=None):
		return self.make_request('delete', endpoint, options=options, params=params, data=data).json()
