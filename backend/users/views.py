import hashlib
import hmac
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from users.models import User

class VerifyTelegramAuthAPIView(APIView):
    """
    Класс для проверки авторизации Telegram и создания/получения пользователя.
    """

    def get(self, request, *args, **kwargs):
        # Получаем initData из GET-параметров
        init_data = request.GET.get('initData', '')

        if not init_data:
            return Response({'error': 'No initData provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Преобразуем строку в словарь
        try:
            data_dict = dict(param.split('=') for param in init_data.split('&'))
        except ValueError:
            return Response({'error': 'Invalid initData format'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем подпись
        hash_key = hashlib.sha256(settings.BOT_TOKEN.encode()).digest()
        check_string = '\n'.join([f'{k}={v}' for k, v in sorted(data_dict.items()) if k != 'hash'])
        hash_value = hmac.new(hash_key, check_string.encode(), hashlib.sha256).hexdigest()

        if hash_value != data_dict.get('hash'):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # Проверяем время авторизации
        auth_date = int(data_dict.get('auth_date', 0))
        if time.time() - auth_date > 86400:  # Авторизация должна быть не старше 1 дня
            return Response({'error': 'Authorization expired'}, status=status.HTTP_401_UNAUTHORIZED)

        # Получаем/создаём пользователя
        tg_id = data_dict.get('id')
        if not tg_id:
            return Response({'error': 'Missing Telegram ID'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            telegram_id=tg_id,
            defaults={
                'username': data_dict.get('username', ''),
                'first_name': data_dict.get('first_name', ''),
                'last_name': data_dict.get('last_name', ''),
            }
        )

        # Возвращаем данные о пользователе
        return Response({'ok': True, 'user_id': user.id, 'created': created}, status=status.HTTP_200_OK)
