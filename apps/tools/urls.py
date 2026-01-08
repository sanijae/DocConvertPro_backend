"""
URLs for Tools app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DigitalSignatureViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'digital-signatures', DigitalSignatureViewSet, basename='digital-signature')

urlpatterns = [
    path('', include(router.urls)),
    # TODO: Add conversion endpoints here
    # path('pdf-to-word/', PdfToWordView.as_view(), name='pdf-to-word'),
    # path('word-to-pdf/', WordToPdfView.as_view(), name='word-to-pdf'),
    # etc.
]
