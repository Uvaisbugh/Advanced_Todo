from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.homepage, name='home'),
    path('sign/', views.signup, name='sign'),
    path('log/', views.loginn, name='login'),
    path('toggle_complete/<int:task_id>/', views.toggle_complete, name='toggle_complete'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('signout/', views.signout, name='signout'),
    
]
