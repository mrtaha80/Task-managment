from django.contrib import admin

from .models import Task, Comment, UserProfile

admin.site.register(Task)

admin.site.register(Comment)

admin.site.register(UserProfile)