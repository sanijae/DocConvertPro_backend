"""
Common utility functions used across the application.
"""
import uuid
import hashlib
from typing import Optional


def generate_unique_id() -> str:
    """Generate a unique identifier."""
    return str(uuid.uuid4())


def hash_file_content(content: bytes) -> str:
    """Generate SHA-256 hash of file content."""
    return hashlib.sha256(content).hexdigest()


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


def is_image_file(filename: str) -> bool:
    """Check if file is an image based on extension."""
    image_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg'}
    return get_file_extension(filename) in image_extensions


def is_document_file(filename: str) -> bool:
    """Check if file is a document based on extension."""
    doc_extensions = {'pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 'xls', 'xlsx', 'ppt', 'pptx', 'csv'}
    return get_file_extension(filename) in doc_extensions


def is_pdf_file(filename: str) -> bool:
    """Check if file is a PDF."""
    return get_file_extension(filename) == 'pdf'
