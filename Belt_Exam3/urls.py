"""
Definition of urls for HandyHelper2.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.models import User, Wish
from app.views import Wish_View

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)
class WishAdmin(admin.ModelAdmin):
    pass
admin.site.register(Wish, WishAdmin)

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('wishes/create/', views.wish_create, name='create wish'),
    path('wishes/like/<int:id>/', views.wish_like, name='like wish'),
    path('wishes/granted/<int:id>/', views.wish_granted, name='granted wish'),
    path('wishes/new/', views.wish_new, name='new wish'),
    path('wishes/remove/<int:id>/', views.wish_remove, name='remove wish'),
    path('wishes/edit/<int:id>/', Wish_View.as_view(), name='edit wish'),
    path('wishes/update/<int:id>/', Wish_View.as_view(), name='update wish'),
    path('wishes/stats/', views.wish_stats, name='wish stats'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
]