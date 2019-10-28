7.0.0
'''''
Added Endpoints:
 - `opengraph`
 - `bots`

Fixes:
 - Some pylint rules that failed have been fixed or where suppressed

Added:
 - Support for Python 3.8
 - Github actions with pylint is now active

BREAKING CHANGES:
 - Support for python 3.4 was dropped

Thanks a lot to @maxbrunet for his contribution!

6.3.1
'''''
Fixes
 - Authentication without `auth` option works again

6.3.0
'''''
Features:
 - Added authentication with .netrc

Thanks a lot to @apfeiffer1 for his contribution!

6.2.0
'''''
Fixes:
 - Fix documentation to make Json valid

Features:
 - Added a configurable timeout #40

Thanks a lot to @sahasrara62 for his contribution!

6.1.3
'''''
Fixes:
 - Add missing endpoints to the driver

Thanks a lot to @opalmer for this fix!

6.1.2
'''''
Fixes:
 - Don't parse non JSON errors #31
 - Logout before cleaning up #37

Thanks a lot to @maxbrunet for these two fixes!

6.1.1
'''''
Update requirements:
- requests@2.20.0

6.1.0
'''''
Added Endpoints:
- Reactions

Thanks a lot to @aedho3yn for this!

6.0.1
'''''
Fixes:
 - Unable to create custom emojies #33
 - Use ResourceNotFound for 404 #34

Thanks a lot to @Sakarah and @maxbrunet for these fixes!

6.0.0
'''''
POSSIBLE BREAKING CHANGES:
 Requirements have been updated:
 - websockets==6.0

This requirement (and requests from 5.0.0) are now included in the setup.py file.
If you didn't need to update before it is possible you do now,
which could cause a breaking change this time.
Not exactly sure about this, but better safe then sorry!

5.0.1
'''''
Fixes:
 - Do not try to parse responses as json when it's clear they are not. Thanks Kenan!

5.0.0
'''''
POSSIBLE BREAKING CHANGES:
 Requirements have been updated:
 - requests==2.19.1
 - websockets==5.0

Fixes:
 - The error message 'Websocket authentication failed' was not always correct

4.6.0
'''''
Release for Mattermost 5.0 api changes.

Yes, I skipped the 4.9 release because of holiday time ;-)

Added endpoints:
 - `scheme` as a whole new endpoint
 - `update_scheme_derived_roles_of_channel_member` in `channels`
 - `set_channel_scheme` in `channels`
 - `convert_channel` in `channels`
 - `update_scheme_derived_roles_of_team_member` in `teams`
 - `delete_team_icon` in `teams`
 - `set_team_scheme` in `teams`
 - `get_stats` in `users`

Fixes:
 - `create_user` in `users` was missing the query parameters

4.5.0
'''''
Release for Mattermost 4.8 api changes.

Yes this release is quite a bit behind schedule, sorry for that!

Added endpoints:
 - `status` as a whole new endpoint
 - `roles` as a whole new endpoint
 - `test_aws_s3_connection` in `system`
 - `get_configuration_environment` in `system`
 - `send_test_email` in `system`
 - `create_ephemeral_post` in `posts`
 - `get_team_icon` in `teams`
 - `set_team_icon` in `teams`

Fixes:
 - Example for `call_webhook` was incorrect #26
 - A slash was missing in `update_user_authentication_method` #27

4.4.0
'''''
Release for Mattermost 4.7 api changes.

Added endpoints:
 - `get_custom_emoji_by_name` in `emoji`
 - `search_custom_emoji` in `emoji`
 - `autocomplete_custom_emoji` in `emoji`
 - `autocomplete_channels` in `channels`

Fixes:
 - `update_user_authentication_method` was missing the request body

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
