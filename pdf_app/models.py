from django.utils import timezone
import uuid
from django.db import models
import secrets

class UsersModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=100)
    conversion_count = models.IntegerField(default=0)
    total_files = models.IntegerField(default=0)
    role = models.CharField(max_length=100,default='user')
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    reset_token_expiration = models.DateTimeField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    payment = models.OneToOneField('Payments', null=True, blank=True, on_delete=models.CASCADE)
    plan = models.OneToOneField('Plans', null=True, blank=True, on_delete=models.CASCADE)


class Plans(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_name = models.CharField(max_length=100,default='Free')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    conversion_limit = models.IntegerField(default=0, null=True, blank=True)
    user = models.OneToOneField(UsersModel,blank=True, null=True, on_delete=models.CASCADE)
    payment = models.OneToOneField('Payments',blank=True, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    end_date = models.DateField(blank=True, null=True)
    date_created = models.DateTimeField(default= timezone.now)

class Payments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UsersModel, blank=True, null=True, on_delete=models.CASCADE)
    plan = models.CharField(max_length=200, blank=True, default='')
    paymentSource = models.CharField(max_length=100,blank=True,default='')
    amount = models.PositiveIntegerField()
    ref_code = models.CharField(max_length=200, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    file = models.FileField(upload_to='pdf_documents/')
    converted_file_url = models.URLField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# class OCRDocument(models.Model):
#     file = models.FileField(upload_to='pdf_documents/')
#     converted_file_url = models.URLField(blank=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

class DigitalSignature(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    signed_file_url = models.URLField(blank=True)
    signature = models.BinaryField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class APIKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=200, default=secrets.token_urlsafe)
    user = models.OneToOneField(UsersModel, on_delete=models.CASCADE)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.TextField(default='')
    message = models.TextField(default='')
    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name