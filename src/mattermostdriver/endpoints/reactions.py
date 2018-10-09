from .base import Base
from .posts import Posts
from .users import Users


class Reactions(Base):
	endpoint = '/reactions'

	def create_reaction(self, options=None):
		return self.client.post(
			self.endpoint,
			options=options
		)

	def get_reactions_of_post(self, post_id):
		return self.client.get(
			Posts.endpoint + '/' + post_id + '/' + self.endpoint,
		)

	def delete_reaction(self, user_id, post_id, emoji_name, params=None):
		return self.client.delete(
			Users.endpoint + '/' + user_id + '/posts/' + post_id +
			'/reactions/' + emoji_name,
			params=params
		)
