from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'password')
        extra_kwargs = {'password': {'write_only': True,
                                     'style': {'input_type': 'password'}}}


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
