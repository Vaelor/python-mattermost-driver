4.3.2
'''''
Fixes
 - https://github.com/Vaelor/python-mattermost-driver/issues/24

4.3.1
'''''
Added endpoints
 - `create_user_access_token` in `/users`

4.2.1
'''''
Fixes
 - https://github.com/Vaelor/python-mattermost-driver/pull/21
 - https://github.com/Vaelor/python-mattermost-driver/pull/22

Thanks to @dan-klasson for these!!

4.2.0
'''''
Release for Mattermost 4.6 api changes.

Added endpoints:
 - `get_user_access_token` in `/users`
 - `search_tokens` in `/users`
 - `update_user_authentication_method` in `/users`

4.1.0
'''''
This release mostly improves on the documentation.

The sphinx theme has been changed to the readthedocs one.

This also adds a `debug` option, which enables a very verbose log output.
Be careful, as everything, even your mattermost password when you log in,
is readable in the log output!
This is definitely not for production usage!

4.0.2
'''''
This release makes some internal changes on how the endpoints are accessed.

Since this works much better then using `api['endpoint']` has been deprecated for the next Major release.

Fixes https://github.com/Vaelor/python-mattermost-driver/issues/5


4.0.1
'''''
The release 4.0.0 was not quite correct, since the following changes did not really happen, only the api documentation for mattermost 4.4.0 changed.

.. code::

    Endpoints moved from team to channels https://github.com/mattermost/mattermost-api-reference/pull/298/files
     - get_public_channels
     - get_deleted_channels
     - search_channels


4.0.0
'''''
This has some changes related to Mattermost 4.4

BREAKING CHANGES:
 - Endpoints moved from `team` to `channels` https://github.com/mattermost/mattermost-api-reference/pull/298/files
   - `get_public_channels`
   - `get_deleted_channels`
   - `search_channels`

Added endpoints:
 - `revoke_all_user_sessions` in `/users`
 - `disable_personal_access_token` in `/users`
 - `enable_personal_access_token` in `/users`

Also, you can now access the api endpoints directly,
without using `Driver.api['endpoint']`, instead you can
`Driver.users.get_user('me')`.
Both ways are working, so no breaking change there.
Related Issue for this: https://github.com/Vaelor/python-mattermost-driver/issues/5

3.0.1
'''''
Thanks to SmartHoneyBee!
 - Changed setup of the logger #14

3.0.0
'''''
 - Removed python 3.3 from supported versions
 - Add data_retention endpoint

2.3.0
'''''
Make a `basepath` available in `Client.make_request()`.
This is mainly needed for calling `/hooks`.

2.2.0
'''''
Support for personal access tokens and MFA Token.

2.0.0
'''''

Breaking change for file uploads.
Instead of a `data` dict containing all formdata,
a `files` dict is in the following endpoints

 - emoji
   - `create_custom_emoji()` takes `emoji_name` additionally to a `files` dict

 - files
   - `upload_file()` takes `channel_id` additionally to a `files` dict

 - brand
   - `upload_brand_image()`

 - saml
   - `upload_idp_certificate()`
   - `upload_public_certificate()`
   - `upload_private_key()`

 - system
   - `upload_license_file()`

 - users
   - `set_user_profile_image()`

See the documentation for an example.