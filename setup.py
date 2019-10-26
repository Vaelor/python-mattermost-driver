#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

from setuptools import setup, find_packages

full_version = ''

root_dir = os.path.abspath(os.path.dirname(__file__))

readme_file = os.path.join(root_dir, 'README.rst')
with open(readme_file, encoding='utf-8') as f:
	long_description = f.read()

version_module = os.path.join(root_dir, 'src', 'mattermostdriver', 'version.py')
with open(version_module, encoding='utf-8') as f:
	exec(f.read())


setup(
	name='mattermostdriver',
	version=full_version,
	description='A Python Mattermost Driver',
	long_description=long_description,
	url='https://github.com/Vaelor/python-mattermost-driver',
	author='Christian Plümer',
	author_email='github@kuuku.net',
	license='MIT',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	],
	package_dir={'': 'src'},
	packages=find_packages('src'),
	python_requires=">=3.5",
	install_requires=[
		'websockets>=6',
		'requests>=2.19'
	],
)
