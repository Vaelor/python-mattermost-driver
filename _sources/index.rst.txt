.. mattermostdriver documentation master file, created by
   sphinx-quickstart on Thu Jun 29 10:38:30 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mattermostdriver documentation
==============================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   endpoints
   changelog
   contributing


See https://github.com/Vaelor/python-mattermost-driver for the github repository.

You interact with this module mainly by using the Driver class.
If you want to access information about the logged in user, like the user id,
you can access them by using `Driver.client.userid`.

Installation
''''''''''''
.. include:: ../README.rst
    :start-after: inclusion-marker-start-install
    :end-before: inclusion-marker-end-install

Usage
'''''
.. include:: ../README.rst
    :start-after: inclusion-marker-start-usage
    :end-before: inclusion-marker-end-usage

.. include:: auth.rst

Classes
'''''''

.. automodule:: mattermostdriver
.. autoclass:: Driver
    :members:
    :undoc-members:

.. autoclass:: Client
    :members:

Exceptions that api requests can throw
''''''''''''''''''''''''''''''''''''''

.. automodule:: mattermostdriver.exceptions

.. autoclass:: InvalidOrMissingParameters

.. autoclass:: NoAccessTokenProvided

.. autoclass:: NotEnoughPermissions

.. autoclass:: ResourceNotFound

.. autoclass:: ContentTooLarge

.. autoclass:: FeatureDisabled


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
