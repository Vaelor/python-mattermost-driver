from .base import Base


class System(Base):
	def check_system_health(self):
		return self.client.get(
			'/system/ping'
		)

	def recycle_database_connection(self):
		return self.client.post(
			'/database/recycle'
		)

	def send_test_email(self):
		return self.client.post(
			'/email/test'
		)

	def get_configuration(self):
		return self.client.get(
			'/config'
		)

	def update_configuration(self):
		return self.client.put(
			'/config'
		)

	def reload_configuration(self):
		return self.client.post(
			'/config/reload'
		)

	def get_client_configuration(self, params):
		return self.client.get(
			'/config/client',
			params=params
		)

	def upload_license_file(self, files):
		return self.client.post(
			'/license',
			files=files
		)

	def remove_license_file(self):
		return self.client.delete(
			'/license'
		)

	def get_client_license(self, params):
		return self.client.get(
			'/license/client',
			params=params
		)

	def get_audits(self, params):
		return self.client.get(
			'/audits',
			params=params
		)

	def invalidate_all_caches(self):
		return self.client.post(
			'/caches/invalidate',
		)

	def get_logs(self, params):
		return self.client.get(
			'/logs',
			params=params
		)

	def add_log_message(self, options):
		return self.client.post(
			'/logs',
			options=options
		)

	def get_webrtc_token(self):
		return self.client.get(
			'/webrtc/token'
		)

	def get_analytics(self, params):
		return self.client.get(
			'/analytics/old',
			params=params
		)
