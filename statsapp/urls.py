from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('main.urls', namespace="main")),
    # path('stats/', include('stats.urls', namespace="stats")),
    path('', include('App.urls', namespace="App")),
    path('api/', include('api.urls', namespace="api")),
    # path('facilitators/', include('facilitators.urls', namespace="facilitators")),
    # path('morphers/', include('morphers.urls', namespace="morphers")),
    path('accounts/login/', LoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
]
