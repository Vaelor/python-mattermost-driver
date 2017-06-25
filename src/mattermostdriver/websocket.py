import json
import ssl
import asyncio
import logging
import websockets

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('mattermostdriver.websocket')


class Websocket:
	def __init__(self, options, token):
		self.options = options
		self._token = token
		self._cookie = None

	@asyncio.coroutine
	def connect(self, event_handler):
		context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
		if not self.options['verify']:
			context.verify_mode = ssl.CERT_NONE

		scheme = 'wss://'
		if self.options['scheme'] != 'https':
			scheme = 'ws://'

		url = scheme + self.options['url'] + ':' + str(self.options['port']) + self.options['basepath'] + '/websocket'

		websocket = yield from websockets.connect(
			url,
			ssl=context,
		)

		yield from self._authenticate_websocket(websocket)
		yield from self._start_loop(websocket, event_handler)

	@asyncio.coroutine
	def _start_loop(self, websocket, event_handler):
		"""
		We will listen for websockets events, sending a heartbeat/pong everytime
		we react a TimeoutError. If we don't the webserver would close the idle connection,
		forcing us to reconnect.
		"""
		log.debug('Starting websocket loop')
		while True:
			try:
				yield from asyncio.wait_for(
					self.wait_for_message(websocket, event_handler),
					timeout=self.options['timeout']
				)
			except asyncio.TimeoutError:
				yield from websocket.pong()
				log.debug("Sending heartbeat...")
				continue

	@asyncio.coroutine
	def _authenticate_websocket(self, websocket):
		"""
		Sends a authentication challenge over a websocket.
		This is not needed when we just send the cookie we got on login
		when connecting to the websocket.
		Currently (Mattermost 3.6.2) won't send all events when authenticated this way
		"""
		json_data = json.dumps({
			"seq": 1,
			"action": "authentication_challenge",
			"data": {
				"token": self._token
			}
		}).encode('utf8')
		while True:
			yield from websocket.send(json_data)
			response = yield from websocket.recv()
			status = json.loads(response)
			log.debug(status)
			if ('status' in status and status['status'] == 'OK') and \
					('seq_reply' in status and status['seq_reply'] == 1):
				log.info('Authentification OK')
				return True


	@asyncio.coroutine
	def wait_for_message(self, websocket, event_handler):
		while True:
			message = yield from websocket.recv()
			yield from event_handler(message)