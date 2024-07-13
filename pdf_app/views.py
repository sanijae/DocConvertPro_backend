import base64
from datetime import timedelta
import cv2
import numpy as np
import pytesseract
import os
import random
import PyPDF2
import PyPDF4
import tabula
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from  tabula import read_pdf
from pdf_office import settings
from django.http import HttpResponseNotFound
from .serializer import *
from rest_framework import status
from pdf2docx import Converter
from django.shortcuts import get_object_or_404, redirect
from .models import DigitalSignature, Document
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import zipfile
import fitz
from PIL import Image
from reportlab.lib.pagesizes import letter
import subprocess
import img2pdf
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from .digital_sign import *
from django.utils import timezone
from django.shortcuts import render



## User Views ##

# User = get_user_model()

def index(request):
    return  render(request, 'index.html', {})

def dashboard(request):
    try:
        document = Plans.objects.all()
        documents = PlanSerializer(document, many=True)

        digital_sign = DigitalSignature.objects.all()
        digital_signs =DigitalSignatureSerializer(digital_sign,many=True)

        api = APIKey.objects.all()
        apis =APiSerializer(api,many=True)

        queryset = UsersModel.objects.all()
        users =UserSerializer(queryset,many=True)

        payment = Payments.objects.all()
        payments =PaymentSerializer(payment,many=True)

        plan = Plans.objects.all()
        plans =PlanSerializer(plan,many=True)
        
        return  render(request, 'pages/dashboard.html', {
            "api_key":apis.data,
            'documents':documents.data,
            "digital_sign":digital_signs.data,
            "users":users.data,
            "payments":payments.data,
            "plans":plans.data
            })
    except:
        return HttpResponseNotFound('Error while fetching data',status=status.HTTP_404_NOT_FOUND)

def tables(request):
    try:
        document = Plans.objects.all()
        documents = PlanSerializer(document, many=True)

        digital_sign = DigitalSignature.objects.all()
        digital_signs =DigitalSignatureSerializer(digital_sign,many=True)

        api = APIKey.objects.all()
        apis =APiSerializer(api,many=True)

        queryset = UsersModel.objects.all()
        users =UserSerializer(queryset,many=True)

        payment = Payments.objects.all()
        payments =PaymentSerializer(payment,many=True)

        plan = Plans.objects.all()
        plans =PlanSerializer(plan,many=True)
        
        return  render(request, 'pages/tables.html', {
            "api_key":apis.data,
            'documents':documents.data,
            "digital_sign":digital_signs.data,
            "users":users.data,
            "payments":payments.data,
            "plans":plans.data
            })
    except:
        return HttpResponseNotFound('Error while fetching data',status=status.HTTP_404_NOT_FOUND)

def billing(request):
    try:
        queryset = UsersModel.objects.all()
        users =UserSerializer(queryset,many=True)

        payment = Payments.objects.all()
        payments =PaymentSerializer(payment,many=True)

        plan = Plans.objects.all()
        plans =PlanSerializer(plan,many=True)
        
        return  render(request, 'pages/billing.html', {
            "users":users.data,
            "payments":payments.data,
            "plans":plans.data
            })
    except:
        return HttpResponseNotFound('Error while fetching data',status=status.HTTP_404_NOT_FOUND)
    
def notifications(request):
    contact = Contact.objects.all()
    contacts =ContactSerializer(contact,many=True)
    return  render(request, 'pages/notifications.html', {'contacts':contacts.data})

def profile(request):
    return  render(request, 'pages/profile.html', {})

def signIn(request):
    return  render(request, 'pages/sign-in.html', {})

def signUp(request):
    return  render(request, 'pages/sign-up.html', {})


class RegisterAPIView(generics.CreateAPIView):
    queryset = UsersModel.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password')
        role = request.data.get('role', 'user')

        if email and UsersModel.objects.filter(email=email).exists():
            return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(password)
        mutable_data = request.data.copy()
        mutable_data['password'] = hashed_password
        mutable_data['role'] = role
        serializer = self.get_serializer(data=mutable_data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        user_instance = UsersModel.objects.get(email=email)  # Retrieve the user instance
        plan_instance = Plans.objects.create(user=user_instance, plan_name='Free',conversion_limit=5, price=0, is_active=True, date_created=timezone.now())
        user_instance.plan = plan_instance
        user_instance.save()
        user_data = serializer.data
        return Response({"message": "Registration successful", "user": user_data}, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                user = UsersModel.objects.get(email=email)
            except UsersModel.DoesNotExist:
                return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

            if not check_password(password, user.password):
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'email_verified': user.email_verified,
            }
            return Response({"message": "Login successful", "user": user_data}, status=status.HTTP_200_OK)
        
        return Response({"error": "Validation error"}, status=status.HTTP_400_BAD_REQUEST)

class ForgetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = UsersModel.objects.get(email=email)
                otp = random.randint(100000, 999999)
                token_expiration = timezone.now() + timezone.timedelta(minutes=15)
                print('OTP: ',otp)
                print('expire in: ',token_expiration)
                print(email)
                
                user.password_reset_token = otp
                user.reset_token_expiration = token_expiration
                user.save()
                
                subject = 'Password reset request'
                email_html = render_to_string('password_reset.html', {'token': otp})
                # sender = 'noreply@yourwebsite.com'
                recipient = [email]
                user_data = {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'email_verified': user.email_verified,
                }
                
                send_mail(subject, None, recipient_list=recipient, html_message=email_html, fail_silently=False,from_email=False)
                return Response({"message": "Password reset code sent to "+ email, 'user':user_data}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'validation failed, please try again'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        # email = request.data.get('email')
        otp = request.data.get('otp')
        email = request.data.get('email')
        try:
            user = UsersModel.objects.get(email=email)
            if not otp:
                return Response({"error": "Enter OTP send to you"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = UsersModel.objects.get(password_reset_token=otp)
                if user.password_reset_token == otp:
                    if user.reset_token_expiration and user.reset_token_expiration > timezone.now():
                        user_data = {
                            'id': user.id,
                            'name': user.name,
                            'email': user.email,
                            'email_verified': user.email_verified
                        }
                        return Response({"message": "OTP verified successfully",'user':user_data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except UsersModel.DoesNotExist:
                return Response({"error": "invalid code, please the valid code"}, status=status.HTTP_404_NOT_FOUND)
        except:
            Response({'error':'request failed, please try again'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateEmailAPIView(APIView):
    def put(self, request,user_id, *args, **kwargs):
        try:
            user = UsersModel.objects.get(id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(instance=user, validated_data=serializer.validated_data)
            user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'email_verified': user.email_verified,
            }
            return Response({'detail': 'Email updated successfully','user':user_data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdatePasswordAPIView(generics.UpdateAPIView):
    def put(self, request, user_id):
        try:
            user = UsersModel.objects.get(id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdatePasswordSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            current_password = request.data.get('password')
            new_password = make_password(request.data.get('new_password'))
            if not check_password(current_password, user.password):
                return Response({'error': 'The current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            user.password = new_password
            user.save()
            user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'email_verified': user.email_verified
            }
            return Response({"message": "Password updated successfully", "user": user_data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid input, please try again"}, status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordAPIView(generics.UpdateAPIView):
    def put(self, request,user_id):
        try:
            user = UsersModel.objects.get(id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChangePasswordSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'email_verified': user.email_verified
            }
            return Response({"message": "Password updated successfully", "user":user_data}, status=status.HTTP_200_OK)
        return Response({"error": "error please try again"}, status=status.HTTP_404_NOT_FOUND)
        

class ProfileImageView(generics.UpdateAPIView):
    def put(self, request, user_id):
        try:
            user = UsersModel.objects.get(id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileImageSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'email_verified': user.email_verified,
                'profile_image': serializer.data['profile_image']
            }
            return Response({"message": "Profile updated successfully", "user":user_data}, status=status.HTTP_200_OK)
        return Response({'error':'Failed to validate input'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def GetUserAPIView(request, user_id):
    try:
        user = UsersModel.objects.get(id=user_id)
    except UsersModel.DoesNotExist:
        return Response({"error": "User with this ID does not exist"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def GetUsersAPIView(request):
        queryset = UsersModel.objects.all()
        serializer =UserSerializer(queryset,many=True)
        return Response(serializer.data)

## Subscription ##

@api_view(['POST'])
def create_payment(request):
    serializer = PaymentUpdateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user_id = serializer.validated_data.get('user')
        user_instance = get_object_or_404(UsersModel, id=user_id.id)

        plan = serializer.validated_data.get('plan')
        amount = serializer.validated_data.get('amount')
        ref_code = serializer.validated_data.get('ref_code')
        
        payment_instance, created = Payments.objects.update_or_create(
            user=user_instance,
            defaults={
                'plan':plan,
                'amount': amount,
                'ref_code': ref_code
            }
        )

        update_user_and_plan(user_instance, plan, amount, payment_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_payment(request, id):
    payment = get_object_or_404(Payments, user=id)
    serializer = PaymentUpdateSerializer(payment, data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data.get('user')
        user_instance = get_object_or_404(UsersModel, id=user_id.id)

        plan = serializer.validated_data.get('plan')
        amount = serializer.validated_data.get('amount')
        ref_code = serializer.validated_data.get('ref_code')
        paymentSource = serializer.validated_data.get('paymentSource')

        payment.plan = plan
        payment.amount = amount
        payment.ref_code = ref_code
        payment.paymentSource = paymentSource
        payment.save()

        update_user_and_plan(user_instance, plan, amount, payment)

        return Response(serializer.data)
    return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def update_user_and_plan(user_instance, plan, amount, payment_instance):
    
    try:
        plan_instance = Plans.objects.get(user=user_instance.id)
    except Plans.DoesNotExist:
        return Response({'error': 'Failed to find Plan'}, status=status.HTTP_400_BAD_REQUEST)
    limit = 0
    if plan == 'Basic':
        limit = 50
    elif plan == 'Premium' or plan == 'Extended':
        limit = None
    expires_in = timezone.now() + timezone.timedelta(days=30)
    plan_instance.plan_name = plan
    plan_instance.user = user_instance
    plan_instance.price = amount
    plan_instance.is_active = True
    plan_instance.end_date = expires_in
    plan_instance.payment = payment_instance
    plan_instance.conversion_limit = limit
    plan_instance.save()

    user_instance.plan = plan_instance
    user_instance.payment = payment_instance
    user_instance.save()

@api_view(['GET'])
def GetAllPlans(request):
        documents = Plans.objects.all()
        serializer = PlanSerializer(documents, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def GetPlan(request,plan_id):
        documents = Plans.objects.get(id=plan_id)
        serializer = PlanSerializer(documents)
        return Response(serializer.data)

@api_view(['GET'])
def GetAllPayments(request):
        documents = Payments.objects.all()
        serializer = PaymentSerializer(documents, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def GetPayment(request, user_id):
    try:
        payments = Payments.objects.filter(user=user_id)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    except Payments.DoesNotExist:
        return Response({'error': 'Payment history not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



##  Documents Views ##

@api_view(['GET'])
def GetAllFiles(request):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

@api_view(['POST'])

def PdfToWord(request,user_id):
        api_key = request.headers.get('Api-Key')
        if api_key:
            try:
                user =  get_object_or_404(UsersModel, id=user_id)
            except UsersModel.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                plan =  get_object_or_404(Plans, user=user_id)
            except UsersModel.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

            limits = plan.conversion_limit
            if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
                serializer = DocumentSerializer(data=request.data)
                if serializer.is_valid():
                    document = serializer.save()
                    # Convert PDF to Word and save
                    pdf_path = document.file.path
                    word_file = pdf_path.replace('.pdf', '.docx')
                    cv = Converter(pdf_path)
                    cv.convert(word_file, start=0, end=None)
                    cv.close()
                    # Save URL of the converted word file
                    word_file_name = os.path.basename(word_file)
                    document.converted_file_url = word_file.replace(settings.MEDIA_ROOT, '/media')
                    document.save()
                    user.total_files +=1
                    user.conversion_count +=1
                    user.save()
                    return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'API key is required'}, status=400)



@api_view(['POST'])
#
def WordToPdf(request,user_id):
        api_key = request.headers.get('Api-Key')
        if api_key:
            try:
                user =  get_object_or_404(UsersModel, id=user_id)
            except UsersModel.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                plan =  get_object_or_404(Plans, user=user_id)
            except UsersModel.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            limits = plan.conversion_limit
            if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
                serializer = DocumentSerializer(data=request.data)
                if serializer.is_valid():
                    document = serializer.save()
                    # Convert Word to PDF and save
                    word_path = document.file.path
                    output_file = os.path.splitext(word_path)[0] + '.pdf'
                    file_path = os.path.dirname(word_path)
                    # Convert Excel to PDF
                    try:
                        subprocess.run(['soffice', '--headless', '--invisible', '--convert-to', 'pdf', '--outdir', file_path, word_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    except subprocess.CalledProcessError as e:
                        return Response({'error': 'Conversion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
                    # Save URL of the converted PDF file
                    user.total_files +=1
                    user.conversion_count +=1
                    user.save()
                    pdf_file_name = os.path.basename(output_file)
                    document.converted_file_url = output_file.replace(settings.MEDIA_ROOT, '/media')
                    document.save()
                    
                    return Response({'result': serializer.data, 'file_name': pdf_file_name}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
#
def PdfToPpt(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                # Convert PDF to Word and save
                pdf_path = document.file.path
                ppt_file = os.path.splitext(pdf_path)[0]+ '.pptx'

                try:
                    with open(ppt_file, 'wb') as f:
                        subprocess.run(['pdf2pptx', pdf_path], check=True, stdout=f)
                except subprocess.CalledProcessError as e:
                    return Response({'error': 'Conversion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                user.total_files +=1
                user.conversion_count +=1
                user.save()
                # Save URL of the converted word file
                word_file_name = os.path.basename(ppt_file)
                document.converted_file_url = ppt_file.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
#
def PptToPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            # print(limits)
            if serializer.is_valid():
                document = serializer.save()
                # Convert Word to PDF and save
                ppt_path = document.file.path
                output_file = os.path.splitext(ppt_path)[0] + '.pdf'
                file_path = os.path.dirname(ppt_path)
                # Convert Excel to PDF
                try:
                    subprocess.run(['soffice', '--headless', '--invisible', '--convert-to', 'pdf', '--outdir', file_path, ppt_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                except subprocess.CalledProcessError as e:
                    return Response({'error': 'Conversion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Save URL of the converted PDF file
                user.total_files +=1
                user.conversion_count +=1
                user.save()
                pdf_file_name = os.path.basename(output_file)
                document.converted_file_url = output_file.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                
                return Response({'result': serializer.data, 'file_name': pdf_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def PdfToExcel(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                file_path = document.file.path
                pdf_file = file_path.replace('.pdf', '.xlsx')
                tables = read_pdf(file_path, pages='all', multiple_tables=True)
                combined_df = pd.concat(tables)
                combined_df.to_excel(pdf_file, index=False)
                user.total_files +=1
                user.conversion_count +=1
                user.save()

                file_name = os.path.basename(pdf_file)
                document.converted_file_url = pdf_file.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result': serializer.data, 'file_name': file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
def ExcelToPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                # Convert Excel to PDF and save
                excel_path = document.file.path
                output_file = os.path.splitext(excel_path)[0] + '.pdf'
                file_path = os.path.dirname(excel_path)
                # Convert Excel to PDF
                try:
                    subprocess.run(['soffice', '--headless', '--invisible', '--convert-to', 'pdf', '--outdir', file_path, excel_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                except subprocess.CalledProcessError as e:
                    return Response({'error': 'Conversion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Save URL of the converted PDF file
                print(file_path)
                user.total_files +=1
                user.conversion_count +=1
                user.save()
                pdf_file_name = os.path.basename(output_file)
                document.converted_file_url = output_file.replace(settings.MEDIA_ROOT, '/media')
                document.save()

                return Response({'result': serializer.data, 'file_name': pdf_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def CsvToPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                file_path = document.file.path
                pdf_file = file_path.replace('.csv', '.pdf')
                df = pd.read_csv(file_path)
                doc = SimpleDocTemplate(pdf_file, pagesize=letter)
                data = [df.columns.tolist()] + df.values.tolist()
            # Create Table object
                table = Table(data)
                doc.build([table])
                user.total_files +=1
                user.conversion_count +=1
                user.save()

                file_name = os.path.basename(pdf_file)
                document.converted_file_url = pdf_file.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result': serializer.data, 'file_name': file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def PdfToCsv(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                file_path = document.file.path
                pdf_file = file_path.replace('.pdf', '.csv')
                user.total_files +=1
                user.conversion_count +=1
                user.save()
                tabula.convert_into(file_path,pdf_file,pages='all',output_format='csv')
                file_name = os.path.basename(pdf_file)
                document.converted_file_url = pdf_file.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result': serializer.data, 'file_name': file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def PdfToJpg(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                file_path = os.path.splitext(pdf_path)[0]

                    # Open the PDF
                pdf_document = fitz.open(pdf_path)
                
                # Create the image folder if it doesn't exist
                os.makedirs(file_path, exist_ok=True)

                for page_number in range(len(pdf_document)):
                    # Get the page
                    page = pdf_document.load_page(page_number)
                    
                    # Convert the page to a pixmap
                    pixmap = page.get_pixmap()
                    
                    # Save the pixmap as an image
                    image_path = f"{file_path}/page_{page_number + 1}.jpg"  # Save as PNG format
                    pixmap.save(image_path)
                    
                    print(f"Page {page_number + 1} saved as {image_path}")
                
                # Close the PDF
                pdf_document.close()
                
                # Create a zip file
                zip_file_path = f"{file_path}.zip"
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    # Add all files in the image folder to the zip file
                    for root, _, files in os.walk(file_path):
                        for file in files:
                            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), file_path))

                print(f"Images zipped and saved as {zip_file_path}")
                user.total_files +=1
                user.conversion_count +=1
                user.save()
            
                file_name = os.path.basename(zip_file_path)
                document.converted_file_url = zip_file_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result': serializer.data, 'file_name': file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def PdfToJpeg(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                file_path = os.path.splitext(pdf_path)[0]

                    # Open the PDF
                pdf_document = fitz.open(pdf_path)
                
                # Create the image folder if it doesn't exist
                os.makedirs(file_path, exist_ok=True)

                for page_number in range(len(pdf_document)):
                    # Get the page
                    page = pdf_document.load_page(page_number)
                    
                    # Convert the page to a pixmap
                    pixmap = page.get_pixmap()
                    
                    # Save the pixmap as an image
                    image_path = f"{file_path}/page_{page_number + 1}.jpeg"  # Save as PNG format
                    pixmap.save(image_path)
                    
                    print(f"Page {page_number + 1} saved as {image_path}")
                
                # Close the PDF
                pdf_document.close()
                
                # Create a zip file
                zip_file_path = f"{file_path}.zip"
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    # Add all files in the image folder to the zip file
                    for root, _, files in os.walk(file_path):
                        for file in files:
                            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), file_path))

                print(f"Images zipped and saved as {zip_file_path}")
                user.total_files +=1
                user.conversion_count +=1
                user.save()
            
                file_name = os.path.basename(zip_file_path)
                document.converted_file_url = zip_file_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result': serializer.data, 'file_name': file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def PdfToPng(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                file_path = os.path.splitext(pdf_path)[0]

                    # Open the PDF
                pdf_document = fitz.open(pdf_path)
                
                # Create the image folder if it doesn't exist
                os.makedirs(file_path, exist_ok=True)

                for page_number in range(len(pdf_document)):
                    # Get the page
                    page = pdf_document.load_page(page_number)
                    
                    # Convert the page to a pixmap
                    pixmap = page.get_pixmap()
                    
                    # Save the pixmap as an image
                    image_path = f"{file_path}/page_{page_number + 1}.png"  # Save as PNG format
                    pixmap.save(image_path)
                    
                    print(f"Page {page_number + 1} saved as {image_path}")
                
                # Close the PDF
                pdf_document.close()
                
                # Create a zip file
                zip_file_path = f"{file_path}.zip"
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    # Add all files in the image folder to the zip file
                    for root, _, files in os.walk(file_path):
                        for file in files:
                            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), file_path))

                print(f"Images zipped and saved as {zip_file_path}")
                user.total_files +=1
                user.conversion_count +=1
                user.save()
            
                file_name = os.path.basename(zip_file_path)
                document.converted_file_url = zip_file_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result': serializer.data, 'file_name': file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def PdfToBmp(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                file_path = os.path.splitext(pdf_path)[0]

                # Create the directory if it doesn't exist
                os.makedirs(file_path, exist_ok=True)

                # Open the PDF
                pdf_document = fitz.open(pdf_path)
                # Iterate through each page
                for page_number in range(len(pdf_document)):
                    # Get the page
                    page = pdf_document.load_page(page_number)
                    
                    # Convert the page to a pixmap
                    pixmap = page.get_pixmap()
                    
                    # Save the pixmap as a PNG or JPEG image first
                    temp_image_path = f"{file_path}/temp_page_{page_number + 1}.png"
                    pixmap.save(temp_image_path)
                    
                    # Open the image and convert it to BMP
                    with Image.open(temp_image_path) as image:
                        bmp_image_path = f"{file_path}/page_{page_number + 1}.bmp"
                        image.save(bmp_image_path)
                    
                    print(f"Page {page_number + 1} saved as {bmp_image_path}")
                
                # Close the PDF
                pdf_document.close()
                
                # Create a zip file
                zip_file_path = f"{file_path}.zip"
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    # Add all files in the image folder to the zip file
                    for root, _, files in os.walk(file_path):
                        for file in files:
                            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), file_path))

                print(f"Images zipped and saved as {zip_file_path}")
                user.total_files +=1
                user.conversion_count +=1
                user.save()
            
                file_name = os.path.basename(zip_file_path)
                document.converted_file_url = zip_file_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result': serializer.data, 'file_name': file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def ImageToPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                image_path = document.file.path
                base_path, ext = os.path.splitext(image_path)
                file_path = base_path + '.pdf'
                image = Image.open(image_path)
                pdf_bytes = img2pdf.convert(image_path)
                file = open(file_path, "wb")
                file.write(pdf_bytes)
                image.close()
                file.close()
                user.total_files +=1
                user.conversion_count +=1
                user.save()
                print("Successfully made pdf file")
                file_name = os.path.basename(file_path)
                document.converted_file_url = file_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result': serializer.data, 'file_name': file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def SplitPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                file_path = os.path.splitext(pdf_path)[0]
                os.makedirs(file_path, exist_ok=True)

                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    
                    for page_number in range(len(reader.pages)):
                        writer = PyPDF2.PdfWriter()
                        writer.add_page(reader.pages[page_number])
                        
                        output_pdf = f"{file_path}/page_{page_number + 1}.pdf"
                        with open(output_pdf, 'wb') as output_file:
                            writer.write(output_file)
                
                zip_file_path = f"{file_path}.zip"
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    for root, _, files in os.walk(file_path):
                        for file in files:
                            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), file_path))

                user.total_files +=1
                user.conversion_count +=1
                user.save()
                print(f"Images zipped and saved as {zip_file_path}")
                word_file_name = os.path.basename(zip_file_path)
                document.converted_file_url = zip_file_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
def MergePdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                base_path, _ = os.path.splitext(pdf_path)
                file_path = f"{base_path}_merged.pdf"

                pdf_merger = PyPDF2.PdfMerger()
                files = request.FILES.getlist('file')
                for file in files:
                    pdf_merger.append(file)

                with open(file_path, 'wb') as output_file:
                    pdf_merger.write(output_file)
                user.total_files +=1
                user.conversion_count +=1
                user.save()

                document.converted_file_url = file_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()

                return Response({'result': serializer.data, 'file_name': os.path.basename(file_path)}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def CompressPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                file_path, extension = os.path.splitext(pdf_path)
                compressed_pdf_path = f"{file_path}_compress{extension}"
                command = [
                    'gs',  # Ghostscript command
                    '-sDEVICE=pdfwrite',  # Output device
                    '-dCompatibilityLevel=1.4',
                    '-dNOPAUSE',
                    '-dQUIET',
                    '-dBATCH',
                    '-dPDFSETTINGS=/printer',  # Compression level (change as needed)
                    '-o', compressed_pdf_path,  # Output file
                    pdf_path  
                ]
                user.total_files +=1
                user.conversion_count +=1
                user.save()
                subprocess.run(command)
                word_file_name = os.path.basename(compressed_pdf_path)
                document.converted_file_url = compressed_pdf_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
def ExtractPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                # Convert PDF to Word and save
                pdf_path = document.file.path
                # Add "compress" to the file name before the extension
                file_path, extension = os.path.splitext(pdf_path)
                extracted_pdf_path = f"{file_path}_extracted_pages{extension}"
                start_page = int(request.data['start'])  # Corrected usage
                end_page = int(request.data['end'])  # Corrected usage

                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    writer = PyPDF2.PdfWriter()

                    for page_number in range(start_page - 1, end_page):
                        writer.add_page(reader.pages[page_number])

                    with open(extracted_pdf_path, 'wb') as output_file:
                        writer.write(output_file)

                user.total_files +=1
                user.conversion_count +=1
                user.save()
                # Save URL of the converted word file
                word_file_name = os.path.basename(extracted_pdf_path)
                document.converted_file_url = extracted_pdf_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def RemovePdfPage(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                file_path, extension = os.path.splitext(pdf_path)
                extracted_pdf_path = f"{file_path}_modified{extension}"

                # remove_pages = request.data.get('page', [])
                remove_pages_str = request.data.get('page', [])
                remove_pages = remove_pages_str.split(',')
                remove_pages = [int(page) for page in remove_pages]
                print(remove_pages)
                if not isinstance(remove_pages, list):
                    remove_pages = [remove_pages]

                try:
                    remove_pages = [int(page) for page in remove_pages]
                except ValueError:
                    return Response({'error': 'Invalid page numbers provided'}, status=status.HTTP_400_BAD_REQUEST)
                    
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    writer = PyPDF2.PdfWriter()

                    for page_number, page in enumerate(reader.pages):
                        # print(page_number)
                        if page_number + 1 not in remove_pages:
                            writer.add_page(page)

                    with open(extracted_pdf_path, 'wb') as output_file:
                        writer.write(output_file)


                user.total_files +=1
                user.conversion_count +=1
                user.save()
                # Save URL of the modified PDF file
                word_file_name = os.path.basename(extracted_pdf_path)
                document.converted_file_url = extracted_pdf_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result': serializer.data, 'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def AddPdfPage(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                file_path, extension = os.path.splitext(pdf_path)
                extracted_pdf_path = f"{file_path}_modified{extension}"
                page_to_add = request.FILES['add_page']
                
                if not page_to_add:
                    return Response({'error': 'No file uploaded for adding page'}, status=status.HTTP_400_BAD_REQUEST)
                
                print(page_to_add)
                after_page = int(request.data.get('after_page'))
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    writer = PyPDF2.PdfWriter()
                    for page_number in range(after_page):
                        writer.add_page(reader.pages[page_number])

                    page_reader = PyPDF2.PdfReader(page_to_add)
                    for page in page_reader.pages:
                        writer.add_page(page)

                    for page_number in range(after_page, len(reader.pages)):
                        writer.add_page(reader.pages[page_number])

                    with open(extracted_pdf_path, 'wb') as output_file:
                        writer.write(output_file)

                user.total_files +=1
                user.conversion_count +=1
                user.save()

                word_file_name = os.path.basename(extracted_pdf_path)
                document.converted_file_url = extracted_pdf_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def RepairPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                # Convert PDF to Word and save
                pdf_path = document.file.path
                # Add "compress" to the file name before the extension
                file_path, extension = os.path.splitext(pdf_path)
                extracted_pdf_path = f"{file_path}_repaired{extension}"

                # Open the input PDF in read-binary mode
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    
                    # Create a new PDF writer
                    writer = PyPDF2.PdfWriter()

                    # Iterate through each page of the input PDF
                    for page_number in range(len(reader.pages)):
                        try:
                            # Try to read the page
                            page = reader.pages[page_number]
                            # Add the page to the writer
                            writer.add_page(page)
                        except Exception as e:
                            # If there's an error reading the page, skip it and continue
                            print(f"Error reading page {page_number + 1}: {e}")
                            return Response(f"Error reading page {page_number + 1}: {e}", status=status.HTTP_400_BAD_REQUEST)
                        
                    # Write the repaired PDF to the output file
                    with open(extracted_pdf_path, 'wb') as output_file:
                        writer.write(output_file)


                user.total_files +=1
                user.conversion_count +=1
                user.save()
                # Save URL of the converted word file
                word_file_name = os.path.basename(extracted_pdf_path)
                document.converted_file_url = extracted_pdf_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
def RotatePdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                file_path, extension = os.path.splitext(pdf_path)
                extracted_pdf_path = f"{file_path}_rotated{extension}"

                rotation_angle = int(request.data.get('angle'))

                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    writer = PyPDF2.PdfWriter()

                    for page_number in range(len(reader.pages)):
                        page = reader.pages[page_number]
                        page.rotate(rotation_angle)
                        writer.add_page(page)

                    with open(extracted_pdf_path, 'wb') as output_file:
                        writer.write(output_file)


                user.total_files +=1
                user.conversion_count +=1
                user.save()
                # Save URL of the converted word file
                word_file_name = os.path.basename(extracted_pdf_path)
                document.converted_file_url = extracted_pdf_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
def AddWatermark(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                # Convert PDF to Word and save
                pdf_path = document.file.path
                # Add "compress" to the file name before the extension
                file_path, extension = os.path.splitext(pdf_path)
                extracted_pdf_path = f"{file_path}_watermarked{extension}"
                watermark_file = request.FILES['watermark']

                if not watermark_file:
                    return Response({'error': 'No file uploaded for adding page'}, status=status.HTTP_400_BAD_REQUEST)
                # Open the input PDF and watermark PDF
                with open(pdf_path, 'rb') as input_file:
                    reader = PyPDF2.PdfReader(input_file)
                    watermark_reader = PyPDF2.PdfReader(watermark_file)
                    watermark_page = watermark_reader.pages[0]

                    # Create a new PDF writer
                    writer = PyPDF2.PdfWriter()

                    # Overlay the watermark on each page of the input PDF
                    for page_number in range(len(reader.pages)):
                        page = reader.pages[page_number]
                        page.merge_page(watermark_page)  # Merge the watermark onto the page
                        writer.add_page(page)

                    # Write the modified PDF to the output file
                    with open(extracted_pdf_path, 'wb') as output_file:
                        writer.write(output_file)


                user.total_files +=1
                user.conversion_count +=1
                user.save()
                # Save URL of the converted word file
                word_file_name = os.path.basename(extracted_pdf_path)
                document.converted_file_url = extracted_pdf_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
def ProtectPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                # Convert PDF to Word and save
                pdf_path = document.file.path
                # Add "compress" to the file name before the extension
                file_path, extension = os.path.splitext(pdf_path)
                extracted_pdf_path = f"{file_path}_protected{extension}"

                user_password = request.data.get('user_password')
                owner_password = request.data.get('owner_password')

                # Open the input PDF
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF4.PdfFileReader(file)
                    
                    # Create a PDF writer object
                    writer = PyPDF4.PdfFileWriter()
                    
                    # Add each page to the writer
                    for page in reader.pages:
                        writer.addPage(page)
                    
                    # Set encryption options
                    encryption_kwargs = {
                        'user_pwd': user_password,
                        'owner_pwd': owner_password,
                        'use_128bit': False  # Use AES-256 encryption
                    }
                    writer.encrypt(**encryption_kwargs)
                    
                    # Write the protected PDF to the output file
                    with open(extracted_pdf_path, 'wb') as output_file:
                        writer.write(output_file)


                user.total_files +=1
                user.conversion_count +=1
                user.save()
                # Save URL of the converted word file
                word_file_name = os.path.basename(extracted_pdf_path)
                document.converted_file_url = extracted_pdf_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
def UnProtectPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                # Convert PDF to Word and save
                pdf_path = document.file.path
                # Add "watermarked" to the file name before the extension
                file_path, extension = os.path.splitext(pdf_path)
                extracted_pdf_path = f"{file_path}_unlocked{extension}"
                password = request.data.get('password')

                # Open the input PDF
                pdf_document = fitz.open(pdf_path)
                
                # Attempt to unlock the PDF with the provided password
                if pdf_document.is_encrypted:
                    try:
                        pdf_document.authenticate(password)
                        pdf_document.save(extracted_pdf_path)
                        pdf_document.close()
                        # Save URL of the extracted PDF file
                        extracted_pdf_file_name = os.path.basename(extracted_pdf_path)
                        document.converted_file_url = extracted_pdf_path.replace(settings.MEDIA_ROOT, '/media')
                        document.save()
                        user.total_files +=1
                        user.conversion_count +=1
                        user.save()
                        return Response({'result':serializer.data,'file_name': extracted_pdf_file_name}, status=status.HTTP_201_CREATED)
                    except:
                        return Response("Incorrect password. Unable to unlock PDF.", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("PDF is not encrypted. No password required.", status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)



@api_view(['POST'])
def SignPdf(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                pdf_path = document.file.path
                file_path, extension = os.path.splitext(pdf_path)
                extracted_pdf_path = f"{file_path}{extension}"
                print(extracted_pdf_path)
                user.total_files +=1
                user.conversion_count +=1
                user.save()
            
                word_file_name = os.path.basename(extracted_pdf_path)
                document.converted_file_url = extracted_pdf_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                return Response({'result':serializer.data,'file_name': word_file_name}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def Digital_signature(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DigitalSignatureSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                file_path = document.file.path
                file_path_without_extension, ext = os.path.splitext(file_path)
                signed_pdf_path = f"{file_path_without_extension}_signed{ext}"
                signature_info_path = f"{file_path_without_extension}_signature_info.txt"
                # signature_info_pdf = f"{file_path_without_extension}_signature_info.pdf"
                zip_folder_path = f"{file_path_without_extension}.zip"
                name = request.data.get('name')
                file_content = document.file.read()
                
                signature = private_key.sign(
                    file_content,
                    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                    hashes.SHA256()
                )
                
                public_key_base64 = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).decode()
                
                signature_base64 = base64.b64encode(signature).decode()
                with open(signature_info_path, 'w') as txt_file:
                    txt_file.write(f"Public Key:\n{public_key_base64}\n\nSignature:\n{signature_base64}")

                path = os.path.dirname(signature_info_path)
                signature_info_pdf = f"{file_path_without_extension}_signature_info.pdf"
                try:
                    subprocess.run(['soffice', '--headless', '--invisible', '--convert-to', 'pdf', '--outdir', path, signature_info_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                except subprocess.CalledProcessError as e:
                    return Response({'error': 'Conversion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                os.rename(file_path, signed_pdf_path)
                with zipfile.ZipFile(zip_folder_path, 'w') as zip_file:
                    zip_file.write(signed_pdf_path, os.path.basename(signed_pdf_path))
                    zip_file.write(signature_info_pdf, os.path.basename(signature_info_pdf))
                    # zip_file.write(signature_info_path, os.path.basename(signature_info_path))
                
                file_name = os.path.basename(zip_folder_path)
                document.name = name
                document.signature = signature
                document.signed_file_url = zip_folder_path.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                
                user.total_files +=1
                user.conversion_count +=1
                user.save()
                os.remove(signed_pdf_path)
                os.remove(signature_info_pdf)
                os.remove(signature_info_path)
                return Response({'result': serializer.data, 'file_name': file_name, 'public key': public_key_base64}, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
def Verify_digital_signature(request,user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user =  get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan =  get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                file_content = document.file.read()
                public_key_str = request.data.get('public_key')
                signature_str = request.data.get('signature')
                
                try:
                    public_key_obj = serialization.load_pem_public_key(public_key_str.encode())
                    signature_base64 = base64.b64decode(signature_str)
                    public_key_obj.verify(
                        signature_base64,
                        file_content,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    user.total_files +=1
                    user.conversion_count +=1
                    user.save()
                    return Response({'result': serializer.data, 'message': 'This digital signature is still valid.'}, status=status.HTTP_200_OK)
                except InvalidSignature:
                    return Response({'message': 'Digital signature is not valid.'}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Invalid signature.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)


@api_view(['POST'])
def ocr_image_document(request, user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user = get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan = get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                file_path = document.file.path
                language = request.data.get('language')
                file_path_without_extension, ext = os.path.splitext(file_path)
                ocr_path = f"{file_path_without_extension}_text_extracted.txt"

                # Perform OCR on the uploaded image
                image = Image.open(document.file)
                text = pytesseract.image_to_string(image, lang=language)
                # print(text)
                with open(ocr_path, 'w') as txt_file:
                    txt_file.write(f"Extracted content:\n{text}")

                path = os.path.dirname(ocr_path)
                text_info_pdf = f"{file_path_without_extension}_text_extracted.pdf"
                try:
                    subprocess.run(['soffice', '--headless', '--invisible', '--convert-to', 'pdf', '--outdir', path, ocr_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                except subprocess.CalledProcessError as e:
                    return Response({'error': 'Conversion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Save the extracted text to the document
                file_name = os.path.basename(text_info_pdf)
                document.converted_file_url = text_info_pdf.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                os.remove(ocr_path)
                os.remove(file_path)
                # os.remove(text_info_pdf)
                user.total_files +=1
                user.conversion_count +=1
                user.save()

                return Response({'result': serializer.data, 'file_name':file_name, 'content': text}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Ohh, is like you exceed the monthly limit, upgrade your plan to enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)

@api_view(['POST'])
def ocr_identity_document(request, user_id):
    api_key = request.headers.get('Api-Key')
    if api_key:
        try:
            user = get_object_or_404(UsersModel, id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan = get_object_or_404(Plans, user=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        limits = plan.conversion_limit
        if limits is None or user.conversion_count < limits or user.role == 'admin' or plan.plan_name in ['Extended', 'Premium']:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save()
                file_path = document.file.path
                file_path_without_extension, ext = os.path.splitext(file_path)
                ocr_path = f"{file_path_without_extension}_text_extracted.txt"
                ocr_noise = f"{file_path_without_extension}_remove_noise{ext}"
                ocr_sample = f"{file_path_without_extension}_sample{ext}"
                img = cv2.imread(file_path)

                # Convert to gray
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Apply dilation and erosion to remove some noise
                kernel = np.ones((7, 6), np.uint8)
                #print(kernel)
                img = cv2.dilate(img, kernel, iterations=1)
                img = cv2.erode(img, kernel, iterations=1)

                # Write image after removed noise
                cv2.imwrite(ocr_noise, img)

                # Write the image after apply opencv to do some
                cv2.imwrite(ocr_sample, img)

                image = Image.open(ocr_sample)
                text = pytesseract.image_to_string(image)
                print(text)
                with open(ocr_path, 'w') as txt_file:
                    txt_file.write(f"Extracted content:\n{text}")

                path = os.path.dirname(ocr_path)
                text_info_pdf = f"{file_path_without_extension}_extracted_content.pdf"
                try:
                    subprocess.run(['soffice', '--headless', '--invisible', '--convert-to', 'pdf', '--outdir', path, ocr_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                except subprocess.CalledProcessError as e:
                    return Response({'error': 'Conversion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Save the extracted text to the document
                file_name = os.path.basename(text_info_pdf)
                document.converted_file_url = text_info_pdf.replace(settings.MEDIA_ROOT, '/media')
                document.save()
                os.remove(ocr_path)
                os.remove(file_path)
                # os.remove(text_info_pdf)

                user.total_files +=1
                user.conversion_count +=1
                user.save()

                return Response({'result': serializer.data, 'file_name':file_name,'content': text}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Ohh, is like you exceed the monthly limit, upgrade your plan to  enjoy unlimited conversion'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'API key is required'}, status=400)




@api_view(['GET'])
def Downloads(request, id):
    try:
        document = Document.objects.get(pk=id)
        file_url = document.converted_file_url
        return redirect(file_url)
    except Document.DoesNotExist:
        return HttpResponseNotFound('File not found')
    
@api_view(['GET'])
def DownloadsSignature(request, id):
    try:
        document = DigitalSignature.objects.get(pk=id)
        file_url = document.signed_file_url
        return redirect(file_url)
    except Document.DoesNotExist:
        return HttpResponseNotFound('File not found')

@api_view(['GET'])
def GetALLDigitalSign(request):
    queryset = DigitalSignature.objects.all()
    serializer =DigitalSignatureSerializer(queryset,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)    


## Api section ##
@api_view(['POST'])
def create_api_key(request, user_id):
    try:
        user = get_object_or_404(UsersModel, id=user_id)
    except UsersModel.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the API key already exists
    try:
        api_key = APIKey.objects.get(user=user)
        return Response({"api_key": api_key.key}, status=status.HTTP_200_OK)
    except APIKey.DoesNotExist:
        # Create a new API key
        end_date = timezone.now() + timezone.timedelta(days=30)
        end_date = timezone.now() + timedelta(days=30)
        api_key = APIKey.objects.create(
            user=user,
            end_date=end_date,
            is_active=True,
        )
        return Response({"api_key": api_key.key}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def GetAPIKEY(request, user_id):
    try:
        api = APIKey.objects.get(user=user_id)
    except APIKey.DoesNotExist:
        return Response({"error": "Cant find this api now, please try again"}, status=status.HTTP_404_NOT_FOUND)

    serializer = APiSerializer(api)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def GetAPIKEYS(request):
    queryset = APIKey.objects.all()
    serializer =APiSerializer(queryset,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


## Delete sections ##


class UsersModelDeleteView(APIView):
    def delete(self, request, id):
        try:
            user = UsersModel.objects.get(id=id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UsersModel.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

class PlansDeleteView(APIView):
    def delete(self, request, id):
        try:
            plan = Plans.objects.get(id=id)
            plan.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Plans.DoesNotExist:
            return Response({"error": "Plan does not exist"}, status=status.HTTP_404_NOT_FOUND)

class PaymentsDeleteView(APIView):
    def delete(self, request, id):
        try:
            payment = Payments.objects.get(id=id)
            payment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Payments.DoesNotExist:
            return Response({"error": "Payment does not exist"}, status=status.HTTP_404_NOT_FOUND)

class DocumentDeleteView(APIView):
    def delete(self, request, id):
        try:
            document = Document.objects.get(id=id)
            document.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response({"error": "Document does not exist"}, status=status.HTTP_404_NOT_FOUND)

class DigitalSignatureDeleteView(APIView):
    def delete(self, request, id):
        try:
            signature = DigitalSignature.objects.get(id=id)
            signature.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DigitalSignature.DoesNotExist:
            return Response({"error": "DigitalSignature does not exist"}, status=status.HTTP_404_NOT_FOUND)

class APIKeyDeleteView(APIView):
    def delete(self, request, id):
        try:
            api_key = APIKey.objects.get(id=id)
            api_key.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except APIKey.DoesNotExist:
            return Response({"error": "APIKey does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
class ContactCreateView(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user_instance = get_object_or_404(UsersModel, id=user_id)
        
        serializer = UpdateContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user_instance)
            return Response({'result': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def GetAllContact(request):
        contact = Contact.objects.all()
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def GetContact(request,contact_id):
        contact = Contact.objects.get(id=contact_id)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

class ContactDeleteView(APIView):
    def delete(self, request, contact_id):
        try:
            contact = Contact.objects.get(id=contact_id)
            contact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:
            return Response({"error": "Contact does not exist"}, status=status.HTTP_404_NOT_FOUND)