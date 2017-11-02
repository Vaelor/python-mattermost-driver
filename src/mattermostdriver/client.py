import logging
import requests

from .exceptions import (
	InvalidOrMissingParameters,
	NoAccessTokenProvided,
	NotEnoughPermissions,
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
		self._options = options
		self._token = ''
		self._cookies = None
		self._userid = ''
		self._username = ''


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
			data = e.response.json()
			if data['status_code'] == 400:
				raise InvalidOrMissingParameters(data['message'])
			elif data['status_code'] == 401:
				raise NoAccessTokenProvided(data['message'])
			elif data['status_code'] == 403:
				raise NotEnoughPermissions(data['message'])
			elif data['status_code'] == 413:
				raise ContentTooLarge(data['message'])
			elif data['status_code'] == 501:
				raise FeatureDisabled(data['message'])
			else:
				raise

		log.debug(response)
		return response

	def get(self, endpoint, options=None, params=None):
		response = self.make_request('get', endpoint, options=options, params=params)
		try:
			return response.json()
		except ValueError:
			return response

	def post(self, endpoint, options=None, params=None, data=None, files=None):
		return self.make_request('post', endpoint, options=options, params=params, data=data, files=files).json()

	def put(self, endpoint, options=None, params=None, data=None):
		return self.make_request('put', endpoint, options=options, params=params, data=data).json()

	def delete(self, endpoint, options=None, params=None, data=None):
		return self.make_request('delete', endpoint, options=options, params=params, data=data).json()
