from django.urls import include, path
from . import views

urlpatterns = [
    path('audioapi/', views.AudioView.as_view()),
    path('device/registration/', views.DeviceRegistrationView.as_view()),
    path('device/status/', views.DeviceStatusView.as_view()),
    path('approval/', views.DeviceApprovalView.as_view()),
    path('log/', views.LogBackupAndDeleteView.as_view()),
]