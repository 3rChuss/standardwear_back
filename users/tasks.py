# users/tasks.py

from celery import shared_task
from time import sleep

from utils.sendemail import send_email


@shared_task
def send_email_task(recipient_list, subject, html_content):
    sleep(20)
    print("Sending email...")
    send_email(recipient_list, subject=subject, html_content=html_content, files_to_attach=None)
