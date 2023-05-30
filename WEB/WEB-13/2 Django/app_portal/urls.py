from django.contrib import admin
from django.urls import path, include
from . import views
from .apps import AppPortalConfig

app_name = AppPortalConfig.name

urlpatterns = [
    path("", views.main, name='root'),
    path("author/", views.author, name='author'),
    path("quote/", views.quote, name='quote'),
    path("tag/", views.tag, name='tag'),
    path('author_details/<int:author_id>', views.author_details, name='author_details'),
]
