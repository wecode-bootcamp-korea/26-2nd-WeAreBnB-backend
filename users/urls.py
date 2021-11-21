from django.urls import path
from users.views import SignInView, SignUpView, KakaoLoginView, ProfileImageView

app_name = 'users'
urlpatterns = [
    path("/signup", SignUpView.as_view()),
    path("/signin", SignInView.as_view()),
    path("/kakaologin", KakaoLoginView.as_view()),
    path("/edit-photo", ProfileImageView.as_view()),
]