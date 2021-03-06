from setuptools import setup, find_packages

__VERSION__ = '0.1'

REQUIREMENTS = [
    'django==2.*',
    'graphene-django>=2.0',
    'django-graphql-jwt',
    'whitenoise',
    'boto3',
    'django-model-utils',
    'Pillow',
    'lxml',
    'cssselect',
    'html5lib',
    'dj_database_url',
    'dj-pagination',
    'prettyconf==1.*',
    'psycopg2-binary',
    'django-extensions',
    'django-user-accounts',
    'django-anymail==1.2.1',
    'django-passwords',
    'django-storages',
    'django-jsonview',
    'django-templated-email',
    'django-extended-choices',
    'easy-thumbnails',
    'phonenumbers',
    'django-cities',
    'django-localflavor',
    'django-mathfilters',
    'django-redis-sessions',
    'django-simple-history',
    'django-admin-select2',
    'gevent>=1.2.2',
    'psycogreen',
    'gunicorn',
    'raven',
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
    python_requires='>=3.6'
)
