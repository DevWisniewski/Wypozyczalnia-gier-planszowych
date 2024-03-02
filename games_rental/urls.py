from django.contrib import admin
from django.urls import path
from games_rental_app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', app_views.LoginView.as_view(), name="login"),
    path('logout/', app_views.LogoutView.as_view(), name="logout"),
    path('add_user/', app_views.AddUserView.as_view(), name="add_user"),
    path('my_account/', app_views.MyAccountView.as_view(), name="my_account"),
    path('game/<slug:slug>/', app_views.GameDetailsView.as_view(), name='dynamic_game_detail'),
    path('static_game_details/', app_views.StaticGameDetailsView.as_view(), name="static_game_details"),
    path('games/', app_views.GameListView.as_view(), name='game_list'),
    path('contact/', app_views.ContactView.as_view(), name='contact'),
    path('welcome/', app_views.WelcomeView.as_view(), name='welcome'),
    path('rentals/', app_views.RentalListView.as_view(), name='rental_list'),

]
