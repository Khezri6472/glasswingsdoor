from django.urls import path

from .views import HomeView,AboutUsView

urlpatterns = [
    path('', HomeView.as_view(),name='home'),
    path('about/', AboutUsView.as_view(),name='about_us'),
]