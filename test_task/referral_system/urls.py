from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('api-auth', AuthUserView.as_view(), name='auth'),
    path('api-users/', UserDetailView.as_view(), name='user'),
    path('api-update-user/', UserUpdateView.as_view(), name='user-update'),
    path('user_page/', TemplateView.as_view(template_name='user_page.html'), name='user_page'),
    path('logout/', user_logout, name='logout'),
]