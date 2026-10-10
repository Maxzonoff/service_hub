"""Celery-задачи для уведомлений."""

import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def notify_new_order(self, order_id):
    """Отправляет email-уведомления админу и клиенту о новом заказе."""
    try:
        from apps.orders.models import Order

        order = Order.objects.get(pk=order_id)

        # Письмо админу
        admin_subject = f'Новая заявка №{order.number}'
        admin_message = render_to_string(
            'notifications/email_admin_new_order.html', {'order': order}
        )
        send_mail(
            subject=admin_subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=admin_message,
            fail_silently=False,
        )

        # Письмо клиенту
        if order.email:
            client_subject = f'Ваша заявка №{order.number} принята'
            client_message = render_to_string(
                'notifications/email_client_new_order.html', {'order': order}
            )
            send_mail(
                subject=client_subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                html_message=client_message,
                fail_silently=True,
            )

        logger.info(f'Уведомления по заказу №{order.number} отправлены')
        return f'OK: order {order.number}'
    except Exception as exc:
        logger.error(f'Ошибка отправки уведомлений: {exc}')
        raise self.retry(exc=exc, countdown=60)


@shared_task
def send_sms(phone, text):
    """Заглушка отправки SMS. Позже подключим SMS.ru / Twilio."""
    logger.info(f'[SMS] → {phone}: {text}')
    return f'SMS to {phone} (заглушка)'
