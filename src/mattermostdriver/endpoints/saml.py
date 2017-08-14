from .base import Base


class SAML(Base):
	endpoint = '/saml'

	def get_metadata(self):
		return self.client.get(
			self.endpoint + '/metadata'
		)

	def upload_idp_certificate(self, files):
		return self.client.post(
			self.endpoint + '/certificate/idp',
			files=files
		)

	def remove_idp_certificate(self):
		return self.client.delete(
			self.endpoint + '/certificate/idp'
		)

	def upload_public_certificate(self, files):
		return self.client.post(
			self.endpoint + '/certificate/public',
			files=files
		)

	def remove_public_certificate(self):
		return self.client.delete(
			self.endpoint + '/certificate/public'
		)

	def upload_private_key(self, files):
		return self.client.post(
			self.endpoint + '/certificate/private',
			files=files
		)

	def remove_private_key(self):
		return self.client.delete(
			self.endpoint + '/certificate/private'
		)

	def get_certificate_status(self):
		return self.client.get(
			self.endpoint + '/certificate/status'
		)