from .base import Base


class Roles(Base):
	endpoint = '/roles'

	def get_role_by_id(self, role_id):
		return self.client.get(
			self.endpoint + '/' + role_id
		)

	def get_role_by_name(self, role_name):
		return self.client.get(
			self.endpoint + '/' + role_name
		)

	def patch_role(self, role_id, options=None):
		return self.client.put(
			self.endpoint + '/' + role_id + '/patch',
			options=options
		)

	def get_list_of_roles_by_name(self):
		return self.client.get(
			self.endpoint + '/names',
		)
