from django.urls import path
from .views import ActivationView, LoginView, RegistrationView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/',  RegistrationView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

]
