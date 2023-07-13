from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [

    # /polls/
    path('', views.index, name='index'),

    # Event URL Patterns
    path('view/<int:id>/', views.view_event, name='view_event'),
    path('edit/<int:id>/', views.edit_event, name='edit_event'),
    path('create/', views.create_event, name='create_event'),

    # AJAX URL Patterns
    path('add/', views.add_event, name='add_event'),
    path('add_entree/', views.add_entree, name='add_entree'),
    path('remove_entree/', views.remove_entree, name='remove_entree'),

]