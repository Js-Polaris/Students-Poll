from django.urls import path

from . import views

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('archive/', views.archive, name='archive'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('section/<slug:section_name>/', views.coming_soon, name='coming_soon'),
]
