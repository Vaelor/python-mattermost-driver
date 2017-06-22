import json

import requests


class Client:
	def __init__(self, options):
		self.url = '{scheme:s}://{url:s}{basePath:s}'.format(
			scheme=options['scheme'],
			url=options['url'],
			basePath=options['basePath']
		)
		self._verify = options['verify']
		self._token = ''

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

	def make_request(self, method, endpoint, options=None):
		if options is None:
			options = {}
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
				json=options
			)
		response.raise_for_status()
		return response

	def get(self, endpoint, options=None):
		return json.loads(
			self.make_request('get', endpoint, options).text
		)

	def post(self, endpoint, options=None):
		return json.loads(
			self.make_request('post', endpoint, options).text
		)

	def put(self, endpoint, options=None):
		return json.loads(
			self.make_request('put', endpoint, options).text
		)

	def delete(self, endpoint, options=None):
		return json.loads(
			self.make_request('delete', endpoint, options).text
		)