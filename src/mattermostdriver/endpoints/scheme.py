from .base import Base


class Scheme(Base):
	endpoint = '/schemes'

	def get_schemes(self, params=None):
		return self.client.get(
			self.endpoint,
			params=params
		)

	def create_scheme(self, options=None):
		return self.client.post(
			self.endpoint,
			options=options
		)

	def get_scheme(self, scheme_id):
		return self.client.get(
			self.endpoint + '/' + scheme_id
		)

	def delete_scheme(self, scheme_id):
		return self.client.delete(
			self.endpoint + '/' + scheme_id
		)

	def patch_scheme(self, scheme_id, options=None):
		return self.client.put(
			self.endpoint + '/' + scheme_id + '/patch',
			options=options
		)

	def get_page_of_teams_using_scheme(self, scheme_id, params=None):
		return self.client.get(
			self.endpoint + '/' + scheme_id + '/teams',
			params=params
		)

	def get_page_of_channels_using_scheme(self, scheme_id, params=None):
		return self.client.get(
			self.endpoint + '/' + scheme_id + '/channels',
			params=params
		)
