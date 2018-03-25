from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def secure_password(self, validated_data):
        if "password" in validated_data:
            pw = validated_data['password']
            validated_data['password'] = make_password(pw)
        return validated_data

    def create(self, validated_data):
        return super().create(self.secure_password(validated_data))

    def update(self, instance, validated_data):
        if "password" in validated_data:
            pw = validated_data['password']
            validated_data['password'] = make_password(pw)
        return super().update(instance, self.secure_password(validated_data))

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': False,
                                     'style': {'input_type': 'password'}}}


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
