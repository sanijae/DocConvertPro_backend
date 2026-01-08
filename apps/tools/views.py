"""
Views for Tools app - PDF conversion endpoints.
Note: This is a simplified structure. The actual conversion logic from pdf_app/views.py
should be migrated here and refactored into service methods.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Document, DigitalSignature
from .serializers import DocumentSerializer, DigitalSignatureSerializer
from .services import ToolsService
from common.exceptions import ConversionLimitExceeded, SubscriptionRequired


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for Document model."""
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter documents by user."""
        return Document.objects.filter(user=self.request.user).order_by('-uploaded_at')
    
    def perform_create(self, serializer):
        """Create document with user."""
        serializer.save(user=self.request.user)


class DigitalSignatureViewSet(viewsets.ModelViewSet):
    """ViewSet for DigitalSignature model."""
    serializer_class = DigitalSignatureSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter digital signatures by user."""
        return DigitalSignature.objects.filter(user=self.request.user).order_by('-date_created')
    
    def perform_create(self, serializer):
        """Create digital signature with user."""
        serializer.save(user=self.request.user)


# Note: The actual PDF conversion views (PdfToWord, WordToPdf, etc.) should be
# added as custom actions or separate view classes. The conversion logic from
# pdf_app/views.py needs to be refactored and moved here.
