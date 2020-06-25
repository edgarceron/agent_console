"""Contains the serializers for the users module"""
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for users model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'lastname', 'active',
                  'profile', 'need_password']

    def create(self, validated_data):
        user_obj = User(**validated_data)
        user_obj.save()
        return user_obj

    def update(self, instance, validated_data):
        instance.username = validated_data["username"]
        instance.password = validated_data["password"]
        instance.name = validated_data["name"]
        instance.lastname = validated_data["lastname"]
        instance.active = validated_data["active"]
        instance.profile = validated_data["profile"]
        instance.save()
        return instance

    def reset_password(self):
        self.need_password = True
        self.save()
        return self

class BasicUserSerializer(serializers.ModelSerializer):
    """A class for serialize an user just with the most basic fields"""
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'lastname', 'active']
