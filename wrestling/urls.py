from django.urls import path
from . import views

app_name = 'wrestling'
urlpatterns = [

    # Main URL patterns
    path(route='', view=views.index, name='index'),
    path(route='home/', view=views.index, name='home'),

    # Wrestler URL patterns
    path(route='wrestlers/create/', view=views.wrestler_create, name='wrestler_create'),
    path(route='wrestlers/profile/<int:wrestler_id>/', view=views.wrestler_profile, name='wrestler_profile'),
    path(route='wrestlers/upgrade/<int:wrestler_id>/', view=views.wrestler_upgrade, name='wrestler_upgrade'),

    # Roster URL Patterns
    path(route='roster', view=views.wrestling_roster, name='wrestling_roster'),

    # Titles URL Patterns
    path(route='titles', view=views.wrestling_titles, name='wrestling_titles'),
    path(route='titles/history/<int:title_id>/', view=views.wrestling_title_history, name='wrestling_title_history'),

    # Shows URL Patterns
    path(route='shows', view=views.wrestling_shows, name='wrestling_shows'),
    
]