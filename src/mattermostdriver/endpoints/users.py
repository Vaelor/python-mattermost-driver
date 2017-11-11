from .base import Base


class Users(Base):
	endpoint = '/users'

	def login_user(self, options):
		return self.client.make_request('post', self.endpoint + '/login', options)

	def logout_user(self):
		return self.client.post(self.endpoint + '/logout')

	def create_user(self, options=None):
		return self.client.post(self.endpoint, options)

	def get_users(self, params=None):
		return self.client.get(	self.endpoint, params=params)

	def get_users_by_ids(self, options=None):
		return self.client.post(
			self.endpoint + '/ids',
			options
		)

	def get_users_by_usernames(self, options=None):
		return self.client.post(
			self.endpoint + '/usernames',
			options
		)

	def search_users(self, options=None):
		return self.client.post(
			self.endpoint + '/search',
			options
		)

	def autocomplete_users(self, params=None):
		return self.client.get(
			self.endpoint + '/autocomplete',
			params=params
		)

	def get_user(self, user_id):
		return self.client.get(
			self.endpoint + '/' + user_id
		)

	def update_user(self, user_id, options=None):
		return self.client.put(
			self.endpoint + '/' + user_id,
			options
		)

	def deactivate_user(self, user_id):
		return self.client.delete(
			self.endpoint + '/' + user_id
		)

	def patch_user(self, user_id, options=None):
		return self.client.put(
			self.endpoint + '/' + user_id + '/patch',
			options
		)

	def update_user_role(self, user_id, options=None):
		return self.client.put(
			self.endpoint + '/' + user_id + '/roles',
			options
		)

	def update_user_active_status(self, user_id, options=None):
		return self.client.put(
			self.endpoint + '/' + user_id + '/active',
			options
		)

	def get_user_profile_image(self, user_id):
		return self.client.get(
			self.endpoint + '/' + user_id + '/image'
		)

	def set_user_profile_image(self, user_id, files):
		return self.client.post(
			self.endpoint + '/' + user_id + '/image',
			files=files
		)

	def get_user_by_username(self, username):
		return self.client.get(
			self.endpoint + '/username/' + username
		)

	def reset_password(self, options=None):
		return self.client.post(
			self.endpoint + '/password/reset',
			options
		)

	def update_user_mfa(self, user_id, options=None):
		return self.client.put(
			self.endpoint + '/' + user_id + '/mfa',
			options
		)

	def generate_mfa(self, user_id):
		return self.client.post(
			self.endpoint + '/' + user_id + '/mfa/generate'
		)

	def check_mfa(self, options=None):
		return self.client.post(
			self.endpoint + '/mfa',
			options
		)

	def update_user_password(self, user_id, options=None):
		return self.client.put(
			self.endpoint + '/' + user_id + '/password',
			options
		)

	def send_password_reset_mail(self, options=None):
		return self.client.post(
			self.endpoint + '/password/reset/send',
			options
		)

	def get_user_by_email(self, email):
		return self.client.get(
			self.endpoint + '/email/' + email
		)

	def get_user_sessions(self, user_id):
		return self.client.get(
			self.endpoint + '/' + user_id + '/sessions'
		)

	def revoke_user_session(self, user_id, options=None):
		return self.client.post(
			self.endpoint + '/' + user_id + '/sessions/revoke',
			options
		)

	def revoke_all_user_sessions(self, user_id):
		return self.client.post(
			self.endpoint + '/' + user_id + '/sessions/revoke/all',
		)

	def attach_mobile_device(self, options=None):
		return self.client.put(
			self.endpoint + '/sessions/device',
			options
		)

	def get_user_audits(self, user_id):
		return self.client.get(
			self.endpoint + '/' + user_id + '/audits'
		)

	def verify_user_email(self, options=None):
		return self.client.post(
			self.endpoint + '/email/verify',
			options
		)

	def send_verification_mail(self, options=None):
		return self.client.post(
			self.endpoint + '/email/verify/send',
			options
		)

	def switch_login_method(self, options=None):
		return self.client.post(
			self.endpoint + '/login/switch',
			options
		)

	def disable_personal_access_token(self, options=None):
		return self.client.post(
			self.endpoint + '/tokens/disable',
			options
		)

	def enable_personal_access_token(self, options=None):
		return self.client.post(
			self.endpoint + '/tokens/enable',
			options
		)
