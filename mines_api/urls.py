from django.urls import path

from . import views

app_name = 'mines_api'

urlpatterns = [
    path('game/new', views.game_new, name='game_new'),
    path('game/get/<int:game_id>', views.game_get, name='game_get'),
    path('game/<int:game_id>/left_click/<int:x>/<int:y>', views.game_left_click, name='game_left_click'),
    path('game/<int:game_id>/right_click/<int:x>/<int:y>', views.game_right_click, name='game_right_click'),
]
