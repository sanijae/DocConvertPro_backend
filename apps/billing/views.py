"""
Views for Billing app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import SubscriptionPlan, Subscription, Payment
from .serializers import SubscriptionPlanSerializer, SubscriptionSerializer, PaymentSerializer
from .services import BillingService
from .selectors import BillingSelector


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for SubscriptionPlan."""
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]  # Allow public access to view plans
    
    def get_queryset(self):
        """Filter plans by type if specified."""
        queryset = super().get_queryset()
        plan_type = self.request.query_params.get('plan_type')
        if plan_type:
            queryset = queryset.filter(plan_type=plan_type)
        return queryset


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for Subscription."""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter subscriptions by user."""
        queryset = Subscription.objects.filter(user=self.request.user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        """Create subscription with user."""
        plan_id = serializer.validated_data.get('plan').id
        plan = SubscriptionPlan.objects.get(id=plan_id)
        payment_method = self.request.data.get('payment_method', 'paystack')
        billing_cycle = self.request.data.get('billing_cycle', 'monthly')
        
        # Validate payment method
        valid_methods = [choice[0] for choice in Payment.PAYMENT_METHODS]
        if payment_method not in valid_methods:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({
                'payment_method': f'Invalid payment method. Must be one of: {", ".join(valid_methods)}'
            })
        
        subscription, payment = BillingService.create_subscription(
            user=self.request.user,
            plan=plan,
            payment_method=payment_method,
            billing_cycle=billing_cycle
        )
        
        serializer.instance = subscription
    
    def create(self, request, *args, **kwargs):
        """Create subscription and return with payment info."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        subscription = serializer.instance
        payment = subscription.payments.first()
        
        return Response({
            'subscription': SubscriptionSerializer(subscription).data,
            'payment': PaymentSerializer(payment).data if payment else None
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a subscription."""
        subscription = self.get_object()
        if subscription.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        subscription = BillingService.activate_subscription(subscription)
        return Response(SubscriptionSerializer(subscription).data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a subscription."""
        subscription = self.get_object()
        if subscription.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        subscription = BillingService.cancel_subscription(subscription)
        return Response(SubscriptionSerializer(subscription).data)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current active subscription."""
        subscription = BillingSelector.get_user_subscription(request.user)
        if subscription:
            return Response(SubscriptionSerializer(subscription).data)
        return Response({'message': 'No active subscription'}, status=status.HTTP_404_NOT_FOUND)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Payment."""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter payments by user."""
        queryset = Payment.objects.filter(user=self.request.user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by payment method
        payment_method = self.request.query_params.get('payment_method')
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Update payment status (for webhooks/callbacks).
        Requires payment to belong to authenticated user.
        """
        payment = self.get_object()
        if payment.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        transaction_id = request.data.get('transaction_id')
        
        if not new_status:
            return Response({'error': 'status is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            updated_payment = BillingService.update_payment_status(
                payment=payment,
                status=new_status,
                transaction_id=transaction_id
            )
            return Response(PaymentSerializer(updated_payment).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
