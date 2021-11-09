from django.urls import path
# from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("list/<int:number>", views.list, name="list"),
    path("comment/<int:number>", views.comment, name="comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("endbid/", views.endbid, name="endbid"),
    path("history/", views.history, name="history"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:name>", views.category, name="category")
]
