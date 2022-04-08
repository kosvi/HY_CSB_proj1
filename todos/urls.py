from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('status', views.update_status, name='update_status'),
    path('update', views.update_todo, name='update_todo'),
    path('delete', views.delete_todo, name='delete_todo'),
    path('todo', views.get_todo, name='get_todo'),
    path('reset', views.reset_db_endpoint, name='reset_db'),
]