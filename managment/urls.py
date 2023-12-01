from django.urls import path
from .views import task_list, create_task, edit_task, delete_task, user_profile , user_logout,login_view , register, edit_profile,register_done,task_detail, home

urlpatterns = [
    path('',home , name='home'),
    path('task', task_list, name='task_list'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/edit/<int:task_id>/', edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('profile/', user_profile, name='user_profile'),
    path('logout/', user_logout, name='logout'),  
    path('login/', login_view, name='login'),
    path('register/', register, name='register' ),
    path('edit_profile/', edit_profile,name = 'edit_profile'),
    path('register/done/', register_done, name='register_done'),
    path('task_details/<int:task_id>', task_detail, name = 'task_details'),
]