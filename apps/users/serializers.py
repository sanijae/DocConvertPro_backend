"""
Serializers for User app.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, APIKey, Contact, PasswordResetToken


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    profile_image = serializers.ImageField(use_url=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'email_verified', 'conversion_count', 'total_files', 'role',
            'profile_image', 'is_active', 'date_joined', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'date_joined', 'created_at', 'updated_at', 'conversion_count', 'total_files']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user."""
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    name = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'name']
        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True, 'allow_null': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True}
        }
    
    def validate(self, attrs):
        """Validate that passwords match and map name to first_name if provided."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Map 'name' field to 'first_name' if 'name' is provided and 'first_name' is not
        if 'name' in attrs and attrs['name']:
            if 'first_name' not in attrs or not attrs.get('first_name'):
                attrs['first_name'] = attrs['name']
        
        return attrs
    
    def create(self, validated_data):
        """Create a new user."""
        from .services import UserService
        
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        
        # Remove 'name' field if it exists (already mapped to first_name in validate)
        validated_data.pop('name', None)
        
        # Get username or None
        username = validated_data.pop('username', None)
        if username:
            username = username.strip()
        if not username:
            username = None
        
        # Get email
        email = validated_data.pop('email')
            
        user = UserService.create_user(
            email=email,
            username=username,
            password=password,
            **validated_data
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    profile_image = serializers.ImageField(use_url=True, required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'profile_image']


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        """Validate that new passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "New password fields didn't match."})
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for forgot password request."""
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        """Validate that email exists in the system."""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email address.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for resetting password with token."""
    token = serializers.UUIDField(required=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        """Validate that new passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "New password fields didn't match."})
        return attrs
    
    def validate_token(self, value):
        """Validate that token exists and is valid."""
        try:
            token_obj = PasswordResetToken.objects.get(token=value)
            if not token_obj.is_valid():
                raise serializers.ValidationError("Invalid or expired token.")
            return token_obj
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")


class APIKeySerializer(serializers.ModelSerializer):
    """Serializer for API Key model."""
    class Meta:
        model = APIKey
        fields = ['id', 'key', 'end_date', 'is_active', 'date_created']
        read_only_fields = ['id', 'key', 'date_created']


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'title', 'message', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']
