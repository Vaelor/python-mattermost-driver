from requests import HTTPError


class InvalidOrMissingParameters(HTTPError):
	"""
	Raised when mattermost returns a
	400 Invalid or missing parameters in URL or request body
	"""


class NoAccessTokenProvided(HTTPError):
	"""
	Raised when mattermost returns a
	401 No access token provided
	"""


class NotEnoughPermissions(HTTPError):
	"""
	Raised when mattermost returns a
	403 Do not have appropriate permissions
	"""


class ResourceNotFound(HTTPError):
	"""
	Raised when mattermost returns a
	404 Resource not found
	"""


class ContentTooLarge(HTTPError):
	"""
	Raised when mattermost returns a
	413 Content too large
	"""


class FeatureDisabled(HTTPError):
	"""
	Raised when mattermost returns a
	501 Feature is disabled
	"""
