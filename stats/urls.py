from django.urls import path
from . import views

urlpatterns = []

mainurls = [
    path('', views.index, name='index'),
    path('games/add/', views.add_game, name='add_game'),
]

htmxurls = [
    path('roster/', views.check_stats_roster, name='check_stats_roster'),
    path('games/add/validate/', views.validate_game, name='validate_game'),
]

urlpatterns += mainurls
urlpatterns += htmxurls