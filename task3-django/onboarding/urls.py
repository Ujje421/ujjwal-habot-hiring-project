from django.urls import path
from .views import StudentOnboardingCreateView

urlpatterns = [
    path('submit/', StudentOnboardingCreateView.as_view(), name='student-onboarding-submit'),
]
