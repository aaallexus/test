from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from .settings import api_settings
from rest_framework.exceptions import ValidationError

_usermodel = get_user_model()


class BriefUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api_v1:users-detail',
        lookup_field='pk'
    )

    class Meta:
        model = _usermodel
        fields = ('url', 'username', 'email', 'groups', 'first_name', 'last_name', 'is_active',)
        read_only_fields = fields


class FullUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = _usermodel
        fields = ('id', 'url', 'username', 'email', 'groups', 'first_name', 'last_name', 'is_active',
                  'is_staff', 'is_superuser')
        extra_kwargs = {
            'is_superuser': {'read_only': True},
            'id': {'read_only': True},
            'url': {'view_name': 'api_v1:users-detail', 'lookup_field': 'pk'},
        }


class SuperUserAccessSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'already_is': 'User have superuser rights already'
    }

    class Meta:
        model = _usermodel
        fields = ('is_superuser',)
        extra_kwargs = {'is_superuser': {'write_only': True}}

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.instance.is_superuser:
            return attrs
        else:
            self.fail("already_is")


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    default_error_messages = {
        'cannot_create_user': 'Something happened. We cannot create new user '
    }

    class Meta:
        model = _usermodel
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
        extra_kwargs = {'password': {'write_only': True, 'input_type': 'password'}}

    def validate(self, attrs):
        user = _usermodel(**attrs)
        password = attrs.get('password')
        try:
            validate_password(password, user=user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {'password': serializer_error['non_field_errors']}
            )
        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = _usermodel.objects.create_user(**validated_data)
            if api_settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        user = self.context["user"]
        # why assert? There are ValidationError / fail everywhere
        assert user is not None
        try:
            validate_password(attrs["new_password"], user)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})
    re_new_password = serializers.CharField(style={"input_type": "password"})
    current_password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        "password_mismatch": "Password fields didn't match. Please try again.",
        "invalid_password": "Invalid password."
    }

    def validate_current_password(self, value):
        is_password_valid = self.context["request"].user.check_password(value)
        if is_password_valid:
            return value
        else:
            self.fail("invalid_password")

    def validate(self, attrs):
        # must provide user existance test...
        user = self.context["request"].user
        # if user is non None...
        try:
            validate_password(attrs["new_password"], user)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        if attrs["new_password"] == attrs["re_new_password"]:
            return attrs
        else:
            self.fail("password_mismatch")

