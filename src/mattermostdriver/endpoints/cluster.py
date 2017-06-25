from .base import Base


class Cluster(Base):
	endpoint = '/cluster'

	def get_cluster_status(self):
		return self.client.get(
			self.endpoint + '/status'
		)
