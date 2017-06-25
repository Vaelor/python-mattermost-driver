from .base import Base


class Compliance(Base):
	endpoint = '/compliance'

	def create_report(self):
		return self.client.post(
			self.endpoint + '/reports'
		)

	def get_reports(self, params=None):
		return self.client.get(
			self.endpoint + '/reports',
			params=params
		)

	def get_report(self, report_id):
		return self.client.get(
			self.endpoint + '/reports/' + report_id
		)

	def download_report(self, report_id):
		return self.client.get(
			self.endpoint + '/reports/' + report_id + '/download'
		)