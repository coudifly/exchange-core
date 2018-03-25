import swapper

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django_otp.plugins.otp_static.models import StaticDevice
from two_factor.models import PhoneDevice
from account.models import (
    Account,
    AccountDeletion,
    EmailAddress,
    PasswordExpiry,
    PasswordHistory,
    SignupCode,
)
from cities.models import (
	Continent, 
	Country, 
	Region, 
	Subregion, 
	City, 
	District,
	PostalCode, 
	AlternativeName
)

admin.site.unregister(Account)
admin.site.unregister(SignupCode)
admin.site.unregister(AccountDeletion)
admin.site.unregister(EmailAddress)
admin.site.unregister(PasswordExpiry)
admin.site.unregister(PasswordHistory)
admin.site.unregister(Continent)
admin.site.unregister(Country)
admin.site.unregister(Region )
admin.site.unregister(Subregion)
admin.site.unregister(City)
admin.site.unregister(District)
admin.site.unregister(PostalCode)
admin.site.unregister(AlternativeName)
admin.site.unregister(PhoneDevice)
admin.site.unregister(StaticDevice)