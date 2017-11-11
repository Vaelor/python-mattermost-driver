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