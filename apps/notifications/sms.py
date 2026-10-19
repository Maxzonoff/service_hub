"""
SMS-провайдеры для Service Hub.

Поддерживается три режима (переключаются через .env → SMS_PROVIDER):
- stub (по умолчанию) — выводит в консоль, ничего не отправляет
- smsru — отправка через SMS.ru API
- twilio — отправка через Twilio API

Клиенты инициализируются лениво — только при первом вызове send().
"""
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class BaseSMSProvider:
    """Базовый интерфейс SMS-провайдера."""

    def send(self, phone, text):
        """
        Отправляет SMS.

        Args:
            phone (str): Номер в формате +7XXXXXXXXXX или 8XXXXXXXXXX.
            text (str): Текст сообщения (до 160 символов).

        Returns:
            bool: True если отправлено успешно.
        """
        raise NotImplementedError


class StubSMSProvider(BaseSMSProvider):
    """Заглушка: пишет в консоль/лог."""

    def send(self, phone, text):
        """Логирует SMS вместо отправки."""
        logger.info(f'[SMS STUB] → {phone}: {text}')
        print(f'\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        print(f'📱 SMS → {phone}')
        print(f'   {text}')
        print(f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
        return True


class SMSRuProvider(BaseSMSProvider):
    """SMS.ru — российский SMS-провайдер (https://sms.ru)."""

    API_URL = 'https://sms.ru/sms/send'

    def send(self, phone, text):
        """Отправляет SMS через SMS.ru."""
        if not settings.SMSRU_API_ID:
            logger.warning('SMSRU_API_ID не задан, SMS не отправлен')
            return False

        # Нормализуем номер: 8XXXXXXXXXX → 7XXXXXXXXXX
        clean_phone = ''.join(c for c in phone if c.isdigit())
        if clean_phone.startswith('8'):
            clean_phone = '7' + clean_phone[1:]

        try:
            response = requests.post(
                self.API_URL,
                data={
                    'api_id': settings.SMSRU_API_ID,
                    'to': clean_phone,
                    'msg': text[:160],
                    'json': 1,
                },
                timeout=10,
            )
            data = response.json()
            if data.get('status') == 'OK':
                logger.info(f'[SMS RU] → {phone}: OK')
                return True
            logger.error(f'[SMS RU] ошибка: {data}')
            return False
        except Exception as e:
            logger.error(f'[SMS RU] исключение: {e}')
            return False


class TwilioProvider(BaseSMSProvider):
    """Twilio — международный SMS-провайдер."""

    def send(self, phone, text):
        """Отправляет SMS через Twilio."""
        if not (settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN):
            logger.warning('Twilio не настроен, SMS не отправлен')
            return False

        try:
            from twilio.rest import Client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=text[:160],
                from_=settings.TWILIO_FROM_NUMBER,
                to=phone,
            )
            logger.info(f'[SMS Twilio] → {phone}: OK')
            return True
        except Exception as e:
            logger.error(f'[SMS Twilio] исключение: {e}')
            return False


def get_sms_provider():
    """
    Возвращает провайдер SMS по настройке SMS_PROVIDER.

    Returns:
        BaseSMSProvider: экземпляр провайдера.
    """
    provider = getattr(settings, 'SMS_PROVIDER', 'stub').lower()
    if provider == 'smsru':
        return SMSRuProvider()
    if provider == 'twilio':
        return TwilioProvider()
    return StubSMSProvider()


def send_sms(phone, text):
    """
    Удобная обёртка: отправляет SMS через текущий провайдер.

    Args:
        phone (str): Номер телефона.
        text (str): Текст сообщения.

    Returns:
        bool: результат отправки.
    """
    return get_sms_provider().send(phone, text)