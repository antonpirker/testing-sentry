from django.urls import path
from . import views

app_name = 'hello'

urlpatterns = [
    path('', views.home, name='home'),
    path('error/', views.error_test, name='error_test'),
    path('greeting/<int:greeting_id>/increment/', views.greeting_count_increment, name='increment_count'),
]
