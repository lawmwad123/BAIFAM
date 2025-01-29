from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Car, Order, CarImage
from .serializers import CarSerializer, OrderSerializer
from .services import CarAPIService
from django.contrib import messages
from django.db import models
from decimal import Decimal

# Create your views here.

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'make', 'model', 'year']
    ordering_fields = ['price', 'year', 'created_at']

    def create(self, request, *args, **kwargs):
        # Create car in external API first
        success, result = CarAPIService.create_car(request.data)
        if not success:
            return Response({'error': result}, status=status.HTTP_400_BAD_REQUEST)
        
        # Then create in our database
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        car = self.get_object()
        car.available = not car.available
        car.save()
        return Response({'status': 'success'})

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Frontend Views
class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 12

    def get_queryset(self):
        queryset = Car.objects.filter(available=True)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                models.Q(name__icontains=search_query) |
                models.Q(make__icontains=search_query) |
                models.Q(model__icontains=search_query) |
                models.Q(year__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Try to fetch latest cars from API
        success, message = CarAPIService.fetch_cars()
        if not success:
            messages.warning(self.request, f"Could not fetch latest cars: {message}")
        return context

class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

@login_required
def place_order(request, car_id):
    car = get_object_or_404(Car, id=car_id, available=True)
    if request.method == 'POST':
        # Set total_amount explicitly, using 0 as default if price is None
        total_amount = car.price if car.price is not None else Decimal('0.00')
        
        order = Order.objects.create(
            user=request.user,
            car=car,
            total_amount=total_amount
        )
        messages.success(request, f"order placed successfully! Order #{order.id}")
        return redirect('cars:order_detail', pk=order.id)
    return render(request, 'cars/place_order.html', {'car': car})

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'cars/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    return render(request, 'cars/order_detail.html', {'order': order})

def fetch_external_cars(request):
    """
    Manually trigger fetching cars from external API this i s better approach
    """
    success, message = CarAPIService.fetch_cars()
    if success:
        return JsonResponse({'status': 'success', 'message': message})
    return JsonResponse({'status': 'error', 'message': message}, status=500)
