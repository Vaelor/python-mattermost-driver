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
		if options['debug']:
			log.setLevel(logging.DEBUG)
		self._token = token
		self._alive = False

	async def connect(self, event_handler):
		"""
		Connect to the websocket and authenticate it.
		When the authentication has finished, start the loop listening for messages,
		sending a ping to the server to keep the connection alive.

		:param event_handler: Every websocket event will be passed there. Takes one argument.
		:type event_handler: Function(message)
		:return:
		"""
		context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
		if not self.options['verify']:
			context.verify_mode = ssl.CERT_NONE

		scheme = 'wss://'
		if self.options['scheme'] != 'https':
			scheme = 'ws://'
			context = None

		url = '{scheme:s}{url:s}:{port:s}{basepath:s}/websocket'.format(
			scheme=scheme,
			url=self.options['url'],
			port=str(self.options['port']),
			basepath=self.options['basepath']
		)

		self._alive = True

		while True:
			try:
				kw_args = {}
				if self.options['websocket_kw_args'] is not None:
					kw_args = self.options['websocket_kw_args']
				websocket = await websockets.connect(
					url,
					ssl=context,
					**kw_args,
				)
				await self._authenticate_websocket(websocket, event_handler)
				while self._alive:
					try:
						await self._start_loop(websocket, event_handler)
					except websockets.ConnectionClosedError:
						break
				if (not self.options['keepalive']) or (not self._alive):
					break
			except Exception as e:
				log.warning(f"Failed to establish websocket connection: {e}")
				await asyncio.sleep(self.options['keepalive_delay'])

	async def _start_loop(self, websocket, event_handler):
		"""
		We will listen for websockets events, sending a heartbeat/pong everytime
		we react a TimeoutError. If we don't the webserver would close the idle connection,
		forcing us to reconnect.
		"""
		log.debug('Starting websocket loop')
		while self._alive:
			try:
				await asyncio.wait_for(
					self._wait_for_message(websocket, event_handler),
					timeout=self.options['timeout']
				)
			except asyncio.TimeoutError:
				await websocket.pong()
				log.debug("Sending heartbeat...")
				continue

	def disconnect(self):
		"""Sets `self._alive` to False so the loop in `self._start_loop` will finish."""
		log.info("Disconnecting websocket")
		self._alive = False

	async def _authenticate_websocket(self, websocket, event_handler):
		"""
		Sends a authentication challenge over a websocket.
		This is not needed when we just send the cookie we got on login
		when connecting to the websocket.
		"""
		log.debug('Authenticating websocket')
		json_data = json.dumps({
			"seq": 1,
			"action": "authentication_challenge",
			"data": {
				"token": self._token
			}
		})
		await websocket.send(json_data)
		while True:
			message = await websocket.recv()
			status = json.loads(message)
			log.debug(status)
			# We want to pass the events to the event_handler already
			# because the hello event could arrive before the authentication ok response
			await event_handler(message)
			if ('event' in status and status['event'] == 'hello') and \
					('seq' in status and status['seq'] == 0):
				log.info('Websocket authentification OK')
				return True
			log.error('Websocket authentification failed')

	async def _wait_for_message(self, websocket, event_handler):
		log.debug('Waiting for messages on websocket')
		while self._alive:
			message = await websocket.recv()
			await event_handler(message)
