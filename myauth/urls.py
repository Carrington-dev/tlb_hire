from django.urls import  path
from myauth import views as auth_data
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", auth_data.home, name="home"),
    path("login/", auth_data.login, name="login"),
    path("register/", auth_data.register, name="register"),

    path('sign-in/', auth_data.login_view, name="login"),
    path('sign-out/', auth_data.logout_view, name="logout"),
    path('register/', auth_data.signup, name="register"),
    path('profile/', auth_data.profile, name="profile"),
     
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    
    path('user-verify-existance/<uidb64>/<token>/', auth_data.account_verification, name='account_verification'),

    path('password-reset-confirm/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
    name='password_reset_confirm'),
    path('password_reset/', auth_data.password_reset_request, name='password_reset'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
      name='password_reset_complete'),
]