from django.urls import path
from .views import UserRegistration, forgot_password, user_login, user_logout, forgot_password, post_code, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path("registration/", UserRegistration.as_view(), name="registration"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("forgot_password/", forgot_password, name="forgot_password"),
    path("get_code/", post_code, name="post_code"),
]