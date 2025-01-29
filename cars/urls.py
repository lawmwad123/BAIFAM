from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cars', views.CarViewSet)
router.register(r'orders', views.OrderViewSet, basename='order')

app_name = 'cars'

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    path('api/fetch-cars/', views.fetch_external_cars, name='fetch_external_cars'),
    
    # Frontend URls
    path('', views.CarListView.as_view(), name='car_list'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/<int:car_id>/order/', views.place_order, name='place_order'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
] 