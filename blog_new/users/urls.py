from django.contrib.auth import views as auth_views
from django.urls import path


from .views import UserLoginView, UserInnerLoginView, UserRegisterView, UserProfileView, PasswordChangeSuccess, logout, UserPasswordChangeView


app_name = 'users'

urlpatterns = [
    # path('subscribe/', NewsletterSignUpView.as_view(), name='subscribe'),
#     path('unsubscribe/', newsletter_unsubscribe, name='unsubscribe'),
    path('user-login/', UserLoginView.as_view(), name='login'),
    path('login/', UserInnerLoginView.as_view(), name='user_login_inner'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('password-change-done/', PasswordChangeSuccess.as_view(), name='password_success'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/registration/password-reset.html'),
         name='password_reset'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/registration/password-reset-done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/registration/password-reset-confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/registration/password-reset-complete.html'),
         name='password_reset_complete'),
#     path('subscribe-success/', NewsletterSignUpSuccessView.as_view(), name='subscribe_success'),
#     path('<int:pk>/password/', PasswordsChangeView.as_view(template_name='users/registration/change-password.html'), name='password_change'),
    path('password-change/', UserPasswordChangeView.as_view(template_name='users/registration/change-password.html'), name='password_change'),
]
