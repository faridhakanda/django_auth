from django.urls import path
from .views import Home, UserRegister, UserLogin,UserLoginWithEmail, UserLogout, LogoutView
urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('register/', UserRegister.as_view(), name='user-register'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
    path('loginwithemail/', UserLoginWithEmail.as_view(), name='user-login_email'),
    path('logout1/', LogoutView.as_view(), name='user-logout1'),

]