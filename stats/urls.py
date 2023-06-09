from django.urls import path
from . import views

app_name = 'stats'
urlpatterns = []

mainurls = [
    path('', views.index, name='index'),
    path('games/add/', views.add_game, name='add_game'),
    path('games/view/<int:id>/', views.view_game, name='view_game'),
    path('seasons/view/<int:id>/', views.view_season, name='view_season'),
    path('seasons/averages/view/<int:id>/', views.view_season_stats, name='view_season_stats'),
]

htmxurls = [
    path('roster/', views.check_stats_roster, name='check_stats_roster'),
    path('games/add/validate/', views.validate_game, name='validate_game'),
    path('seasons/averages/sort/', views.sort_stats, name='sort_stats'),
    path('seasons/averages/options/', views.find_options, name='find_options'),
]

urlpatterns += mainurls
urlpatterns += htmxurls