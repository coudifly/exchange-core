# .env

### Django settings


- [`DEFAULT_FROM_EMAIL=noreplay@example.com`](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-DEFAULT_FROM_EMAIL)
- [`SECURE_HSTS_SECONDS=0`](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SECURE_HSTS_SECONDS)
- [`ADMINS=admin@example.com`](https://docs.djangoproject.com/en/2.0/ref/settings/#adminshttps://docs.djangoproject.com/en/2.0/ref/settings/#admins)
- [`SECURE_CONTENT_TYPE_NOSNIFF=True`](https://docs.djangoproject.com/en/2.0/ref/settings/#secure-content-type-nosniff)
- [`SECURE_BROWSER_XSS_FILTER=True`](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SECURE_BROWSER_XSS_FILTER)
- [`SECURE_SSL_REDIRECT=True`](https://docs.djangoproject.com/en/2.0/ref/settings/#secure-ssl-redirect)
- [`SECURE_HSTS_PRELOAD=True`](https://docs.djangoproject.com/en/2.0/ref/settings/#secure-hsts-preload)
- [`SECURE_HSTS_INCLUDE_SUBDOMAINS=True`](https://docs.djangoproject.com/en/2.0/ref/settings/#secure-hsts-include-subdomains)
- [`SESSION_COOKIE_SECURE=True`](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SESSION_COOKIE_SECURE)
- [`SESSION_COOKIE_HTTPONLY=True`](https://docs.djangoproject.com/en/2.0/ref/settings/#session-cookie-httponly)
- [`CSRF_COOKIE_SECURE=True`](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-CSRF_COOKIE_SECURE)
- [`CSRF_COOKIE_HTTPONLY=True`](https://docs.djangoproject.com/en/2.0/a/settings/#csrf-cookie-httponly)
- [`X_FRAME_OPTIONS=DENY`](https://docs.djangoproject.com/en/2.0/ref/settings/#x-frame-options)


### Exchange Core settings

`PROJECT_NAME=Example`

Used for every place who we need to show the name of the company to the user. This variable is also available in any template as `PROJECT_NAME` context variable.

`DOMAIN=https://example.com`

Used when we need to show the domain link to the user or create full urls with `{% url %}` template tag. This variable is also available in any template as `DOMAIN` context variable.

`ACCOUNT_PASSWORD_EXPIRY=0`

Obliges the user to change its password every x days. Leave 0 (zero) for disabled it. This is a config of the [django-user-accounts](http://django-user-accounts.readthedocs.io/en/latest/usage.html?highlight=ACCOUNT_PASSWORD_EXPIRY#enabling-password-expiration) package.

`MAILGUN_API_KEY=api-thisisainvalidapikey`
`MAILGUN_SENDER_DOMAIN=mg.example.com`

[Mailgun](https://www.mailgun.com/) is the e-mail server used by our Exchange. These two configure variables above sets the Mailgun account to be used for processing all Exchange e-mail stuff.


`SESSION_SECURITY_EXPIRE_AFTER=900`

This setting tells how much time the user can stay inactive. We use this for security reasons, in case of the user forget it session opened. After the time gets end, the Django automatically logout the user. The package used for add this behavior is the [django-session-security](http://django-session-security.readthedocs.io/en/latest/full.html?highlight=SESSION_SECURITY_EXPIRE_AFTER#module-session_security.settings).

`AWS_ACCESS_KEY_ID=thisisainvalidapikey`, 
`AWS_SECRET_ACCESS_KEY=thisisainvalidapikey` 
`AWS_STORAGE_BUCKET_NAME=example`

For handling file storage in the Exchange, we use the Amazon AWS S3 service., who does the hard work for us and make the integration between S3 and Django is the [django-storages](http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html) package.

`ADMIN_URL_PREFIX=admin/`

Django admin URL from `xample.com/admin` to `example.com/abc-admin-security-url`, or something more difficult to guess. If exposed the admin can be be hacked and the Exchange data compromised.


`LANGUAGE_CSS_CLASSES=en:flag-icon-us,pt_BR:flag-icon-br,pt-br:flag-icon-br,es:flag-icon-es`

Maps a relation between a Django i18n language code and a custom css class. This is useful for build the frontend languages dropdown menu with minimum effort.

`DATABASE_URL=postgres://db_username:db_password@db_host_ip_or_domain:5432/db_database_name`

Sets the Exchange database using a URL scheme provided by the [dj-database-url](https://github.com/kennethreitz/dj-database-url) Django package.
