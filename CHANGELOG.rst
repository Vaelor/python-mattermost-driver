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