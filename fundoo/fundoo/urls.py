"""fundoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from __future__ import absolute_import
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from fundooapp import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register('users', views.UserDetailsCrud)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('home/', views.home_page, name="home"),
    path('logout/', views.logout_page, name="logout"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="C:/Users/Tarun vyda/PycharmProjects/FundooNotes/fundoo/fundooapp/templates/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="C:/Users/Tarun vyda/PycharmProjects/FundooNotes/fundoo/fundooapp/templates/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="C:/Users/Tarun vyda/PycharmProjects/FundooNotes/fundoo/fundooapp/templates/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="C:/Users/Tarun vyda/PycharmProjects/FundooNotes/fundoo/fundooapp/templates/password_reset_done.html"),
         name="password_reset_complete"),

]
