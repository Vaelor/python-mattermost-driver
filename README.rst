
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

The repository will try to keep up with the master of https://github.com/mattermost/mattermost-api-reference

If something changes, it is most likely to change because the official mattermost api changed.

Python 3.5 or later is required.

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
        """
        Required options

        Instead of the login/password, you can also use a personal access token.
        If you have a token, you don't need to pass login/pass.
        It is also possible to use 'auth' to pass a auth header in directly,
        for an example, see:
        https://vaelor.github.io/python-mattermost-driver/#authentication
        """
        'url': 'mattermost.server.com',
        'login_id': 'user.name',
        'password': 'verySecret',
        'token': 'YourPersonalAccessToken',

        """
        Optional options

        These options already have useful defaults or are just not needed in every case.
        In most cases, you won't need to modify these, especially the basepath.
        If you can only use a self signed/insecure certificate, you should set
        verify to False. Please double check this if you have any errors while
        using a self signed certificate!
        """
        'scheme': 'https',
        'port': 8065,
        'basepath': '/api/v4',
        'verify': True,
        'mfa_token': 'YourMFAToken',
        """
        Setting this will pass the your auth header directly to
        the request libraries 'auth' parameter.
        You probably only want that, if token or login/password is not set or
        you want to set a custom auth header.
        """
        'auth': None
        """
        If for some reasons you get regular timeouts after a while, try to decrease
        this value. The websocket will ping the server in this interval to keep the connection
        alive.
        If you have access to your server configuration, you can of course increase the timeout
        there.
        """
        'timeout': 30,

        """
        This value controls the request timeout.
        See https://python-requests.org/en/master/user/advanced/#timeouts
        for more information.
        The default value is None here, because it is the default in the
        request library, too.
        """
        'request_timeout': None,

        """
        Setting debug to True, will activate a very verbose logging.
        This also activates the logging for the requests package,
        so you can see every request you send.

        Be careful. This SHOULD NOT be active in production, because this logs a lot!
        Even the password for your account when doing driver.login()!
        """
        'debug': False
    })

    """
    Most of the requests need you to be logged in, so calling login()
    should be the first thing you do after you created your Driver instance.
    login() returns the raw response.
    If using a personal access token, you still need to run login().
    In this case, does not make a login request, but a `get_user('me')`
    and sets everything up in the client.
    """
    foo.login()

    """
    You can make api calls by using calling `Driver.endpointofchoice`.
    Using api[''] is deprecated for 5.0.0!

    So, for example, if you used `Driver.api['users'].get_user('me')` before,
    you now just do `Driver.users.get_user('me')`.
    The names of the endpoints and requests are almost identical to
    the names on the api.mattermost.com/v4 page.
    API calls always return the json the server send as a response.
    """
    foo.users.get_user_by_username('another.name')

    """
    If the api request needs additional parameters
    you can pass them to the function in the following way:
    - Path parameters are always simple parameters you pass to the function
    """
    foo.users.get_user(user_id='me')

    # - Query parameters are always passed by passing a `params` dict to the function
    foo.teams.get_teams(params={...})

    # - Request Bodies are always passed by passing an `options` dict or array to the function
    foo.channels.create_channel(options={...})

    # See the mattermost api documentation to see which parameters you need to pass.
    foo.channels.create_channel(options={
        'team_id': 'some_team_id',
        'name': 'awesome-channel',
        'display_name': 'awesome channel',
        'type': 'O'
    })

    """
    If you want to make a websocket connection to the mattermost server
    you can call the init_websocket method, passing an event_handler.
    Every Websocket event send by mattermost will be send to that event_handler.
    See the API documentation for which events are available.
    """
    foo.init_websocket(event_handler)

    # To upload a file you will need to pass a `files` dictionary
    channel_id = foo.channels.get_channel_by_name_and_team_name('team', 'channel')['id']
    file_id = foo.files.upload_file(
        channel_id=channel_id
        files={'files': (filename, open(filename))}
    )['file_infos'][0]['id']


    # track the file id and pass it in `create_post` options, to attach the file
    foo.posts.create_post(options={
        'channel_id': channel_id,
        'message': 'This is the important file',
        'file_ids': [file_id]})

    # If needed, you can make custom requests by calling `make_request`
    foo.client.make_request('post', '/endpoint', options=None, params=None, data=None, files=None, basepath=None)

    # If you want to call a webhook/execute it use the `call_webhook` method.
    # This method does not exist on the mattermost api AFAIK, I added it for ease of use.
    foo.webhooks.call_webhook('myHookId', options) # Options are optional


.. inclusion-marker-end-usage
