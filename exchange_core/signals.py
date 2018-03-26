from exchange_core.models import Users, Currencies, Accounts
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from templated_email import send_templated_mail

DOCUMENTS_TEMPLATED_EMAILS = {
    Users.STATUS.approved_documentation: 'approved_documentation',
    Users.STATUS.disapproved_documentation: 'disapproved_documentation'
}


@receiver(post_save, sender=Users)
def send_documents_email(sender, instance, **kwargs):
    if instance.status == instance._original_status:
        return
    if instance.status not in DOCUMENTS_TEMPLATED_EMAILS:
        return

    send_templated_mail(
        template_name=DOCUMENTS_TEMPLATED_EMAILS[instance.status],
        from_email=settings.DEFAULT_FROM_EMAIL,
        context={'user': instance, 'project_name': settings.PROJECT_NAME},
        recipient_list=[instance.email]
    )


# Cria as contas do usuário
@receiver(post_save, sender=Users, dispatch_uid='create_user_accounts')
def create_user_accounts(sender, instance, created, **kwargs):
    if created:
        currencies = Currencies.objects.all()

        with transaction.atomic():
            for currency in currencies:
                account = Accounts()
                account.user = instance
                account.currency = currency
                account.save()


@receiver(post_save, sender=Currencies, dispatch_uid='create_currency_user_accounts')
def create_currency_user_accounts(sender, instance, created, **kwargs):
    with transaction.atomic():
        # Filtra pelos usuários que ainda não tem essa conta
        users = Users.objects.exclude(accounts__currency=instance)

        for user in users:
            account = Accounts()
            account.currency = instance
            account.user = user
            account.save()