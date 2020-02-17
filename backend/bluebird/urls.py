from django.urls import path
from bluebird import views


urlpatterns = [
    path('contragents/', views.ContragentsView.as_view()),
    path('contragents/<int:pk>/', views.ContragentView.as_view()),
    path('contragents/<int:pk>/packages/', views.PackagesView.as_view()),
    path('contragents/<int:pk>/packages/<int:package_id>/',
         views.PackageView.as_view()),
    path('contragents/<int:pk>/packages/<int:package_id>/other-files/',
         views.OtherFilesView.as_view()),
    path('contragents/<int:pk>/packages/<int:package_id>/other-files/\
<int:file_id>/',
         views.OtherFileView.as_view()),

    path('tasks/<str:group_id>/', views.TasksView.as_view()),
    path('norms/', views.NormsView.as_view()),
    path('sign_users/', views.SignUsersView.as_view()),
]
