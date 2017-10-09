from .base import Base


class Webhooks(Base):
	endpoint = '/hooks'

	def create_incoming_hook(self, options):
		return self.client.post(
			self.endpoint + '/incoming',
			options=options
		)

	def list_incoming_hooks(self, params):
		return self.client.get(
			self.endpoint + '/incoming',
			params=params
		)

	def get_incoming_hook(self, hook_id):
		return self.client.get(
			self.endpoint + '/incoming/' + hook_id
		)

	def update_incoming_hook(self, hook_id, options):
		return self.client.put(
			self.endpoint + '/incoming/' + hook_id,
			options=options
		)

	def create_outgoing_hook(self, options):
		return self.client.post(
			self.endpoint + '/outgoing',
			options=options
		)

	def list_outgoing_hooks(self, params):
		return self.client.get(
			self.endpoint + '/outgoing',
			params=params
		)

	def get_outgoing_hook(self, hook_id):
		return self.client.get(
			self.endpoint + '/outgoing/' + hook_id
		)

	def delete_outgoing_hook(self, hook_id):
		return self.client.delete(
			self.endpoint + '/outgoing/' + hook_id
		)

	def update_outgoing_hook(self, hook_id, options):
		return self.client.put(
			self.endpoint + '/outgoing/' + hook_id,
			options=options
		)

	def regenerate_token_outgoing_hook(self, hook_id):
		return self.client.put(
			self.endpoint + '/outgoing/' + hook_id + '/regen_token'
		)

	def call_webhook(self, hook_id, options=None):
		return self.client.make_request('post', '/' + hook_id, options=options, basepath='/hooks')
