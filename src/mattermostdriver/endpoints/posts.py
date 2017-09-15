from .base import Base
from .teams import Teams
from .users import Users
from .channels import Channels


class Posts(Base):
	endpoint = '/posts'

	def create_post(self, options):
		return self.client.post(
			self.endpoint,
			options=options
		)

	def get_post(self, post_id):
		return self.client.get(
			self.endpoint + '/' + post_id,
		)

	def delete_post(self, post_id):
		return self.client.delete(
			self.endpoint + '/' + post_id,
		)

	def update_post(self, post_id, options=None):
		return self.client.put(
			self.endpoint + '/' + post_id,
			options=options
		)

	def patch_post(self, post_id, options=None):
		return self.client.put(
			self.endpoint + '/' + post_id + '/patch',
			options=options
		)

	def get_thread(self, post_id):
		return self.client.get(
			self.endpoint + '/' + post_id + '/thread',
		)

	def get_list_of_flagged_posts(self, user_id, params=None):
		return self.client.get(
			Users.endpoint + '/' + user_id + '/posts/flagged',
			params=params
		)

	def get_file_info_for_post(self, post_id):
		return self.client.get(
			self.endpoint + '/' + post_id + '/files/info',
		)

	def get_posts_for_channel(self, channel_id, params=None):
		return self.client.get(
			Channels.endpoint + '/' + channel_id + '/posts',
			params=params
		)

	def search_for_team_posts(self, team_id, options):
		return self.client.post(
			Teams.endpoint + '/' + team_id + '/posts/search',
			options=options
		)

	def pin_post_to_channel(self, post_id):
		return self.client.post(
			self.endpoint + '/' + post_id + '/pin'
		)

	def unpin_post_to_channel(self, post_id):
		return self.client.post(
			self.endpoint + '/' + post_id + '/unpin'
		)

	def perform_post_action(self, post_id, action_id):
		return self.client.post(
			self.endpoint + '/' + post_id + '/actions/' + action_id
		)
