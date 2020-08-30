from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("artist", views.artist, name='artist'),
    path("artist/<str:id>", views.oneartist, name='artist'),
    path('album/', views.album, name='album'),
    path('album/<str:id>', views.onealbum, name='album'),
    path('profile/<int:id>', views.profile, name="profile"),
    path('addsong', views.addsong, name="addsong")
]
