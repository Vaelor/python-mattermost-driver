from .base import Base
from .users import Users


class Preferences(Base):
	"""
	This is the endpoint for Preferences.
	It is special in a way, that the endpoint is /user and not /preferences,
	like one might expect at first!
	"""
	endpoint = Users.endpoint

	def get_user_preferences(self, user_id):
		return self.client.get(
			self.endpoint + '/' + user_id + '/preferences'
		)

	def save_user_preferences(self, user_id, options=None):
		return self.client.put(
			self.endpoint + '/' + user_id + '/preferences',
			options=options
		)

	def delete_user_preferences(self, user_id, options=None):
		return self.client.post(
			self.endpoint + '/' + user_id + '/preferences/delete',
			options=options
		)

	def list_user_preferences_by_category(self, user_id, category):
		return self.client.get(
			self.endpoint + '/' + user_id + '/preferences/' + category
		)

	def get_specific_user_preference(self, user_id, category, preference_name):
		return self.client.get(
			self.endpoint + '/' + user_id +
			'/preferences/' + category +
			'/name/' + preference_name
		)
