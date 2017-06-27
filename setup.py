import os.path
import sys

from setuptools import setup, find_packages

root_dir = os.path.abspath(os.path.dirname(__file__))

readme_file = os.path.join(root_dir, 'README.rst')
with open(readme_file, encoding='utf-8') as f:
	long_description = f.read()

py_version = sys.version_info[:2]

if py_version < (3, 3):
	raise Exception("python-mattermost-driver requires Python >= 3.3.")

setup(
	name='mattermostdriver',
	version='0.4.0',
	description='A Python Mattermost Driver',
	long_description=long_description,
	url='https://github.com/Vaelor/python-mattermost-driver',
	author='Christian Plümer',
	author_email='github@kuuku.net',
	license='MIT',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
	package_dir={'': 'src'},
	packages=find_packages('src'),
	extras_require={
		':python_version=="3.3"': ['asyncio'],
	},
	install_requires=[
		'websockets>=3.2',
		'requests>=2.1'
	],
)
