Python Mattermost Driver (APIv4)
================================

Info
----

Currently WIP / Unstable
Breaking Changes are likely!

Installation
------------

``pip install mattermostdriver``

Usage
-----

.. code:: python

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

    foo.api['users'].get_user_by_username('another.name') # Returns JSON

    foo.api['channels'].create_channel(options={
        'team_id': 'some_team_id',
        'name': 'awesome-channel',
        'display_name': 'awesome channel',
        'type': 'O'
    })

    foo.init_websocket(event_handler)


If the mattermost api expects you to...

- ... add a request body, use ``options`` with either a dict or array/list

.. code:: python
    foo.api['channels'].create_channel(options={...})


- ... add query parameters, use ``params`` with a dict

.. code:: python
    foo.api['teams'].get_teams(params={...})


- ... add a path parameter, use a normal parameter

.. code:: python
    foo.api['user'].get_user(user_id='me')


Available endpoints:
''''''''''''''''''''

-  users
-  teams
-  channels
-  posts
-  files
-  preferences
-  system
-  webhooks
-  commands
-  compliance
-  cluster
-  brand
-  oauth
-  saml
-  ldap
-  jobs

See https://api.mattermost.com/v4/ to see which api requests are
available.
