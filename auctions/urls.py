from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("watchlist/add/<str:id>",views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/remove/<str:id>",views.remove_from_watchlist, name="remove_from_watchlist")
]
