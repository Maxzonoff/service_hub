"""Celery-задачи для уведомлений: email + SMS."""
import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .sms import send_sms

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# EMAIL
# ─────────────────────────────────────────────
@shared_task(bind=True, max_retries=3)
def notify_new_order(self, order_id):
    """Email-уведомления админу и клиенту о новом заказе."""
    try:
        from apps.orders.models import Order
        order = Order.objects.get(pk=order_id)

        # Админу
        admin_subject = f'Новая заявка №{order.number}'
        admin_message = render_to_string('notifications/email_admin_new_order.html', {'order': order})
        send_mail(
            subject=admin_subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=admin_message,
            fail_silently=False,
        )

        # Клиенту
        if order.email:
            client_subject = f'Ваша заявка №{order.number} принята'
            client_message = render_to_string('notifications/email_client_new_order.html', {'order': order})
            send_mail(
                subject=client_subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                html_message=client_message,
                fail_silently=True,
            )

        logger.info(f'Email-уведомления по заказу №{order.number} отправлены')
        return f'OK: order {order.number}'
    except Exception as exc:
        logger.error(f'Ошибка email-уведомлений: {exc}')
        raise self.retry(exc=exc, countdown=60)


# ─────────────────────────────────────────────
# SMS
# ─────────────────────────────────────────────
@shared_task(bind=True, max_retries=3)
def send_sms_order_created(self, order_id):
    """SMS клиенту и админу при создании заказа."""
    try:
        from apps.orders.models import Order
        order = Order.objects.get(pk=order_id)

        # Клиенту
        if order.phone:
            send_sms(
                order.phone,
                f'Service Hub: заявка №{order.number} принята. Перезвоним в течение 15 минут.',
            )

        # Админу (если настроен ADMIN_PHONE)
        admin_phone = getattr(settings, 'ADMIN_PHONE', '')
        if admin_phone:
            send_sms(
                admin_phone,
                f'НОВАЯ ЗАЯВКА №{order.number}: {order.name}, {order.phone}. {order.service or ""}',
            )

        logger.info(f'SMS по заказу №{order.number} отправлены')
        return f'OK: sms order {order.number}'
    except Exception as exc:
        logger.error(f'Ошибка SMS при создании заказа: {exc}')
        raise self.retry(exc=exc, countdown=60)


@shared_task
def send_sms_order_status_changed(order_id, new_status):
    """SMS клиенту при смене статуса заказа."""
    try:
        from apps.orders.models import Order
        order = Order.objects.get(pk=order_id)

        status_messages = {
            'in_progress': f'Ваш заказ №{order.number} принят в работу. Мастер скоро свяжется.',
            'done': f'Заказ №{order.number} выполнен. Спасибо, что выбрали Service Hub!',
            'canceled': f'Заказ №{order.number} отменён. Если это ошибка — позвоните нам.',
        }
        text = status_messages.get(new_status)
        if not text:
            logger.warning(f'Нет сообщения для статуса {new_status}')
            return f'SKIP: status {new_status}'

        if order.phone:
            send_sms(order.phone, text)

        logger.info(f'SMS о статусе {new_status} отправлен клиенту заказа №{order.number}')
        return f'OK: status sms for {order.number}'
    except Exception as exc:
        logger.error(f'Ошибка SMS при смене статуса: {exc}')
        return f'ERROR: {exc}'


# ─────────────────────────────────────────────
# Утилита: ручная отправка SMS
# ─────────────────────────────────────────────
@shared_task
def send_sms_custom(phone, text):
    """Произвольная отправка SMS (для админки/тестов)."""
    result = send_sms(phone, text)
    return f'OK: {phone}' if result else f'FAILED: {phone}'