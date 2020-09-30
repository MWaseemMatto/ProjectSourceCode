from django.urls import path
from . import views

app_name = 'webApp'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('baseline/', views.baseline),
    # path('userImages/', views.UserImagesList.as_view()),
]
