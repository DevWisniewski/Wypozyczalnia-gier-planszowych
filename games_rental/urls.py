"""
URL configuration for games_rental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from games_rental_app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', app_views.LoginView.as_view(), name="login"),
    path('logout/', app_views.LogoutView.as_view(), name="logout"),
    path('add_user/', app_views.AddUserView.as_view(), name="add_user"),
    path('my_account/', app_views.MyAccountView.as_view(), name='my_account'),

]
