class Base:
	def __init__(self, client):
		self.client = client

	def build_query(self, query):
		if query is None:
			query_string = ''
		else:
			query_string = '?'
			for key, value in query.items():
				if not query_string.endswith('?'):
					query_string = query_string + '&'
					query_string = query_string + key + '=' + value
		return query_string
