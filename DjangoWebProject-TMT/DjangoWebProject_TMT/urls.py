"""
Definition of urls for DjangoWebProject_TMT.
"""

from datetime import datetime
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.urls import path, include
from django.views.generic.base import TemplateView


# path to .html files
urlpatterns = [
    path('', views.home, name='home'),
    # path('contact/', views.contact, name='contact'),
    # path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('signup/', views.user_signup, name='signup'),
    path('task/', views.TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', views.TaskDetail.as_view(), name='task'),
    path('task-create/', views.TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', views.TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', views.DeleteView.as_view(), name='task-delete'),
]