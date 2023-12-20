from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:filename>", views.renderFile, name="renderFile"),
    path("wiki/", views.wiki, name="wiki"),
    path("new/", views.newPage, name="newPage")
]
