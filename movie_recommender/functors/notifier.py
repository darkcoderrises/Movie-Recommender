from django.core.mail import send_mail
from .singleton import Singleton


class Notifier(Singleton):
    @staticmethod
    def mail(user, subject, body):
        """
        Usage: Notifier.mail(args)
        :param user: User model(s) to send the email to
        :param subject: Subject of the mail
        :param body: Body of the mail
        :return:
        """
        return send_mail(
            subject,
            body,
            "no-reply@booker.com",
            [user.email if not isinstance(user, list) else [u.email for u in user]],
            fail_silently=False,
        )

    @staticmethod
    def sms(user, body):
        return True
