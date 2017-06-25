from .base import Base


class LDAP(Base):
	endpoint = '/ldap'

	def sync_ldap(self):
		return self.client.post(
			self.endpoint + '/sync'
		)

	def test_ldap_config(self):
		return self.client.post(
			self.endpoint + '/test'
		)
