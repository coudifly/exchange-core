from exchange_core.models import Users
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
