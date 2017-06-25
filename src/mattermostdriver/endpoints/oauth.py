from .base import Base
from .users import Users


class OAuth(Base):
	endpoint = '/oauth'

	def register_oauth_app(self, options):
		return self.client.post(
			self.endpoint + '/apps',
			options=options
		)

	def get_oauth_apps(self, params=None):
		return self.client.get(
			self.endpoint + '/apps',
			params=params
		)

	def get_oauth_app(self, app_id):
		return self.client.get(
			self.endpoint + '/apps/' + app_id
		)

	def delete_oauth_app(self, app_id):
		return self.client.delete(
			self.endpoint + '/apps/' + app_id
		)

	def regenerate_oauth_app_secret(self, app_id):
		return self.client.post(
			self.endpoint + '/apps/' + app_id + '/regen_secret'
		)

	def get_info_on_oauth_app(self, app_id):
		return self.client.get(
			self.endpoint + '/apps/' + app_id + '/info'
		)

	def get_authorized_oauth_apps(self, user_id, params=None):
		return self.client.get(
			Users.endpoint + user_id + '/oauth/apps/authorized',
			params=params
		)