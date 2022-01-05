from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api_v1'

urlpatterns = [
    path('users/all/', views.LocalUsersList.as_view(), name='users-list-all'),
    path('users/add-new/', views.LocalUserAdd.as_view(), name='users-add'),
    path('users/<int:pk>/', views.LocalUserDetail.as_view(), name='users-detail'),
    path('users/<int:pk>/setpassword/', views.LocalUserSetPassword.as_view(), name='users-setpassword'),
    path('users/change-password/', views.LocalUserChangePassword.as_view(), name='users-change-password'),
    path('users/<int:pk>/provide-superuser/', views.LocalUserProvidingSuperUserAccess.as_view(),
         name='users-provide-superuser'),
]

urlpatterns = format_suffix_patterns(urlpatterns)


