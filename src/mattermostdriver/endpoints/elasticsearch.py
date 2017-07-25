from .base import Base


class Elasticsearch(Base):
	endpoint = '/elasticsearch'

	def test_elasticsearch_configuration(self):
		return self.client.post(
			self.endpoint + '/test'
		)

	def purge_all_elasticsearch_indexes(self):
		return self.client.post(
			self.endpoint + '/purge_indexes'
		)
