"""
URLs for Tools app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DigitalSignatureViewSet
from .conversion_views import (
    # PDF to Other Formats
    PdfToWordView, PdfToExcelView, PdfToJpgView, PdfToPngView,
    PdfToJpegView, PdfToCsvView, PdfToBmpView, PdfToPptView,
    # Other Formats to PDF
    WordToPdfView, ExcelToPdfView, CsvToPdfView, ImageToPdfView, PptToPdfView,
    # PDF Editing
    ExtractPdfView, RemovePdfPageView, AddPdfPageView, RepairPdfView,
    RotatePdfView, AddWatermarkView,
    # PDF Optimization
    CompressPdfView, MergePdfView, SplitPdfView,
    # PDF Security
    ProtectPdfView, UnProtectPdfView, SignPdfView,
    # OCR
    OcrImageView, OcrIdentityView,
)

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'digital-signatures', DigitalSignatureViewSet, basename='digital-signature')

urlpatterns = [
    path('', include(router.urls)),
    
    # PDF to Other Formats
    path('pdf-to-word/', PdfToWordView.as_view(), name='pdf-to-word'),
    path('pdf-to-excel/', PdfToExcelView.as_view(), name='pdf-to-excel'),
    path('pdf-to-jpg/', PdfToJpgView.as_view(), name='pdf-to-jpg'),
    path('pdf-to-png/', PdfToPngView.as_view(), name='pdf-to-png'),
    path('pdf-to-jpeg/', PdfToJpegView.as_view(), name='pdf-to-jpeg'),
    path('pdf-to-csv/', PdfToCsvView.as_view(), name='pdf-to-csv'),
    path('pdf-to-bmp/', PdfToBmpView.as_view(), name='pdf-to-bmp'),
    path('pdf-to-ppt/', PdfToPptView.as_view(), name='pdf-to-ppt'),
    
    # Other Formats to PDF
    path('word-to-pdf/', WordToPdfView.as_view(), name='word-to-pdf'),
    path('excel-to-pdf/', ExcelToPdfView.as_view(), name='excel-to-pdf'),
    path('csv-to-pdf/', CsvToPdfView.as_view(), name='csv-to-pdf'),
    path('image-to-pdf/', ImageToPdfView.as_view(), name='image-to-pdf'),
    path('ppt-to-pdf/', PptToPdfView.as_view(), name='ppt-to-pdf'),
    
    # PDF Editing
    path('extract-pdf/', ExtractPdfView.as_view(), name='extract-pdf'),
    path('remove-pdf-page/', RemovePdfPageView.as_view(), name='remove-pdf-page'),
    path('add-pdf-page/', AddPdfPageView.as_view(), name='add-pdf-page'),
    path('repair-pdf/', RepairPdfView.as_view(), name='repair-pdf'),
    path('rotate-pdf/', RotatePdfView.as_view(), name='rotate-pdf'),
    path('add-watermark/', AddWatermarkView.as_view(), name='add-watermark'),
    
    # PDF Optimization
    path('compress-pdf/', CompressPdfView.as_view(), name='compress-pdf'),
    path('merge-pdf/', MergePdfView.as_view(), name='merge-pdf'),
    path('split-pdf/', SplitPdfView.as_view(), name='split-pdf'),
    
    # PDF Security
    path('protect-pdf/', ProtectPdfView.as_view(), name='protect-pdf'),
    path('unprotect-pdf/', UnProtectPdfView.as_view(), name='unprotect-pdf'),
    path('sign-pdf/', SignPdfView.as_view(), name='sign-pdf'),
    
    # OCR
    path('ocr-image/', OcrImageView.as_view(), name='ocr-image'),
    path('ocr-identity/', OcrIdentityView.as_view(), name='ocr-identity'),
]
