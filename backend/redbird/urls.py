from django.urls import path

from redbird import views


urlpatterns = [
    path('journal/<int:package_id>/', views.JournalView.as_view()),
    path('journal/report/', views.ReportView.as_view())
]
