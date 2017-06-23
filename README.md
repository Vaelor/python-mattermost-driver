# Python Mattermost Driver (APIv4)

## Usage

```python
foo = Driver({
    'url': 'mattermost.server.com',
    'login_id': 'user.name',
    'password': 'verySecret'
})

foo.login() # Returns the response

foo.users_api().get_user_by_username('another.name') # Returns JSON

foo.channels_api().create_channel({
    'team_id': 'some_team_id',
    'name': 'awesome-channel',
    'display_name': 'awesome channel',
    'type': 'O'
})
```

See https://api.mattermost.com/v4/ to see which api requests are available.