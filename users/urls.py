from django.urls import path
from users.views import *

urlpatterns = [
    path("/signup", SignUpView.as_view()),
    path("/signin", SignInView.as_view()),
    path("/kakaologin", KakaoLoginView.as_view()),
    path("/mypage", MyPageDetailView.as_view())
]