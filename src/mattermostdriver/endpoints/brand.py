from .base import Base

class Brand(Base):
	endpoint = '/brand'

	def get_brand_image(self):
		return self.client.get(
			self.endpoint + '/image'
		)

	def upload_brand_image(self, data=None):
		return self.client.post(
			self.endpoint + '/image',
			data=data
		)
