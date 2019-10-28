from .base import Base


class Opengraph(Base):
	endpoint = '/opengraph'

	def get_opengraph_metadata_for_url(self, options):
		return self.client.post(
			self.endpoint,
			options=options
		)
