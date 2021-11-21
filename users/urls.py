from django.urls import path
from users.views import SignInView, SignUpView, KakaoLoginView, UserProfileView, UserProfileUploadView

app_name = 'users'
urlpatterns = [
    path("/signup"        , SignUpView.as_view()),
    path("/signin"        , SignInView.as_view()),
    path("/kakaologin"    , KakaoLoginView.as_view()),
    path("/profile"       , UserProfileView.as_view()),
    path("/profile-upload", UserProfileUploadView.as_view()),
]