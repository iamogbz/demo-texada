from rest_framework import serializers
from .models import Package, Status


class StatusSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Status
        fields = ('id', 'package', 'latitude',
                  'longitude', 'elevation', 'created', 'url')


class PackageStatusSerializer(StatusSerializer):
    def to_representation(self, instance):
        # get the default representation
        ret = super().to_representation(instance)
        ret.pop('package', None)
        return ret


class PackageSerializer(serializers.ModelSerializer):
    tracking = PackageStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ('id', 'description', 'tracking', 'url')
