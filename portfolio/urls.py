from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^details/(?P<currency>\w+)/(?P<percent_of_investment>\w+)/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)$',
        views.details, name='details'),
    path('charts/data', views.charts_data, name='charts_data'),
    path('calculate', views.calculate, name='calculate'),
]
