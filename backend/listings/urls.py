from django.urls import path
from .views import AllListingsView, ListingView, SearchView

urlpatterns = [
    path('', AllListingsView.as_view()),
    path('search', SearchView.as_view()),
    path('<slug>', ListingView.as_view())
]
