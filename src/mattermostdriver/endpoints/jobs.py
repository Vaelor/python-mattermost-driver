from .base import Base


class Jobs(Base):
	endpoint = '/jobs'

	def get_status_of_job(self, job_id):
		return self.client.get(
			self.endpoint + '/' + job_id + '/status'
		)

	def get_status_of_jobs(self, type, params=None):
		return self.client.get(
			self.endpoint + '/type/' + type + '/statuses',
			params=params
		)
