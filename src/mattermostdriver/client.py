"""
Client for the driver, which holds information about the logged in user
and actually makes the requests to the mattermost server
"""

import logging
import httpx

from .exceptions import (
    InvalidOrMissingParameters,
    NoAccessTokenProvided,
    NotEnoughPermissions,
    ResourceNotFound,
    MethodNotAllowed,
    ContentTooLarge,
    FeatureDisabled,
)

log = logging.getLogger("mattermostdriver.websocket")
log.setLevel(logging.INFO)


class BaseClient:
    def __init__(self, options):
        self._url = self._make_url(options["scheme"], options["url"], options["port"], options["basepath"])
        self._scheme = options["scheme"]
        self._basepath = options["basepath"]
        self._port = options["port"]
        self._auth = options["auth"]
        if options["debug"]:
            self.activate_verbose_logging()

        self._options = options
        self._token = ""
        self._cookies = None
        self._userid = ""
        self._username = ""
        self._proxies = None
        if options["proxy"]:
            self._proxies = {"all://": options["proxy"]}

    @staticmethod
    def _make_url(scheme, url, port, basepath):
        return f"{scheme:s}://{url:s}:{port:d}{basepath:s}"

    @staticmethod
    def activate_verbose_logging(level=logging.DEBUG):
        log.setLevel(level)
        # enable trace level logging in httpx
        httpx_log = logging.getLogger("httpx")
        httpx_log.setLevel("TRACE")
        httpx_log.propagate = True

    @property
    def userid(self):
        """
        :return: The user id of the logged in user
        """
        return self._userid

    @userid.setter
    def userid(self, user_id):
        self._userid = user_id

    @property
    def username(self):
        """
        :return: The username of the logged in user. If none, returns an emtpy string.
        """
        return self._username

    @property
    def request_timeout(self):
        """
        :return: The configured timeout for the requests
        """
        return self._options["request_timeout"]

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def url(self):
        return self._url

    @property
    def cookies(self):
        """
        :return: The cookie given on login
        """
        return self._cookies

    @cookies.setter
    def cookies(self, cookies):
        self._cookies = cookies

    @property
    def token(self):
        """
        :return: The token for the login
        """
        return self._token

    @token.setter
    def token(self, t):
        self._token = t

    def auth_header(self):
        if self._auth:
            return None
        if self._token == "":
            return {}
        return {"Authorization": "Bearer {token:s}".format(token=self._token)}

    def _build_request(self, method, options=None, params=None, data=None, files=None, basepath=None):
        if params is None:
            params = {}
        if data is None:
            data = {}
        if basepath:
            url = self._make_url(self._options["scheme"], self._options["url"], self._options["port"], basepath)
        else:
            url = self.url

        request_params = {"headers": self.auth_header(), "timeout": self.request_timeout}

        if params is not None:
            request_params["params"] = params

        if method in ("post", "put"):
            if options is not None:
                request_params["json"] = options
            if data is not None:
                request_params["data"] = data
            if files is not None:
                request_params["files"] = files

        if self._auth is not None:
            request_params["auth"] = self._auth()

        return self._get_request_method(method, self.client), url, request_params

    @staticmethod
    def _check_response(response):
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                data = e.response.json()
                message = data.get("message", data)
            except ValueError:
                log.debug("Could not convert response to json")
                message = response.text
            log.error(message)

            if e.response.status_code == 400:
                raise InvalidOrMissingParameters(message) from None
            elif e.response.status_code == 401:
                raise NoAccessTokenProvided(message) from None
            elif e.response.status_code == 403:
                raise NotEnoughPermissions(message) from None
            elif e.response.status_code == 404:
                raise ResourceNotFound(message) from None
            elif e.response.status_code == 405:
                raise MethodNotAllowed(message) from None
            elif e.response.status_code == 413:
                raise ContentTooLarge(message) from None
            elif e.response.status_code == 501:
                raise FeatureDisabled(message) from None
            else:
                raise

        log.debug(response)

    @staticmethod
    def _get_request_method(method, client):
        method = method.lower()
        if method == "post":
            return client.post
        elif method == "put":
            return client.put
        elif method == "delete":
            return client.delete
        else:
            return client.get


class Client(BaseClient):
    def __init__(self, options):
        super().__init__(options)
        self.client = httpx.Client(
            http2=options.get("http2", False),
            proxies=self._proxies,
            verify=options.get("verify", True),
        )

    def make_request(self, method, endpoint, options=None, params=None, data=None, files=None, basepath=None):
        request, url, request_params = self._build_request(method, options, params, data, files, basepath)
        response = request(url + endpoint, **request_params)

        self._check_response(response)
        return response

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, *exc_info):
        return self.client.__exit__(*exc_info)

    def get(self, endpoint, options=None, params=None):
        response = self.make_request("get", endpoint, options=options, params=params)

        if response.headers["Content-Type"] != "application/json":
            log.debug("Response is not application/json, returning raw response")
            return response

        try:
            return response.json()
        except ValueError:
            log.debug("Could not convert response to json, returning raw response")
            return response

    def post(self, endpoint, options=None, params=None, data=None, files=None):
        return self.make_request("post", endpoint, options=options, params=params, data=data, files=files).json()

    def put(self, endpoint, options=None, params=None, data=None):
        return self.make_request("put", endpoint, options=options, params=params, data=data).json()

    def delete(self, endpoint, options=None, params=None, data=None):
        return self.make_request("delete", endpoint, options=options, params=params, data=data).json()


class AsyncClient(BaseClient):
    def __init__(self, options):
        super().__init__(options)
        self.client = httpx.AsyncClient(
            http2=options.get("http2", False),
            proxies=self._proxies,
            verify=options.get("verify", True),
        )

    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *exc_info):
        return await self.client.__aexit__(*exc_info)

    async def make_request(self, method, endpoint, options=None, params=None, data=None, files=None, basepath=None):
        request, url, request_params = self._build_request(method, options, params, data, files, basepath)
        response = await request(url + endpoint, **request_params)

        self._check_response(response)
        return response

    async def get(self, endpoint, options=None, params=None):
        response = await self.make_request("get", endpoint, options=options, params=params)

        if response.headers["Content-Type"] != "application/json":
            log.debug("Response is not application/json, returning raw response")
            return response

        try:
            return response.json()
        except ValueError:
            log.debug("Could not convert response to json, returning raw response")
            return response

    async def post(self, endpoint, options=None, params=None, data=None, files=None):
        response = await self.make_request("post", endpoint, options=options, params=params, data=data, files=files)
        return response.json()

    async def put(self, endpoint, options=None, params=None, data=None):
        response = await self.make_request("put", endpoint, options=options, params=params, data=data)
        return response.json()

    async def delete(self, endpoint, options=None, params=None, data=None):
        response = await self.make_request("delete", endpoint, options=options, params=params, data=data)
        return response.json()
