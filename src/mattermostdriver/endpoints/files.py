from .base import Base


class Files(Base):
	endpoint = '/files'

	def upload_file(self, channel_id, files):
		return self.client.post(
			self.endpoint,
			data={'channel_id': channel_id},
			files=files
		)

	def get_file(self, file_id):
		return self.client.get(
			self.endpoint + '/' + file_id,
		)

	def get_file_thumbnail(self, file_id):
		return self.client.get(
			self.endpoint + '/' + file_id + '/thumbnail',
		)

	def get_file_preview(self, file_id):
		return self.client.get(
			self.endpoint + '/' + file_id + '/preview',
		)

	def get_public_file_link(self, file_id):
		return self.client.get(
			self.endpoint + '/' + file_id + '/link',
		)

	def get_file_metadata(self, file_id):
		return self.client.get(
			self.endpoint + '/' + file_id + '/info',
		)
