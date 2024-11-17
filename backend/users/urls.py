from django.urls import path

from users.views import VerifyTelegramAuthAPIView

app_name = 'users'

urlpatterns = [
    path('api/verify_telegram_auth/', VerifyTelegramAuthAPIView.as_view()),
]
