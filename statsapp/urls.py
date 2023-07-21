from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import handler404

handler404 = 'App.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls', namespace="App")),
    path('api/', include('api.urls', namespace="api")),
    # path('facilitators/', include('facilitators.urls', namespace="facilitators")),
    # path('morphers/', include('morphers.urls', namespace="morphers")),
    path('accounts/login/', LoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
]
