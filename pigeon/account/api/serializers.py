from rest_framework import serializers
from account.models import Account
from django.contrib.auth.models import User
# Import library for password hashing
from django.contrib.auth.hashers import make_password


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'password']
        read_only_fields = ['id']

class RegistrationSerializer(serializers.ModelSerializer):
    password_verify = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password_verify']

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password_verify = self.validated_data['password_verify']

        if password != password_verify:
            raise serializers.ValidationError(
                {'password': 'Passwords must match'})
        # Now passwords won't be displayed in plain-text over the REST API admin interface
        # password = make_password(self.validated_data['password'])
        account.set_password(password)
        account.save()
        return account
