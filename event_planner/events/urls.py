# events/urls.py
from django.urls import path
from .views import event_list, event_detail, create_event, register_event

urlpatterns = [
    path('', event_list, name='event_list'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('create/', create_event, name='create_event'),
    path('<int:event_id>/register/', register_event, name='register_event'),
]
