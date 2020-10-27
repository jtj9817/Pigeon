from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from account.api.views import (AccountCreateView, AccountDeleteView,
                               AccountDetailView, AccountListView,
                               ObtainAuthTokenView,
                               registration_view, logout_view)

app_name = "account"

urlpatterns = [
    path('register', registration_view, name="register"),
    path('login', ObtainAuthTokenView.as_view(), name="login"),
    path('logout', logout_view, name='logout'),
    path('', AccountListView.as_view()),
    path('create', AccountCreateView.as_view()),
    path('<pk>', AccountDetailView.as_view()),
    path('<pk>/delete/', AccountDeleteView.as_view())
]
