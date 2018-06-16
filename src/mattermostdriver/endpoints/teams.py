import warnings

from .base import Base
from .users import Users


class Teams(Base):
	endpoint = '/teams'

	def create_team(self, options=None):
		return self.client.post(
			self.endpoint,
			options
		)

	def get_teams(self, params=None):
		return self.client.get(
			self.endpoint,
			params=params
		)

	def get_team(self, team_id):
		return self.client.get(
			self.endpoint + '/' + team_id,
		)

	def update_team(self, team_id, options=None):
		return self.client.put(
			self.endpoint + '/' + team_id,
			options
		)

	def delete_team(self, team_id, params=None):
		return self.client.delete(
			self.endpoint + '/' + team_id,
			params=params
		)

	def patch_team(self, team_id, options=None):
		return self.client.put(
			self.endpoint + '/' + team_id + '/patch',
			options
		)

	def get_team_by_name(self, name):
		return self.client.get(
			self.endpoint + '/name/' + name
		)

	def search_teams(self, options=None):
		return self.client.post(
			self.endpoint + '/search',
			options
		)

	def check_team_exists(self, name):
		return self.client.get(
			self.endpoint + '/name/' + name + '/exists'
		)

	def get_user_teams(self, user_id):
		return self.client.get(
			Users.endpoint + '/' + user_id + '/teams'
		)

	def get_team_members(self, team_id, params=None):
		return self.client.get(
			self.endpoint + '/' + team_id + '/members',
			params=params
		)

	def add_user_to_team(self, team_id, options=None):
		return self.client.post(
			self.endpoint + '/' + team_id + '/members',
			options=options
		)

	def add_user_to_team_from_invite(self, params=None):
		return self.client.post(
			self.endpoint + '/members/invite',
			params=params
		)

	def add_multiple_users_to_team(self, team_id, options=None):
		return self.client.post(
			self.endpoint + '/' + team_id + '/members/batch',
			options=options
		)

	def get_team_members_for_user(self, user_id):
		return self.client.get(
			Users.endpoint + '/' + user_id + '/teams/members'
		)

	def get_team_member(self, team_id, user_id):
		return self.client.get(
			self.endpoint + '/' + team_id + '/members/' + user_id
		)

	def remove_user_from_team(self, team_id, user_id):
		return self.client.delete(
			self.endpoint + '/' + team_id + '/members/' + user_id
		)

	def get_team_members_by_id(self, team_id, options=None):
		return self.client.post(
			self.endpoint + '/' + team_id + '/members/ids',
			options
		)

	def get_team_stats(self, team_id):
		return self.client.get(
			self.endpoint + '/' + team_id + '/stats'
		)

	def update_team_member_roles(self, team_id, user_id, options=None):
		return self.client.put(
			self.endpoint + '/' + team_id + '/members/' + user_id + '/roles',
			options
		)

	def get_team_unreads_for_user(self, user_id, params=None):
		return self.client.get(
			Users.endpoint + '/' + user_id + '/teams/unread',
			params=params
		)

	def get_unreads_for_team(self, user_id, team_id):
		return self.client.get(
			Users.endpoint + '/' + user_id + '/teams/' + team_id + '/unread',
		)

	def invite_users_to_team_by_mail(self, team_id, options=None):
		return self.client.post(
			self.endpoint + '/' + team_id + '/invite/email',
			options
		)

	def import_team_from_other_app(self, team_id, data=None):
		return self.client.post(
			self.endpoint + '/' + team_id + '/import',
			data=data
		)

	def get_invite_info_for_team(self, invite_id):
		return self.client.get(
			self.endpoint + '/invite/' + invite_id,
		)

	def get_public_channels(self, team_id, params=None):
		warnings.warn(
			'Using deprecated endpoint Teams.get_public_channels(). ' +
			'Use Channels.get_public_channels() instead.',
			DeprecationWarning
		)
		return self.client.get(
			self.endpoint + '/' + team_id + '/channels',
			params=params
		)

	def get_deleted_channels(self, team_id, params=None):
		warnings.warn(
			'Using deprecated endpoint Teams.get_deleted_channels(). ' +
			'Use Channels.get_deleted_channels() instead.',
			DeprecationWarning
		)
		return self.client.get(
			self.endpoint + '/' + team_id + '/channels/deleted',
			params=params
		)

	def search_channels(self, team_id, options=None):
		warnings.warn(
			'Using deprecated endpoint Teams.search_channels(). Use Channels.search_channels() instead.',
			DeprecationWarning
		)
		return self.client.post(
			self.endpoint + '/' + team_id + '/channels/search',
			options=options
		)

	def get_team_icon(self, team_id):
		return self.client.get(
			self.endpoint + '/' + team_id + '/image'
		)

	def set_team_icon(self, team_id, file):
		return self.client.post(
			self.endpoint + '/' + team_id + '/image',
			files=file
		)

	def update_scheme_derived_roles_of_team_member(self, team_id, user_id, options=None):
		return self.client.put(
			self.endpoint + '/' + team_id + '/members/' + user_id + '/schemeRoles',
			options=options
		)

	def delete_team_icon(self, team_id):
		self.client.delete(
			self.endpoint + '/' + team_id + '/image'
		)

	def set_team_scheme(self, team_id):
		return self.client.put(
			self.endpoint + '/' + team_id + '/scheme'
		)
