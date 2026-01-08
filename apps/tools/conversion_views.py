"""
PDF conversion views - migrated from pdf_app.
These views handle all PDF conversion operations.
"""
import os
import base64
import zipfile
import subprocess
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Conversion libraries
from pdf2docx import Converter
import fitz  # PyMuPDF
from PIL import Image
import img2pdf
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import tabula
import pytesseract
import cv2
import numpy as np
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

# App imports
from apps.users.models import User
from apps.tools.models import Document, DigitalSignature
from apps.tools.serializers import DocumentSerializer, DigitalSignatureSerializer
from apps.tools.services import ToolsService
from apps.tools.digital_signature_utils import generate_key_pair
from apps.billing.selectors import BillingSelector
from common.exceptions import ConversionLimitExceeded, SubscriptionRequired


class BaseConversionView(APIView):
    """Base class for all conversion views."""
    permission_classes = [IsAuthenticated]
    
    def check_conversion_limit(self, user):
        """Check if user can perform conversion."""
        try:
            ToolsService.check_conversion_limit(user)
            return True
        except (ConversionLimitExceeded, SubscriptionRequired) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_403_FORBIDDEN if isinstance(e, ConversionLimitExceeded) else status.HTTP_402_PAYMENT_REQUIRED
            )


# PDF to Other Formats
class PdfToWordView(BaseConversionView):
    """Convert PDF to Word document."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save(user=user, file_type='pdf', conversion_type='pdf_to_word')
            
            try:
                # Convert PDF to Word
                pdf_path = document.file.path
                word_file = pdf_path.replace('.pdf', '.docx')
                cv = Converter(pdf_path)
                cv.convert(word_file, start=0, end=None)
                cv.close()
                
                # Save URL of the converted word file
                word_file_name = os.path.basename(word_file)
                document.converted_file_url = word_file.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                
                # Record conversion
                ToolsService.record_conversion(user, 'word', 'pdf_to_word')
                
                return Response({
                    'result': DocumentSerializer(document).data,
                    'file_name': word_file_name
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                document.delete()
                return Response({'error': f'Conversion failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PdfToExcelView(BaseConversionView):
    """Convert PDF to Excel."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'PDF to Excel conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class PdfToJpgView(BaseConversionView):
    """Convert PDF to JPG images."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'PDF to JPG conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class PdfToPngView(BaseConversionView):
    """Convert PDF to PNG images."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'PDF to PNG conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class PdfToJpegView(BaseConversionView):
    """Convert PDF to JPEG images."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'PDF to JPEG conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class PdfToCsvView(BaseConversionView):
    """Convert PDF to CSV."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'PDF to CSV conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class PdfToBmpView(BaseConversionView):
    """Convert PDF to BMP images."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'PDF to BMP conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class PdfToPptView(BaseConversionView):
    """Convert PDF to PowerPoint."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'PDF to PPT conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


# Other Formats to PDF
class WordToPdfView(BaseConversionView):
    """Convert Word to PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save(user=user, file_type='word', conversion_type='word_to_pdf')
            
            try:
                # Convert Word to PDF
                word_path = document.file.path
                output_file = os.path.splitext(word_path)[0] + '.pdf'
                file_path = os.path.dirname(word_path)
                
                # Use LibreOffice to convert
                subprocess.run(
                    ['soffice', '--headless', '--invisible', '--convert-to', 'pdf', '--outdir', file_path, word_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )
                
                # Save URL of the converted PDF file
                pdf_file_name = os.path.basename(output_file)
                document.converted_file_url = output_file.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                
                # Record conversion
                ToolsService.record_conversion(user, 'pdf', 'word_to_pdf')
                
                return Response({
                    'result': DocumentSerializer(document).data,
                    'file_name': pdf_file_name
                }, status=status.HTTP_201_CREATED)
            except subprocess.CalledProcessError as e:
                document.delete()
                return Response({'error': 'Conversion failed. Please ensure LibreOffice is installed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                document.delete()
                return Response({'error': f'Conversion failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExcelToPdfView(BaseConversionView):
    """Convert Excel to PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Excel to PDF conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class CsvToPdfView(BaseConversionView):
    """Convert CSV to PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'CSV to PDF conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class ImageToPdfView(BaseConversionView):
    """Convert Images to PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Image to PDF conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class PptToPdfView(BaseConversionView):
    """Convert PowerPoint to PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'PPT to PDF conversion - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


# PDF Editing
class ExtractPdfView(BaseConversionView):
    """Extract text from PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Extract PDF - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class RemovePdfPageView(BaseConversionView):
    """Remove pages from PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Remove PDF page - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class AddPdfPageView(BaseConversionView):
    """Add pages to PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Add PDF page - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class RepairPdfView(BaseConversionView):
    """Repair corrupted PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Repair PDF - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class RotatePdfView(BaseConversionView):
    """Rotate PDF pages."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Rotate PDF - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class AddWatermarkView(BaseConversionView):
    """Add watermark to PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Add watermark - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


# PDF Optimization
class CompressPdfView(BaseConversionView):
    """Compress PDF file."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Compress PDF - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class MergePdfView(BaseConversionView):
    """Merge multiple PDFs."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Merge PDF - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class SplitPdfView(BaseConversionView):
    """Split PDF into multiple files."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Split PDF - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


# PDF Security
class ProtectPdfView(BaseConversionView):
    """Protect PDF with password."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Protect PDF - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class UnProtectPdfView(BaseConversionView):
    """Remove password from PDF."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'Unprotect PDF - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class SignPdfView(BaseConversionView):
    """Sign PDF digitally."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        serializer = DigitalSignatureSerializer(data=request.data)
        if serializer.is_valid():
            digital_signature = serializer.save(user=user)
            
            try:
                file_path = digital_signature.file.path
                file_path_without_extension, ext = os.path.splitext(file_path)
                signed_pdf_path = f"{file_path_without_extension}_signed{ext}"
                signature_info_path = f"{file_path_without_extension}_signature_info.txt"
                zip_folder_path = f"{file_path_without_extension}.zip"
                name = request.data.get('name', 'Document')
                
                file_content = digital_signature.file.read()
                
                # Generate key pair and signature
                private_key, public_key, private_key_pem, public_key_pem = generate_key_pair()
                
                signature = private_key.sign(
                    file_content,
                    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                    hashes.SHA256()
                )
                
                public_key_base64 = public_key_pem.decode()
                signature_base64 = base64.b64encode(signature).decode()
                
                # Write signature info
                with open(signature_info_path, 'w') as txt_file:
                    txt_file.write(f"Public Key:\n{public_key_base64}\n\nSignature:\n{signature_base64}")
                
                # Convert signature info to PDF
                path = os.path.dirname(signature_info_path)
                signature_info_pdf = f"{file_path_without_extension}_signature_info.pdf"
                try:
                    subprocess.run(
                        ['soffice', '--headless', '--invisible', '--convert-to', 'pdf', '--outdir', path, signature_info_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True
                    )
                except subprocess.CalledProcessError:
                    return Response({'error': 'Signature info conversion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Create signed PDF and zip
                os.rename(file_path, signed_pdf_path)
                with zipfile.ZipFile(zip_folder_path, 'w') as zip_file:
                    zip_file.write(signed_pdf_path, os.path.basename(signed_pdf_path))
                    zip_file.write(signature_info_pdf, os.path.basename(signature_info_pdf))
                
                file_name = os.path.basename(zip_folder_path)
                digital_signature.name = name
                digital_signature.signature = signature
                digital_signature.signed_file_url = zip_folder_path.replace(settings.MEDIA_ROOT, '/media')
                digital_signature.save()
                
                # Record conversion
                ToolsService.record_conversion(user, 'pdf', 'sign_pdf')
                
                # Cleanup temporary files
                if os.path.exists(signed_pdf_path):
                    os.remove(signed_pdf_path)
                if os.path.exists(signature_info_pdf):
                    os.remove(signature_info_pdf)
                if os.path.exists(signature_info_path):
                    os.remove(signature_info_path)
                
                return Response({
                    'result': DigitalSignatureSerializer(digital_signature).data,
                    'file_name': file_name,
                    'public_key': public_key_base64
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                digital_signature.delete()
                return Response({'error': f'Signing failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# OCR
class OcrImageView(BaseConversionView):
    """OCR for image documents."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'OCR Image - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)


class OcrIdentityView(BaseConversionView):
    """OCR for identity documents."""
    
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        
        return Response({
            'message': 'OCR Identity - to be implemented',
            'user_id': str(user.id)
        }, status=status.HTTP_200_OK)
