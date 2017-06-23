from src.endpoints.base import Base


class Teams(Base):
	endpoint = '/teams'

	def create_team(self, options=None):
		return self.client.post(
			self.endpoint,
			options
		)

	def get_teams(self, params=None, options=None):
		return self.client.get(
			self.endpoint,
			options=options,
			params=params
		)

	def get_team(self, team_id, options=None):
		return self.client.get(
			self.endpoint + '/' + team_id,
			options
		)

	def update_team(self, team_id, options=None):
		return self.client.put(
			self.endpoint + '/' + team_id,
			options
		)

	def delete_team(self, team_id, params=None, options=None):
		return self.client.delete(
			self.endpoint + '/' + team_id,
			options=options,
			params=params
		)

	def patch_team(self, team_id, options=None):
		return self.client.put(
			self.endpoint + '/' + team_id + '/patch',
			options
		)

	def get_team_by_name(self, name, options=None):
		return self.client.get(
			self.endpoint + '/name/' + name,
			options
		)

	def search_teams(self, options=None):
		return self.client.post(
			self.endpoint + '/search',
			options
		)

	def check_team_exists(self, name, options=None):
		return self.client.get(
			self.endpoint + '/name/' + name + '/exists',
			options
		)