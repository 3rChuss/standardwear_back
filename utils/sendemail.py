
from django.core.mail import EmailMultiAlternatives, mail_admins
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def send_email(
        to_email: str,
        subject: str,
        html_content: str,
        files_to_attach: list = None,
) -> None:
    try:
        sender_email = f'{_("Standard-Wear - Tu tienda de Merchandasing ECOlogica")} <{settings.EMAIL_HOST_USER}>'
        headers = {'Reply-To': sender_email, 'format': 'flowed'}
        msg = EmailMultiAlternatives(
            subject, from_email=sender_email, to=[to_email], headers=headers)

        msg.attach_alternative(html_content, "text/html")

        if files_to_attach is not None:
            for file_to_attach in files_to_attach:
                try:
                    with open(str(settings.BASE_DIR) + file_to_attach, 'rb') as f:
                        # attach file
                        msg.attach(f.name, f.read())
                except Exception as e:
                    print(e)

        msg.send()
    except Exception as e:
        # send error to admin
        error_email = f'{_("Error sending email")}: {e} \n\n' \
                      f'{_("To")}: {to_email} \n' \
                      f'{_("Subject")}: {subject} \n' \
                      f'{_("Content")}: {html_content} \n' \
                      f'{_("Files")}: {files_to_attach} \n'

        mail_admins(_("Error sending email"), error_email)
        pass
