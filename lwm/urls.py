from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.main, name='main'),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]