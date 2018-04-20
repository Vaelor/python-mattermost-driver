from .base import Base


class Status(Base):

	def get_user_status(self, user_id):
		return self.client.get(
			'/users/' + user_id + '/status'
		)

	def update_user_status(self, user_id, options=None):
		return self.client.put(
			'/users/' + user_id + '/status',
			options=options
		)

	def get_user_statuses_by_id(self):
		return self.client.post(
			'/users/status/ids'
		)
