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
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from fundooapp import views
from notes import views as note_view
from labels import views as label_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/',
         views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('note/', note_view.Notes.as_view(), name="note"),
    path('note/<int:pk>', note_view.Notes.as_view()),
    path('label/', label_view.Labels.as_view(), name="label-post"),
    path('label/<int:pk>', label_view.Labels.as_view(), name="label"),
    path('note/archived/', note_view.ArchivedView.as_view(), name="archived"),
    path('note/archived/<int:pk>', note_view.ArchivedView.as_view()),
    path('note/pinned/', note_view.PinnedView.as_view(), name="pinned"),
    path('note/pinned/<int:pk>', note_view.PinnedView.as_view()),
    path('note/trash/', note_view.TrashView.as_view(), name="trash"),
    path('note/trash/<int:pk>', note_view.TrashView.as_view()),
    path('note/search/', note_view.SearchNote.as_view(), name="search")

]
