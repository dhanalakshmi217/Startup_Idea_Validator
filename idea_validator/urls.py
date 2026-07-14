from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('validate/', views.validate_idea, name='validate_idea'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('report/<int:pk>/delete/', views.delete_report, name='delete_report'),
]
