import json

from .base import Base


class Emoji(Base):
	endpoint = '/emoji'

	def create_custom_emoji(self, emoji_name, files):
		emoji = {'name': emoji_name, 'creator_id': self.client.userid}
		return self.client.post(
			self.endpoint,
			data={'emoji': json.dumps(emoji)},
			files=files
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

	def get_custom_emoji_by_name(self, name):
		return self.client.get(
			self.endpoint + '/name/' + name
		)

	def get_custom_emoji_image(self, emoji_id):
		return self.client.get(
			self.endpoint + '/' + emoji_id + '/image'
		)

	def search_custom_emoji(self, options=None):
		return self.client.post(
			self.endpoint + '/search',
			options=options
		)

	def autocomplete_custom_emoji(self, params=None):
		return self.client.get(
			self.endpoint + '/autocomplete',
			params=params
		)
