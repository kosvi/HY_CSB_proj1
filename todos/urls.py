from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('status', views.update_status, name='update_status'),
    path('todo', views.get_todo, name='get_todo'),
]