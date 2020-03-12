from django.urls import path

from yellowbird import views

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('user/', views.UserView.as_view()),
    path('user/login/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('user/login/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
]