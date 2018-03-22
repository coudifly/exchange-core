from setuptools import setup, find_packages


__VERSION__ = '0.1'

REQUIREMENTS = [
	'django==2.0.1', 
	'whitenoise',
	'boto3==1.5.20',
	'django-model-utils', 
	'Pillow', 
	'lxml',
	'cssselect',
	'html5lib',
	'django-two-factor-auth', 
	'dj_database_url==0.4.2', 
	'dj-pagination',
	'prettyconf', 
	'psycopg2-binary',
	'django-extensions',
	'django-user-accounts',
	'django-anymail==1.2',
	'django-passwords',
	'django-storages',
	'django-jsonview',
	'django-templated-email',
	'easy-thumbnails',
	'phonenumbers',
	'django-cities',
	'django-localflavor',
	'django-mathfilters',
	'django-redis-sessions',
	'gevent',
	'psycogreen',
	'gunicorn',
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