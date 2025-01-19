

from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [
    path('api/', include('product.urls')),
    path('api/user/', include('user.urls')),

]
