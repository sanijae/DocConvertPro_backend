"""
Serializers for Tools app.
"""
from rest_framework import serializers
from .models import Document, DigitalSignature


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'user', 'file', 'file_url', 'converted_file_url', 'file_type', 
                  'conversion_type', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
    
    def get_file_url(self, obj):
        """Get file URL."""
        if obj.file:
            return obj.file.url
        return None


class DigitalSignatureSerializer(serializers.ModelSerializer):
    """Serializer for DigitalSignature model."""
    file_url = serializers.SerializerMethodField()
    signed_file_url = serializers.URLField(read_only=True)
    
    class Meta:
        model = DigitalSignature
        fields = ['id', 'user', 'name', 'file', 'file_url', 'signed_file_url', 'date_created']
        read_only_fields = ['id', 'date_created']
    
    def get_file_url(self, obj):
        """Get file URL."""
        if obj.file:
            return obj.file.url
        return None
