from django.urls import path
from . import views

app_name = 'hello'

urlpatterns = [
    path('', views.home, name='home'),
    path('error/', views.error_test, name='error_test'),
    path('greeting/<int:greeting_id>/increment/', views.greeting_count_increment, name='increment_count'),

    # Connection pool testing routes
    path('test/pool-stress/', views.connection_pool_stress_test, name='pool_stress_test'),
    path('test/sentry-db-interaction/', views.sentry_database_interaction_test, name='sentry_db_test'),
    path('test/connection-leak/', views.connection_leak_simulation, name='connection_leak_test'),
]
