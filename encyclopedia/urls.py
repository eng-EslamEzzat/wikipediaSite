from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.contents, name="contents"),
    path("search", views.search, name="search"),
    path("creatNewPage", views.creatNewPage, name="creatNewPage"),
    path("edit/<str:title>", views.editContents, name="editContents"),
    path("randomPage", views.randomPage, name="randomPage")
]
