from django.urls import path
from .views import profile, BBLoginView, BBLogoutView
from . import views

urlpatterns = [
    path('', views.main, name='main'),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
]
