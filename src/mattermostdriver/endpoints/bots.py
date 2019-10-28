from .base import Base


class Bots(Base):
	endpoint = '/bots'

	def create_bot(self, options):
		return self.client.post(
			self.endpoint,
			options=options
		)

	def get_bots(self, params=None):
		return self.client.get(
			self.endpoint,
			params=params
		)

	def patch_bot(self, bot_id, options):
		return self.client.put(
			self.endpoint + '/' + bot_id,
			options=options
		)

	def get_bot(self, bot_id, params=None):
		return self.client.get(
			self.endpoint + '/' + bot_id,
			params=params
		)

	def disable_bot(self, bot_id):
		return self.client.post(
			self.endpoint + '/' + bot_id + '/disable'
		)

	def enable_bot(self, bot_id):
		return self.client.post(
			self.endpoint + '/' + bot_id + '/enable'
		)

	def assign_bot_to_user(self, bot_id, user_id):
		return self.client.post(
			self.endpoint + '/' + bot_id + '/assign/' + user_id
		)

	def get_bot_lhs_icon(self, bot_id):
		return self.client.get(
			self.endpoint + '/' + bot_id + '/icon'
		)

	def set_bot_lhs_icon(self, bot_id, files):
		return self.client.post(
			self.endpoint + '/' + bot_id + '/icon',
			files=files
		)

	def delete_bot_lhs_icon(self, bot_id):
		return self.client.delete(
			self.endpoint + '/' + bot_id + '/icon'
		)
