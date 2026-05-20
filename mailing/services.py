from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing


def send_recipient():
    mailing_recipient = Mailing.objects.filter(status=Mailing.NEW).all()
    for mailing in mailing_recipient:
        mailing.status = Mailing.LAUNCHED
        mailing.save()
        recipients = mailing.recipients.all()
        for recipient in recipients:

            try:
                send_mail(
                    subject=mailing.message.subject_letter,
                    message=mailing.message.body_letter,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[recipient.email],
                )
                recipient.status = True
                recipient.save()

            except Exception as e:
                recipient.server_response = str(e)
                recipient.save()
        mailing.status = Mailing.COMPLETED
        mailing.save()
