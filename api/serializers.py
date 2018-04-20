"""
Define api model serializers
"""

from rest_framework import serializers
from .models import (
    Package,
    Status,
)


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for package status
    """
    class Meta:
        model = Status
        fields = ('id', 'package', 'latitude',
                  'longitude', 'elevation', 'created', 'url')


class PackageStatusSerializer(StatusSerializer):
    """
    Serializer for package status
    shown in package resource endpoint
    """
    class Meta:
        model = Status
        fields = ('id', 'package', 'latitude',
                  'longitude', 'elevation', 'created', 'url')
        extra_kwargs = {'package': {'read_only': True}}

    def to_representation(self, instance):
        # get the default representation
        ret = super().to_representation(instance)
        ret.pop('package', None)
        return ret


class PackageSerializer(serializers.ModelSerializer):
    """
    Serializer for package
    """

    tracking = PackageStatusSerializer(many=True, read_only=True)
    status = serializers.HyperlinkedIdentityField(
        view_name='package-tracking')

    class Meta:
        model = Package
        fields = ('id', 'description', 'status', 'tracking', 'url')
