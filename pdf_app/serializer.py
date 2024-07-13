from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.profile_image:
            representation['profile_image'] = instance.profile_image.url
        return representation

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = ['id','name', 'email', 'password','role']
        read_only_fields = ['id'] 


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = ['password']


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = ['password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
    
class UpdatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = ['password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)



class UpdateEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = ['email']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save(update_fields=['email'])
        return instance


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = ['profile_image']

    
## subscriptions ##
class PlanSerializer(serializers.ModelSerializer):
    formatted_date_created = serializers.SerializerMethodField()
    class Meta:
        model = Plans
        fields = '__all__'

    def get_formatted_date_created(self, obj):
        return obj.date_created.strftime('%d/%m/%Y')

class PlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ['plan_name', 'user','price','payment','is_active','end_date']

class PaymentSerializer(serializers.ModelSerializer):
    formatted_date_created = serializers.SerializerMethodField()
    class Meta:
        model = Payments
        fields = '__all__'
    
    def get_formatted_date_created(self, obj):
        return obj.date_created.strftime('%d/%m/%Y')

class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['user', 'plan','amount','paymentSource','ref_code']

## Document Serializer ##
class DocumentSerializer(serializers.ModelSerializer):
    formatted_date_created = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = '__all__'

    def get_formatted_date_created(self, obj):
        return obj.uploaded_at.strftime('%d/%m/%Y')
    
class DigitalSignatureSerializer(serializers.ModelSerializer):
    formatted_date_created = serializers.SerializerMethodField()
    class Meta:
        model = DigitalSignature
        fields = '__all__'

    def get_formatted_date_created(self, obj):
        return obj.date_created.strftime('%d/%m/%Y')

class APiSerializer(serializers.ModelSerializer):
    formatted_date_created = serializers.SerializerMethodField()

    class Meta:
        model = APIKey
        fields = '__all__'

    def get_formatted_date_created(self, obj):
        return obj.date_created.strftime('%d/%m/%Y')
    

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def get_formatted_date_created(self, obj):
        return obj.date_created.strftime('%d/%m/%Y')

class UpdateContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [ 'name', 'email', 'message','title']