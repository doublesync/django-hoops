from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [

    # /polls/
    path('', views.index, name='index'),

    # Poll URL Patterns
    path('view/<int:id>/', views.view_poll, name='view_poll'),
    path('create/', views.create_poll, name='create_poll'),
]