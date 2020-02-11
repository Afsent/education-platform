from django.urls import path
from .views import profile, BBLoginView, BBLogoutView, ChangeUserInfoView, \
    BBPasswordChangeView, RegisterDoneView, RegisterUserView
from . import views

urlpatterns = [
    path('', views.main, name='main'),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(),
         name='profile_change'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(),
         name='password_change'),
    path('accounts/register/done/', RegisterDoneView.as_view(),
         name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
]
