from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import handler404

from .appsConfig import getAppUrls

handler404 = 'App.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls', namespace="App")),
    path('api/', include('api.urls', namespace="api")),
    path('events/', include('events.urls', namespace="events")),
    path('facilitators/', include('facilitators.urls', namespace="facilitators")),
    path('dashboard/', include('dashboard.urls', namespace="dashboard")),
    path('accounts/login/', LoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
]

urlpatterns += getAppUrls()
