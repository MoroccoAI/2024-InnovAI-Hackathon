# accounts/urls.py
from django.urls import path
from .views import CreateUserView
from .views import LoginView
from .views import LogoutView
#from .views import ProtectedEndpointView

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create-user'),
     path("login/", LoginView.as_view(), name="login"),
     # path("protected-endpoint/", ProtectedEndpointView.as_view(), name="protected-endpoint"),
      path("logout/", LogoutView.as_view(), name="logout"),
]
