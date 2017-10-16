from .base import Base


class DataRetention(Base):
	endpoint = '/data_retention'

	def get_data_retention_policy(self):
		return self.client.get(
			self.endpoint + '/policy'
		)
