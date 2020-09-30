from django.urls import path
from . import views

app_name = 'treeHealth'

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('user-mobile/', views.UserList.as_view()),
    path('mobile-images/', views.UserList.as_view()),

]
