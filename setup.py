from setuptools import setup, find_packages


__VERSION__ = '0.1'

REQUIREMENTS = [
	'django>=2.0', 
	'whitenoise',
	'boto3',
	'django-model-utils', 
	'Pillow', 
	'lxml',
	'cssselect',
	'html5lib',
	'django-two-factor-auth', 
	'dj_database_url', 
	'dj-pagination',
	'prettyconf', 
	'psycopg2-binary',
	'django-extensions',
	'django-user-accounts',
	'django-anymail',
	'django-passwords',
	'django-storages',
	'django-jsonview',
	'django-templated-email',
	'easy-thumbnails',
	'phonenumbers',
	'django-cities',
	'django-localflavor',
]

setup(
	name='exchange-core',
	version=__VERSION__,
	description='Exchange core package',
	author='Juliano Gouveia',
	author_email='juliano@neosacode.com',
	keywords='exchange, neosacode, coins',
	install_requires=REQUIREMENTS,
	packages=find_packages(exclude=[]),
	python_requires='>=3.5'
)