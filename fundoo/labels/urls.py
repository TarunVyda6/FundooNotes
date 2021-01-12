from django.urls import path
from . import views as label_view


urlpatterns = [

    path('label/', label_view.Labels.as_view(), name="label-post"),
    path('label/<int:pk>', label_view.Labels.as_view(), name="label"),
]