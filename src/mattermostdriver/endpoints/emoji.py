from .base import Base


class Emoji(Base):
	endpoint = '/emoji'

	def create_custom_emoji(self, data):
		return self.client.post(
			self.endpoint,
			data=data
		)

	def get_emoji_list(self, params=None):
		return self.client.get(
			self.endpoint,
			params=params
		)

	def get_custom_emoji(self, emoji_id):
		return self.client.get(
			self.endpoint + '/' + emoji_id
		)

	def delete_custom_emoji(self, emoji_id):
		return self.client.delete(
			self.endpoint + '/' + emoji_id
		)

	def get_custom_emoji_image(self, emoji_id):
		return self.client.get(
			self.endpoint + '/' + emoji_id + '/image'
		)
