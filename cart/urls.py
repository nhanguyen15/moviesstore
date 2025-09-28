from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add/', views.add, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
    path('purchase/', views.purchase, name='cart.purchase'),
    path('purchase/confirmation/<int:order_id>/', views.purchase_confirmation, name='cart.purchase_confirmation'),
    path('feedback/', views.feedback_list, name='cart.feedback_list'),  # This line is important
  ] 
