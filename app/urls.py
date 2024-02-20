from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'app'

urlpatterns = [
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', views.homepage, name='homepage'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/add_task', add_task, name='add_task'),
    path('diary/', diary_list, name='diary_list'),
    path('diary/add', add_diary_entry, name='add_diary_entry'),
    path('profile/', view_user_profile, name='view_user_profile'),
    path('profile/week/', user_profile_week, name='user_profile_week'),
    path('profile/edit/', edit_user_profile, name='edit_user_profile'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('diary/edit/<int:entry_id>/', views.edit_diary_entry, name='edit_diary_entry'),
    path('diary/delete/<int:diary_entry_id>/', views.delete_diary_entry, name='delete_diary_entry'),
]




