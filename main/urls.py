from django.urls import path
from .views import profile, LWMLoginView, LWMLogoutView, ChangeUserInfoView, \
    LWMPasswordChangeView, RegisterDoneView, RegisterUserView, user_activate, \
    main, DeleteUserView, by_rubric, detail, profile_lesson_detail, \
    profile_lesson_add, profile_lesson_change, profile_lesson_delete, project

urlpatterns = [
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('', main, name='main'),
    path('projects/<int:pk>/', project, name='project'),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/profile/change/<int:pk>/', profile_lesson_change,
         name='profile_lesson_change'),
    path('accounts/profile/delete/<int:pk>/', profile_lesson_delete,
         name='profile_lesson_delete'),
    path('accounts/profile/add/', profile_lesson_add,
         name='profile_lesson_add'),
    path('accounts/profile/<int:pk>/', profile_lesson_detail,
         name='profile_lesson_detail'),
    path('accounts/login/', LWMLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', LWMLogoutView.as_view(), name='logout'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(),
         name='profile_change'),
    path('accounts/password/change/', LWMPasswordChangeView.as_view(),
         name='password_change'),
    path('accounts/register/done/', RegisterDoneView.as_view(),
         name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/activate/<str:sign>/', user_activate,
         name='register_activate'),
    path('accounts/profile/delete/', DeleteUserView.as_view(),
         name='profile_delete'),
]
