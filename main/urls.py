from django.urls import path
from .views import profile, BBLoginView, BBLogoutView, ChangeUserInfoView, \
    BBPasswordChangeView, RegisterDoneView, RegisterUserView, user_activate, \
    main, DeleteUserView, by_rubric, detail, profile_lesson_detail, \
    profile_lesson_add

urlpatterns = [
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('', main, name='main'),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/profile/add/', profile_lesson_add,
         name='profile_lesson_add'),
    path('accounts/profile/<int:pk>/', profile_lesson_detail,
         name='profile_lesson_detail'),
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
    path('accounts/register/activate/<str:sign>/', user_activate,
         name='register_activate'),
    path('accounts/profile/delete/', DeleteUserView.as_view(),
         name='profile_delete'),
]
