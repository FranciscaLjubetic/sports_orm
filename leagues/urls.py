from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('/sportsorm2', views.indextwo, name="indextwo"),
	path('initialize', views.make_data, name="make_data"),
]
