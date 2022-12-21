from django.urls import path,include,re_path
from django.urls import re_path as url
from . import views

urlpatterns = [
    url('compiler/(?P<pk>\w{0,50})/',views.test,name="test"),
   path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('',views.createprojet,name="createprojet"),
    url('save/(?P<pk>\w{0,50})/',views.save,name="save"),

    path('liste_Collaboration/',views.liste_Collaboration,name="liste_Collaboration"),
    path('Collaboration/<str:pk>/',views.Collaboratio_projet,name="Collaboratio_projet"),
    path('accepter_Collaboration/<str:pk>/',views.accepter_Collaboration,name="accepter_Collaboration"),

    path('delete_project/<str:pk>/', views.delete_project, name="delete_project"),
    path('delete_Collaboration/<str:pk>/', views.delete_Collaboration, name="delete_Collaboration"),
    path('delete_Collaboration_members/<str:pk_user>/<str:pk>/', views.delete_Collaboration_members, name="delete_Collaboration_members"),


]
