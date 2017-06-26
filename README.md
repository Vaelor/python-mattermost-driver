# Python Mattermost Driver (APIv4)

## Info

Currently WIP / Unstable

## Installation
NOT WORKING YET!
`pip install mattermostdriver`

## Usage

```python
from mattermostdriver import Driver

foo = Driver({
    # Required options
    'url': 'mattermost.server.com',
    'login_id': 'user.name',
    'password': 'verySecret',
    # Optional / defaults to
	'scheme': 'https',
	'port': 8065,
	'basepath': '/api/v4',
	# Use False if self signed/insecure certificate
	'verify': True,
	# The interval the websocket will ping the server to keep the connection alive
	'timeout': 30,
})

foo.login() # Returns the response

foo.api.users.get_user_by_username('another.name') # Returns JSON

foo.api.channels.create_channel({
    'team_id': 'some_team_id',
    'name': 'awesome-channel',
    'display_name': 'awesome channel',
    'type': 'O'
})

foo.init_websocket(event_handler)
```

##### Available endpoints:
 - users
 - teams
 - channels
 - posts
 - files
 - preferences
 - system
 - webhooks
 - commands
 - compliance
 - cluster
 - brand
 - oauth
 - saml
 - ldap
 - jobs

See https://api.mattermost.com/v4/ to see which api requests are available.
