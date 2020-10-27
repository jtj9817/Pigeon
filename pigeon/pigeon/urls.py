"""pigeon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers
from django.contrib.auth import logout
urlpatterns = [
    path('admin/', admin.site.urls),
]

# Django-REST Framework Configuration
router = routers.SimpleRouter()

urlpatterns += [
    path('', include(router.urls)),
    path('logout', logout, name="logout"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Add Account API urls
    path('api/account/', include('account.api.urls', 'account_api')),
    # Add Pigeon_Messaging API urls
    path('api/messages/', include('pigeon_messaging.api.urls', 'pigeon_messaging_api')),
    # Add Pigeon_Posts API URLs
    path('api/posts/', include('pigeon_posts.api.urls', 'pigeon_posts_api')),
    path('rest-auth/', include('rest_auth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls'))
]

urlpatterns += router.urls

# Base URL
# urlpatterns += [
#    path('', RedirectView.as_view(url='/pigeon/', permanent=True))
# ]


# Allow serving static files for development purposes
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
