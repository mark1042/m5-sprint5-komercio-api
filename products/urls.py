from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ListCreateProductView.as_view()),
    path('products/<pk>/', views.RetrievePatchProductView.as_view())
]