from .base import Base
from .teams import Teams


class Commands(Base):
	endpoint = '/commands'

	def create_command(self, options=None):
		return self.client.post(
			self.endpoint,
			options=options
		)

	def list_commands_for_team(self, params=None):
		return self.client.get(
			self.endpoint,
			params=params
		)

	def list_autocomplete_commands(self, team_id):
		return self.client.get(
			Teams.endpoint + team_id + '/commands/autocomplete'
		)

	def update_command(self, command_id, options=None):
		return self.client.put(
			self.endpoint + command_id,
			options=options
		)

	def delete_command(self, command_id):
		return self.client.delete(
			self.endpoint + command_id
		)

	def generate_new_token(self, command_id):
		return self.client.put(
			self.endpoint + command_id + '/regen_token'
		)

	def execute_command(self, options=None):
		return self.client.post(
			self.endpoint + '/execute',
			options=options
		)