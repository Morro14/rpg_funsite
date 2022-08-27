from django.urls import path
from .views import PersonalPageView

urlpatterns = [
    path('', PersonalPageView.as_view()),
]