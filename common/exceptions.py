"""
Custom exceptions for the application.
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class StorageLimitExceeded(APIException):
    """Exception raised when user exceeds storage limit."""
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    default_detail = 'Storage limit exceeded.'
    default_code = 'storage_limit_exceeded'


class FileNotFound(APIException):
    """Exception raised when file is not found."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'File not found.'
    default_code = 'file_not_found'


class PermissionDenied(APIException):
    """Exception raised when user doesn't have permission."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Permission denied.'
    default_code = 'permission_denied'


class InvalidFileType(APIException):
    """Exception raised when file type is not allowed."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid file type.'
    default_code = 'invalid_file_type'


class ConversionLimitExceeded(APIException):
    """Exception raised when user exceeds conversion limit."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Conversion limit exceeded for your plan.'
    default_code = 'conversion_limit_exceeded'


class SubscriptionRequired(APIException):
    """Exception raised when subscription is required."""
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'Active subscription required.'
    default_code = 'subscription_required'
