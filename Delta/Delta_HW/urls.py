from django.urls import path

from . import views

app_name = 'Delta_HW'
urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('users', views.users, name='users'),
    path('create_user', views.createAppuser, name='create_user'),
    path('newuser', views.userCreated, name='newuser'),
    path('search_patients', views.search_patients, name='search_patients'),
    path('viewPatient', views.viewPatient, name='viewPatient'),
    path('createPatient', views.createPatient, name='createPatient'),
]
