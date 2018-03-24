from rest_framework import serializers
from .models import Package, Status


class PackageSerializer(serializers.ModelSerializer):
    tracking = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='status-detail')

    class Meta:
        model = Package
        fields = ('id', 'description', 'tracking',)


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ('package', 'latitude', 'longitude', 'elevation',)
