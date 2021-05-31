from django.urls import path
from .views import ContactCreateView

url_patterns = [
    path('', ContactCreateView.as_view())
]
