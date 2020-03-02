from django.urls import path
from yellowbird import views


urlpatterns = [
    path('user/', views.UserView.as_view()),
]