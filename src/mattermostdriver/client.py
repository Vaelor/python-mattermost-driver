import json

import logging
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('mattermostdriver.websocket')


class Client:
	def __init__(self, options):
		self.url = '{scheme:s}://{url:s}{basepath:s}'.format(
			scheme=options['scheme'],
			url=options['url'],
			basepath=options['basepath']
		)
		self._scheme = options['scheme']
		self._url = options['url']
		self._basepath = options['basepath']
		self._port = options['port']
		self._verify = options['verify']
		self._token = ''
		self._cookie = None

	@property
	def token(self):
		return self._token

	@token.setter
	def token(self, t):
		self._token = t

	def auth_header(self):
		if self._token == '':
			return {}
		return {"Authorization": "Bearer {token:s}".format(token=self._token)}

	def make_request(self, method, endpoint, options=None, params=None, data=None):
		if options is None:
			options = {}
		if params is None:
			params = {}
		if data is None:
			data = {}
		method = method.lower()
		request = requests.get
		if method == 'post':
			request = requests.post
		elif method == 'put':
			request = requests.put
		elif method == 'delete':
			request = requests.delete

		response = request(
				self.url + endpoint,
				headers=self.auth_header(),
				verify=self._verify,
				json=options,
				params=params,
				data=data
			)
		response.raise_for_status()
		return response

	def get(self, endpoint, options=None, params=None):
		return json.loads(
			self.make_request('get', endpoint, options=options, params=params).text
		)

	def post(self, endpoint, options=None, params=None, data=None):
		return json.loads(
			self.make_request('post', endpoint, options=options, params=params, data=data).text
		)

	def put(self, endpoint, options=None, params=None, data=None):
		return json.loads(
			self.make_request('put', endpoint, options=options, params=params, data=data).text
		)

	def delete(self, endpoint, options=None, params=None, data=None):
		return json.loads(
			self.make_request('delete', endpoint, options=options, params=params, data=data).text
		)