import json
import ssl
import asyncio
import logging
import websockets

log = logging.getLogger('mattermostdriver.websocket')
log.setLevel(logging.INFO)

class Websocket:
	def __init__(self, options, token):
		self.options = options
		self._token = token

	@asyncio.coroutine
	def connect(self, event_handler):
		"""
		Connect to the websocket and authenticate it.
		When the authentication has finished, start the loop listening for messages,
		sending a ping to the server to keep the connection alive.
		:param event_handler: Every websocket event will be passed there
		:type event_handler: Function
		:return:
		"""
		context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
		if not self.options['verify']:
			context.verify_mode = ssl.CERT_NONE

		scheme = 'wss://'
		if self.options['scheme'] != 'https':
			scheme = 'ws://'
			context = None

		url = scheme + self.options['url'] + ':' + str(self.options['port']) + self.options['basepath'] + '/websocket'

		websocket = yield from websockets.connect(
			url,
			ssl=context,
		)

		yield from self._authenticate_websocket(websocket, event_handler)
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
					self._wait_for_message(websocket, event_handler),
					timeout=self.options['timeout']
				)
			except asyncio.TimeoutError:
				yield from websocket.pong()
				log.debug("Sending heartbeat...")
				continue

	@asyncio.coroutine
	def _authenticate_websocket(self, websocket, event_handler):
		"""
		Sends a authentication challenge over a websocket.
		This is not needed when we just send the cookie we got on login
		when connecting to the websocket.
		"""
		json_data = json.dumps({
			"seq": 1,
			"action": "authentication_challenge",
			"data": {
				"token": self._token
			}
		}).encode('utf8')
		yield from websocket.send(json_data)
		while True:
			message = yield from websocket.recv()
			status = json.loads(message)
			log.debug(status)
			# We want to pass the events to the event_handler already
			# because the hello event could arrive before the authentication ok response
			yield from event_handler(message)
			if ('status' in status and status['status'] == 'OK') and \
					('seq_reply' in status and status['seq_reply'] == 1):
				log.info('Websocket authentification OK')
				return True

	@asyncio.coroutine
	def _wait_for_message(self, websocket, event_handler):
		while True:
			message = yield from websocket.recv()
			yield from event_handler(message)
