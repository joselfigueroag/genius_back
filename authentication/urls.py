from django.urls import path

from .views import UserViewSet, login_view, logout_view

urlpatterns = [
  path('api/user_register/', UserViewSet.as_view({
    "post": "create"
  })),
  path('api/login/', login_view, name="login"),
  path('api/logout/', logout_view, name="logout"),
]