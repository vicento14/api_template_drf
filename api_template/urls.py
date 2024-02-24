from django.urls import path, include
from api_template import views

urlpatterns = [
    path('user_accounts', views.UserAccountsApiView.as_view(), name="user_accounts-list"),
    path('user_accounts/<int:Id>/', views.UserAccountsDetailsApiView.as_view(), name="user_accounts-list"),
    path("", views.api_root),
]