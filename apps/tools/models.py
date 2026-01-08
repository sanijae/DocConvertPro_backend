"""
Models for Tools app.
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Document(models.Model):
    """Document model for storing converted files."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    file = models.FileField(upload_to='pdf_documents/')
    converted_file_url = models.URLField(blank=True)
    file_type = models.CharField(max_length=50, blank=True)  # pdf, word, excel, etc.
    conversion_type = models.CharField(max_length=100, blank=True)  # pdf_to_word, word_to_pdf, etc.
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'documents'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.file_type} - {self.uploaded_at}"


class DigitalSignature(models.Model):
    """Digital signature model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='digital_signatures', null=True, blank=True)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    signed_file_url = models.URLField(blank=True)
    signature = models.BinaryField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'digital_signatures'
        verbose_name = 'Digital Signature'
        verbose_name_plural = 'Digital Signatures'
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.name} - {self.date_created}"
