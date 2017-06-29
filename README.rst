
.. image:: https://img.shields.io/pypi/v/mattermostdriver.svg
    :target: https://pypi.python.org/pypi/mattermostdriver

.. image:: https://img.shields.io/pypi/l/mattermostdriver.svg
    :target: https://pypi.python.org/pypi/mattermostdriver

.. image:: https://img.shields.io/pypi/pyversions/mattermostdriver.svg
    :target: https://pypi.python.org/pypi/mattermostdriver

Python Mattermost Driver (APIv4)
================================

Info
----

Breaking changes may happen but I try to avoid them.

Mostly a bit more documentation to do now.

If something changes, it is most likely to change because the official mattermost api changed.

Installation
------------

.. inclusion-marker-start-install

``pip install mattermostdriver``

.. inclusion-marker-end-install

Documentation
-------------
Documentation can be found at https://vaelor.github.io/python-mattermost-driver/ .

Usage
-----

.. inclusion-marker-start-usage

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

    # Most of the requests need you to be logged in, so calling login()
    # should be the first thing you do after you created your Driver instance.
    # login() returns the raw response
    foo.login()

    # You can make api calls by using api['yourendpointofchoice'].
    # The names of the endpoints and requests are almost identical to
    # the names on the api.mattermost.com/v4 page.
    # API calls always return the json the server send as a response.
    foo.api['users'].get_user_by_username('another.name')

    # If the api request needs additional parameters
    # you can pass them to the function in the following way:
    # - Path parameters are always simple parameters you pass to the function
    foo.api['user'].get_user(user_id='me')

    # - Query parameters are always passed by passing a `params` dict to the function
    foo.api['teams'].get_teams(params={...})

    # - Request Bodies are always passed by passing an `options` dict or array to the function
    foo.api['channels'].create_channel(options={...})

    # See the mattermost api documentation to see which parameters you need to pass.
    foo.api['channels'].create_channel(options={
        'team_id': 'some_team_id',
        'name': 'awesome-channel',
        'display_name': 'awesome channel',
        'type': 'O'
    })

    # If you want to make a websocket connection to the mattermost server
    # you can call the init_websocket method, passing an event_handler.
    # Every Websocket event send by mattermost will be send to that event_handler.
    # See the API documentation for which events are available.
    foo.init_websocket(event_handler)

.. inclusion-marker-end-usage

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
